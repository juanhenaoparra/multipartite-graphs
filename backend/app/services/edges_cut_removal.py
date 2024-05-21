import numpy as np
from app.services.matching import CheckBipartite
from app.schemas.graphs import GraphSchema
from app.schemas.generation import GenGraphInput
from app.services.gen_graph import GenerateGraph, TransformToGraphSchema, generateNodeLabels
from .matrix import get_binary_position, product_tensor, recursive_marginalization, expand_matrix, get_emd


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
            new_weight=0.0
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

def calculate_edges_costs(p_matrix: np.ndarray, binary_distribution: str, presentNodesCount: int, futureNodesCount: int, base_effect: tuple, base_cause: tuple):
    original_distribution = product_tensor(p_matrix, row=get_binary_position(binary=binary_distribution))

    g_dict = GenerateGraph(
      GenGraphInput(
        nodesNumber=presentNodesCount+futureNodesCount,
        isBipartite=True,
        presentNodesCount=presentNodesCount,
        futureNodesCount=futureNodesCount,
      )
    )

    all_labels = generateNodeLabels(futureNodesCount)
    labels = {
      "effects": {i: l+"'" for i, l in enumerate(all_labels) },
      "causes": {i: l for i, l in enumerate(all_labels) }
    }

    anti_labels = {
      "effects": {l+"'": i for i, l in enumerate(all_labels) },
      "causes": {l: i for i, l in enumerate(all_labels) }
    }

    g = TransformToGraphSchema(g_dict)

    p_m = p_matrix.copy()

    class MinCut:
        cost = float('inf')
        connected_components = None
        graph = None

    min_cut: MinCut = MinCut()

    for effect in range(3):
        subscriptors = g.get_nodes_pointing_to(labels["effects"][effect])
        subscriptors.sort(key=lambda n: n.label)

        for sub in subscriptors:
            cause_node_int = anti_labels["causes"][sub.label]
            target_cause = tuple(i for i in range(3) if i != cause_node_int)

            res = evaluate_edge_removal(g, labels, p_m, original_distribution, binary_distribution, effect, target_cause, base_effect, base_cause)

            if res.cost == 0:
                p_m = res.new_matrix # replace the matrix with the modified matrix if the cost is 0

            if len(res.connected_components) == 2 and res.cost < min_cut.cost:
                min_cut.cost = res.cost
                min_cut.connected_components = res.connected_components

    return [g, min_cut]