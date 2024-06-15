import numpy as np
from app.services.matching import CheckBipartite
from app.schemas.graphs import GraphSchema
from app.schemas.generation import GenGraphInput
from app.services.gen_graph import GenerateGraph, TransformToGraphSchema, generateNodeLabels
from .matrix import get_binary_position, product_tensor, recursive_marginalization, expand_matrix, get_emd
from .compare_partitions import MinimumPartitionResponse


class EdgeRemovalResult:
    new_matrix = None
    expanded_matrix = None
    vector_resultant = None
    cost = None
    connected_components = None

    def __init__(self, new_matrix, expanded_matrix, vector_resultant):
        self.new_matrix: np.ndarray = new_matrix
        self.expanded_matrix: np.ndarray = expanded_matrix
        self.vector_resultant: np.ndarray = vector_resultant

class MinCut:
        cost = float('inf')
        connected_components = None
        graph = None
        partition = None

def remove_present_from_effect(p_matrix: np.ndarray, effect: int, target_cause: tuple, base_cause: tuple):
    base_cause_set = set(base_cause)
    diff_target_cause = list(base_cause_set.difference(target_cause))
    diff_target_cause.sort()

    effect_columns = [effect*2, (effect*2)+1]

    effect_marginalized = recursive_marginalization(
        matrix=p_matrix[:, effect_columns],
        tensors=len(base_cause),
        positions=diff_target_cause,
        axis=1,
    )

    expanded_matrix = expand_matrix(
        matrix=effect_marginalized,
        tensors=len(base_cause)-len(diff_target_cause),
        positions=diff_target_cause,
        axis=0
    )

    return expanded_matrix

def get_probability_distribution_with_new_effect(p_matrix: np.ndarray, binary_distribution: str, effect: int, target_cause: tuple, base_cause: tuple):
    expanded_matrix = remove_present_from_effect(p_matrix, effect, target_cause, base_cause)

    new_matrix = p_matrix.copy()
    effect_columns = [effect*2, (effect*2)+1]

    row_index = get_binary_position(binary=binary_distribution)
    new_matrix[:, effect_columns] = expanded_matrix

    return EdgeRemovalResult(
        new_matrix=new_matrix,
        expanded_matrix=expanded_matrix,
        vector_resultant=product_tensor(matrix=new_matrix, row=row_index)
    )

def evaluate_edge_removal(g: GraphSchema, labels: dict, p_matrix: np.ndarray, original_vector: np.ndarray, binary_distribution: str, effect: int, target_cause: tuple, base_effect: tuple, base_cause: tuple):
    base_cause_set = set(base_cause)
    causes_to_remove = list(base_cause_set.difference(target_cause))
    causes_to_remove.sort()

    removal_result = get_probability_distribution_with_new_effect(
        p_matrix=p_matrix,
        binary_distribution=binary_distribution,
        effect=effect,
        target_cause=target_cause,
        base_cause=base_cause)

    distance = get_emd(original_vector[0], removal_result.vector_resultant[0])
    removal_result.cost = distance

    edges_to_restore = []

    for c in causes_to_remove:
        from_node_id = labels["causes"][c]
        to_node_id = labels["effects"][effect]

        g.update_edge_weight(
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            new_weight=0.0,
            color="#FF6B6B",
            lineType="dashed"
        )

        edges_to_restore.append((from_node_id, to_node_id))

    bip = CheckBipartite(g=g)
    bip.exclude_zero_weights = True
    check_bipartite_res = bip.process()

    removal_result.connected_components = check_bipartite_res.connectedComponents

    if removal_result.cost == 0.0:
        return removal_result

    for from_node, to_node in edges_to_restore:
        g.update_edge_weight(
            from_node_id=from_node,
            to_node_id=to_node,
            new_weight=removal_result.cost
        )

    return removal_result

def calculate_edges_costs(p_matrix: np.ndarray, binary_distribution: str, presentNodesCount: int, futureNodesCount: int, base_effect: tuple, base_cause: tuple, g: GraphSchema):
    original_distribution = product_tensor(p_matrix, row=get_binary_position(binary=binary_distribution))

    cause_labels = generateNodeLabels(presentNodesCount)
    effect_labels = generateNodeLabels(futureNodesCount)
    labels = {
      "effects": {i: l+"'" for i, l in enumerate(effect_labels) },
      "causes": {i: l for i, l in enumerate(cause_labels) }
    }

    anti_labels = {
      "effects": {l+"'": i for i, l in enumerate(effect_labels) },
      "causes": {l: i for i, l in enumerate(cause_labels) }
    }

    p_m = p_matrix.copy()
    adjayency_matrix = np.zeros((presentNodesCount, futureNodesCount))

    min_cut: MinCut = MinCut()

    for effect in range(futureNodesCount):
        subscriptors = g.get_nodes_pointing_to(labels["effects"][effect])
        subscriptors.sort(key=lambda n: n.label)

        for sub in subscriptors:
            cause_node_int = anti_labels["causes"][sub.label]
            target_cause = tuple(i for i in range(3) if i != cause_node_int)

            res = evaluate_edge_removal(g, labels, p_m, original_distribution, binary_distribution, effect, target_cause, base_effect, base_cause)

            if res.cost == 0:
                p_m = res.new_matrix # replace the matrix with the modified matrix if the cost is 0
            else:
                adjayency_matrix[cause_node_int, effect] = res.cost

            if len(res.connected_components) == 2 and res.cost < min_cut.cost:
                min_cut.cost = res.cost
                min_cut.connected_components = res.connected_components
                # TODO: find min_cut.partition

    min_cut.graph = g

    return [min_cut, adjayency_matrix]

def get_cut_cost_from_adj_matrix(cost_matrix, rows_sum, columns_sum, rows, columns):
    return abs(rows_sum[rows].sum() + columns_sum[columns].sum() - 2*cost_matrix[rows, :][:, columns].sum())

def walk_heatmap_desc(adj_matrix: np.ndarray):
    rows_sum = adj_matrix.sum(axis=1)
    rows_order = np.argsort(rows_sum)[::-1]

    columns_sum = adj_matrix.sum(axis=0)
    columns_order = np.argsort(columns_sum)[::-1]

    top_limit_rows = len(rows_order) - 1
    rows_count = 0

    min_cut = MinCut()
    min_cut.cost = rows_sum[rows_order[-1]]
    min_cut.partition = [[], [rows_order[-1]]]

    if columns_sum[columns_order[-1]] < min_cut.cost:
        min_cut.cost = columns_sum[columns_order[-1]]
        min_cut.partition = [[columns_order[-1]], []]

    for i, col in enumerate(columns_order[:-1]):
        rows_hold = rows_order[:rows_count+1]
        cols_hold = columns_order[:i+1]

        partition_cost = get_cut_cost_from_adj_matrix(
            cost_matrix=adj_matrix,
            rows_sum=rows_sum,
            columns_sum=columns_sum,
            rows=rows_hold,
            columns=cols_hold,
        )

        if partition_cost < min_cut.cost:
            min_cut.cost = partition_cost
            min_cut.partition = [cols_hold, rows_hold]

        if rows_count < top_limit_rows:
            rows_count += 1

    return min_cut

def calculate_edges_cut(p_matrix: np.ndarray, binary_distribution: str, presentNodesCount: int, futureNodesCount: int, base_effect: tuple, base_cause: tuple):
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

    wal_res = walk_heatmap_desc(adj_matrix=adjayency_matrix)
    response.distance = wal_res.cost
    response.partition = wal_res.partition

    return response
