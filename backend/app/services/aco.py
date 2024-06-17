import numpy as np
import random
from copy import deepcopy
from app.services.matching import CheckBipartite
from app.schemas.graphs import GraphSchema
from app.schemas.generation import GenGraphInput
from app.services.gen_graph import GenerateGraph, TransformToGraphSchema, generateNodeLabels
from .edges_cut_removal import calculate_edges_costs
from .compare_partitions import MinimumPartitionResponse

class AntColony:
    def __init__(self, graph: GraphSchema, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        if not isinstance(graph, GraphSchema):
            raise ValueError("Expected a GraphSchema instance.")
        self.graph = graph
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.graph.set_nodes_map()
        nodes = self.graph.data
        self.pheromone = [[1 / (len(nodes) * len(nodes))] * len(nodes) for _ in range(len(nodes))]

    def run(self):
        best_solutions = []
        for i in range(self.n_iterations):
            all_paths = self.construct_solutions()
            if i == 1:
                print("la feromona", self.pheromone)
            self.spread_pheronome(all_paths, self.n_best)
            best_solutions.append(min(all_paths, key=lambda x: x[1]))
            self.evaporate_pheromone()

        partitions = self.generate_partitions()
        print("la feromona", self.pheromone)
        return best_solutions, partitions

    def construct_solutions(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.construct_path(0)
            all_paths.append((path, self.path_length(path)))
        return all_paths

    def construct_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.graph.data) - 1):
            move = self.select_move(self.pheromone[prev], self.get_distances(prev), visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def get_distances(self, node_idx):
        node_id = self.graph.data[node_idx].id
        distances = [float('inf')] * len(self.graph.data)
        for edge in self.graph.data[node_idx].linkedTo:
            to_node_idx = self.get_node_index_by_id(edge.nodeId)
            distances[to_node_idx] = edge.weight if edge.weight is not None else float('inf')
        return distances

    def get_node_index_by_id(self, node_id):
        for idx, node in enumerate(self.graph.data):
            if node.id == node_id:
                return idx
        raise ValueError(f"Node id {node_id} not found in graph.")

    def select_move(self, pheromone, distances, visited):
        pheromone = list(pheromone)
        pheromone = [p ** self.alpha for p in pheromone]
        attractiveness = [1 / d if d > 0 else 0 for d in distances]
        row = zip(pheromone, attractiveness)
        row = [(phero, attr) for phero, attr in row if attr != 0 and attr not in visited]
        if not row:
            return random.choice([i for i in range(len(distances)) if i not in visited])
        norm_row = [phero * attr for phero, attr in row]
        sum_row = sum(norm_row)
        norm_row = [nr / sum_row for nr in norm_row]
        move = random.choices(range(len(row)), norm_row)[0]
        return move

    def path_length(self, path):
        total_distance = 0
        for ele in path:
            total_distance += self.get_distances(ele[0])[ele[1]]
        return total_distance

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                weight = self.get_distances(move[0])[move[1]]
                if weight > 0:  # Evitar división por cero
                    self.pheromone[move[0]][move[1]] += 1.0 / weight

    def evaporate_pheromone(self):
        self.pheromone = [[self.decay * phero for phero in row] for row in self.pheromone]

    def generate_partitions(self):
        pheromone_edges = []
        for i in range(len(self.pheromone)):
            for j in range(len(self.pheromone[i])):
                pheromone_edges.append((self.pheromone[i][j], i, j))
        pheromone_edges.sort(reverse=True, key=lambda x: x[0])

        for _, i, j in pheromone_edges:
            if i == j:
                continue  # No actualizar aristas entre un nodo y sí mismo

            from_node_id = self.graph.data[i].id
            to_node_id = self.graph.data[j].id

            # Verificar si la arista existe antes de intentar actualizar
            from_node = self.graph.get_node_by_id(from_node_id)
            if from_node and any(edge.nodeId == to_node_id for edge in from_node.linkedTo):
                # Crear una copia del grafo y eliminar el borde con la mayor cantidad de feromonas
                temp_graph = deepcopy(self.graph)  # Usar deepcopy para clonar el grafo correctamente
                temp_graph.update_edge_weight(from_node_id=from_node_id, to_node_id=to_node_id, new_weight=0.0)

                bip = CheckBipartite(g=temp_graph)
                bip.exclude_zero_weights = True
                check_bipartite_res = bip.process()

                if check_bipartite_res.isBipartite and len(check_bipartite_res.connectedComponents) == 2:
                    partitions = [[], []]
                    for idx, component in enumerate(check_bipartite_res.connectedComponents.values()):
                        for node in component:
                            partitions[idx].append(node)
                    return partitions
            else:
                print(f"Arista no encontrada: {from_node_id} -> {to_node_id}")

        # Retornar particiones vacías si no se encuentra una bipartición válida
        return [[], []]

def run_aco(p_matrix: np.ndarray, binary_distribution: str, presentNodesCount: int, futureNodesCount: int, base_effect: tuple, base_cause: tuple):
    p_matrix = np.array(p_matrix)

    response = MinimumPartitionResponse(
        binary_distribution=binary_distribution,
    )

    g_dict = GenerateGraph(
        GenGraphInput(
            nodesNumber=presentNodesCount + futureNodesCount,
            isBipartite=True,
            presentNodesCount=presentNodesCount,
            futureNodesCount=futureNodesCount,
        )
    )

    g = TransformToGraphSchema(g_dict)

    min_cut, adjayency_matrix = calculate_edges_costs(
        p_matrix=p_matrix,
        binary_distribution=binary_distribution,
        presentNodesCount=presentNodesCount,
        futureNodesCount=futureNodesCount,
        base_effect=base_effect,
        base_cause=base_cause,
        g=g
    )

    response.graph = g.model_dump()

    if min_cut.cost < float('inf'):
        response.distance = min_cut.cost
        response.partition = min_cut.connected_components

        return response

    # ACO based con adjayency matrix
    ant_colony = AntColony(graph=g, n_ants=len(adjayency_matrix) * 2, n_best=2, n_iterations=100, decay=0.85, alpha=-1, beta=1)
    best_solutions, partitions = ant_colony.run()
    response.partition = partitions

    return response
