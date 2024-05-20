import numpy as np
from app.schemas.graphs import GraphSchema
from app.services.matching import CheckBipartite
from .matrix import get_binary_position, product_tensor, recursive_marginalization, expand_matrix, get_emd


class EdgeRemovalResult:
    new_matrix = None
    expanded_matrix = None
    vector_resultant = None
    cost = None
    connected_components = -1

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

    removal_result.connected_components = len(check_bipartite_res.connectedComponents)

    if removal_result.cost == 0.0:
        return removal_result

    for from_node, to_node in edges_to_restore:
        g.update_edge_weight(
            from_node_id=from_node,
            to_node_id=to_node,
            new_weight=removal_result.cost
        )

    return removal_result
