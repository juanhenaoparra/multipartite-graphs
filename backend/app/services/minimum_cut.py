class Queue:
    def __init__(self):
        self.q = []

    def push(self, nodeId, node):
        # Implementa la inserción binaria para detectar la posición del nodo en la cola
        pass

    def pop(self):
        return self.q.pop()

def get_weighted_nodes(V, E):
    n = len(V)
    m = len(E)
    C = [[0, 0, 0] for _ in range(n)]  # Inicializa la matriz C

    for i in range(m):
        nodeIdSource = E[i][0]
        nodeIdSink = E[i][1]
        edgeCost = E[i][2]

        # Incrementa los valores del nodo fuente
        C[nodeIdSource][0] += 1  # Incrementa el grado
        C[nodeIdSource][1] += edgeCost  # Incrementa el min_deletion_cost
        C[nodeIdSource][2] += edgeCost  # Incrementa el max_deletion_cost

        # Incrementa los valores del nodo sumidero
        C[nodeIdSink][0] += 1  # Incrementa el grado
        if edgeCost > C[nodeIdSink][1]:
            C[nodeIdSink][1] = edgeCost  # Establece el min_deletion_cost
        C[nodeIdSink][2] += edgeCost  # Incrementa el max_deletion_cost

    return C

def get_left_right_node_sets(E):
    L = []
    R = []

    for edge in E:
        L.append(edge[0])
        R.append(edge[1])

    return L, R

def get_subgraph(V, E):
    C = get_weighted_nodes(V, E)
    Ordered_C = sorted(enumerate(C), key=lambda x: (-x[1][2], -x[1][0]))  # Ordena por max_deletion_cost y grado
    Q = Queue()

    L, R = get_left_right_node_sets(E)

    L_length = len(L)
    R_length = len(R)

    # Agrega nodos que pertenecen al conjunto L a la cola de prioridad
    for nodeId in L:
        Q.push(nodeId, C[nodeId])

    # Inicializa el límite global con el costo de eliminación mínimo del nodo menos costoso
    min_subgraph = [Ordered_C[-1]]
    G = min_subgraph[0][2]

    explored_nodes = []

    while len(Q.q) > 0:
        _node = Q.pop()
        nodeId = _node[0]
        node = C[nodeId]
        explored_nodes.append(nodeId)

        path = find_augmenting_path_max_flow(nodeId, explored_nodes, L, R)

        for i in range(len(path)):
            nodeId = path[i]
            node = C[nodeId]

            deletion_cost, minimum_edge_cost = calculate_deletion_cost([nodeId] + path[1:i], E)

            if minimum_edge_cost < min_subgraph:
                if deletion_cost == minimum_edge_cost:
                    G = deletion_cost
                    break

                children = get_children_of_node(nodeId)

                for child in children:
                    if child in L or child in R:
                        Q.push(child in L)

    return min_subgraph

def calculate_deletion_cost(path, E):
    deletion_cost = 0
    minimum_edge_cost = float('inf')

    related_edges = get_related_edges_except(path, E)

    for edge in related_edges:
        deletion_cost += edge[2]
        if edge[2] < minimum_edge_cost:
            minimum_edge_cost = edge[2]

    return deletion_cost, minimum_edge_cost
