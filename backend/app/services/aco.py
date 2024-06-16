import numpy as np
import random
from app.services.matching import CheckBipartite
from app.schemas.graphs import GraphSchema
from app.schemas.generation import GenGraphInput
from app.services.gen_graph import GenerateGraph, TransformToGraphSchema, generateNodeLabels
from .edges_cut_removal import calculate_edges_costs
from .compare_partitions import MinimumPartitionResponse

class AntColony:
    def __init__(self, graph, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.graph = graph
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.pheromone = [[1 / (len(graph) * len(graph))] * len(graph) for _ in range(len(graph))]

    def run(self):
        best_solutions = []
        for i in range(self.n_iterations):
            all_paths = self.construct_solutions()
            if i ==1:
                print("la feromona",self.pheromone)
            self.spread_pheronome(all_paths, self.n_best)
            best_solutions.append(min(all_paths, key=lambda x: x[1]))
            self.pheromone = self.evaporate_pheromone()

        partitions = self.generate_partitions()
        print("la feromona",self.pheromone)
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
        for _ in range(len(self.graph) - 1):
            move = self.select_move(self.pheromone[prev], self.graph[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def select_move(self, pheromone, distances, visited):
        pheromone = list(pheromone)
        pheromone = [p ** self.alpha for p in pheromone]
        row = zip(pheromone, distances)
        row = [(phero, dist) for phero, dist in row if dist != 0 and dist not in visited]
        norm_row = [phero / sum(pheromone) for phero, dist in row]
        move = random.choices(range(len(row)), norm_row)
        return move[0]

    def path_length(self, path):
        total_distance = 0
        for ele in path:
            total_distance += self.graph[ele[0]][ele[1]]
        return total_distance

    def spread_pheronome(self, all_paths, n_best):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                weight = self.graph[move[0]][move[1]]
                if weight > 0:  # Evitar división por cero
                    self.pheromone[move[0]][move[1]] += 1.0 / weight




    def evaporate_pheromone(self):
        return [[self.decay * phero for phero in row] for row in self.pheromone]

    def generate_partitions(self):
        threshold = sum(sum(row) for row in self.pheromone) / (len(self.pheromone) * len(self.pheromone))
        partitions = {'A': set(), 'B': set()}
        for i in range(len(self.pheromone)):
            for j in range(len(self.pheromone[i])):
                if self.pheromone[i][j] > threshold:
                    partitions['A'].add(i)
                    partitions['A'].add(j)
                else:
                    partitions['B'].add(i)
                    partitions['B'].add(j)
        return partitions

def run_aco(p_matrix: np.ndarray, binary_distribution: str, presentNodesCount: int, futureNodesCount: int, base_effect: tuple, base_cause: tuple):
    p_matrix = np.array(p_matrix)

    response = MinimumPartitionResponse(
        binary_distribution=binary_distribution,
    )

    g_dict = GenerateGraph(
      GenGraphInput(
        nodesNumber=presentNodesCount+futureNodesCount,
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
    ant_colony = AntColony(adjayency_matrix, len(adjayency_matrix)*2, 2, 100, 0.85, alpha=-1, beta=1)
    best_solutions, partitions = ant_colony.run()
    response.partition = partitions

    return response