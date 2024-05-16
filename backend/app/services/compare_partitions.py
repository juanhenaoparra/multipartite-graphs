from typing import Dict, Tuple
import numpy as np
from pydantic import BaseModel
from .matrix import get_binary_position, product_tensor_with_cut, recursive_marginalization, get_emd
from .partitions_generator import gen_system_partitions

class Memo(BaseModel):
    binary_distribution: str = ""
    matrix: Dict[Tuple, Dict[Tuple, np.ndarray]] = {}
    marginalizations: Dict[Tuple, Dict[Tuple, np.ndarray]] = {}

    class Config:
        arbitrary_types_allowed = True

    def get(self, effect: tuple, cause: tuple, scope=None):
        space = self.matrix

        if scope == "MG":
            space = self.marginalizations

        try:
            m = space[effect][cause]
            return m
        except:
            return None

    def add(self, effect: tuple, cause: tuple, m, scope=None):
        space = self.matrix

        if scope == "MG":
            space = self.marginalizations

        if self.get(effect=effect, cause=cause, scope=scope) is not None:
            return

        if space.get(effect) is None:
            space[effect] = {}

        space[effect][cause] = m

class MinimumPartitionResponse(BaseModel):
    binary_distribution: str
    partition: list
    distance: float

def find_insertion_pos(l, to_insert):
    for i, num in enumerate(l):
        if num >= to_insert:
            return i

    return len(l)

def get_probability_distribution(p_matrix: np.ndarray, binary_distribution: str, target_effect: tuple, target_cause:tuple, base_cause: tuple, memo: Memo):
    """
    Calculate the probability distribution of a target effect given a target cause and a base cause.
    The strategy used at this level is top-down recursion with memoization.
    Where the probability distribution of the target effect is calculated by the product tensor of the leftmost target effect variable and the probability distribution of the rightest target effect, which is calculated recursively.

    The memoization structure is accessed by a target effect and a target cause.

    Args:
        p_matrix (np.ndarray): The probability matrix.
        binary_distribution (str): The binary distribution of the system.
        target_effect (tuple): The target effect to calculate the probability.
        target_cause (tuple): The target cause to calculate the probability.
        base_cause (tuple): The base cause of the target effect.
        memo (Memo): The memoization object to store the results.

    Returns:
        np.ndarray: The probability distribution of the target effect given the target cause and the base cause.
    """
    if not target_effect or len(target_effect) == 0:
        return None

    memoized_matrix = memo.get(target_effect, target_cause)
    if memoized_matrix is not None:
        return memoized_matrix

    leftmost_target, *rightest = target_effect
    rightest = tuple(rightest)

    base_cause_set = set(base_cause)
    diff_target_cause = list(base_cause_set.difference(target_cause))
    diff_target_cause.sort()

    leftmost_row_index = get_binary_position(binary=binary_distribution)
    leftmost_columns = [leftmost_target*2, (leftmost_target*2)+1]
    leftmost_resultant = p_matrix[leftmost_row_index, leftmost_columns][np.newaxis, :]

    if len(diff_target_cause) > 0:
        memoized_left_matrix = memo.get((leftmost_target,), target_cause)
        if memoized_left_matrix:
            leftmost_resultant = memoized_left_matrix
        else:
            lefmost_marginalized = recursive_marginalization(
                matrix=p_matrix[:, leftmost_columns],
                tensors=len(base_cause),
                positions=diff_target_cause,
                axis=1,
            )

            memo.add(target_effect, target_cause, lefmost_marginalized, scope="MG")

            leftmost_row_index = get_binary_position(binary=binary_distribution, mask=target_cause)
            leftmost_resultant = lefmost_marginalized[leftmost_row_index, [0, 1]][np.newaxis, :]

    rightest_resultant = get_probability_distribution(
        p_matrix=p_matrix,
        binary_distribution=binary_distribution,
        target_effect=rightest,
        target_cause=target_cause,
        base_cause=base_cause,
        memo=memo,
    )

    if rightest_resultant is None:
        return leftmost_resultant

    memo.add(rightest, target_cause, rightest_resultant) # memoize rightest resultant

    concatenated_matrix = np.concatenate([leftmost_resultant, rightest_resultant], axis=1)
    row_index = get_binary_position(binary=binary_distribution, mask=target_cause)
    cut = leftmost_resultant.shape[1]
    insert_position = find_insertion_pos(l=rightest, to_insert=leftmost_target)

    r = product_tensor_with_cut(concatenated_matrix, row_index, cut=cut, left_side_exp=[insert_position])

    memo.add(target_effect, target_cause, r) # memoize resultant

    return r

def calculate_partition_distance(matrix: np.ndarray, original: np.ndarray, binary_distribution: str, base_cause: tuple, partitions: list[tuple], memo: Memo):
    """
    Calculate the distance between two partitions of a system given a matrix and a binary distribution.

    Args:
        matrix (np.ndarray): The matrix of the system.
        original (np.ndarray): The original matrix of the system.
        binary_distribution (str): The binary distribution of the system.
        base_cause (tuple): The base cause of the system.
        partitions (list[tuple]): A list containing the partitions of the system.
        memo (Memo): The memoization object to store the results.

    Returns:
        float: The distance between the two partitions.
    """
    partition_a = get_probability_distribution(p_matrix=matrix, binary_distribution=binary_distribution, target_effect=partitions[0], target_cause=partitions[1], base_cause=base_cause, memo=memo)

    partition_b = get_probability_distribution(p_matrix=matrix, binary_distribution=binary_distribution, target_effect=partitions[2], target_cause=partitions[3], base_cause=base_cause, memo=memo)

    partition_joined = np.concatenate([partition_a, partition_b], axis=1)
    partition_joined_m = product_tensor_with_cut(partition_joined, 0, partition_a.shape[1], partitions[1])

    return get_emd(original[0], partition_joined_m[0])

def calculate_minimum_partition(full_system: list, matrix, binary_distribution: str) -> MinimumPartitionResponse:
    """
    Calculate the minimum partition of a system given a matrix and a binary distribution.

    Args:
        original_system (list): The original system.
        matrix (np.ndarray): The matrix of the system.
        binary_distribution (str): The binary distribution of the system.

    Returns:
        MinimumPartitionResponse: The minimum partition of the system with its details
    """
    memo = Memo(binary_distribution=binary_distribution)
    partitions = gen_system_partitions(matrix)
    base_effect = tuple(matrix[0])
    base_cause = tuple(matrix[1])

    full_system = np.array(full_system)

    original_distribution = get_probability_distribution(p_matrix=full_system, binary_distribution=binary_distribution, target_effect=base_effect, target_cause=base_cause, base_cause=base_cause, memo=memo)

    min_distance = float("inf")
    min_partition = None

    for partition in partitions:
        distance = calculate_partition_distance(full_system, original_distribution, binary_distribution, base_cause, partition, memo)
        absolute_distance = abs(distance)

        if absolute_distance < min_distance:
            min_distance = absolute_distance
            min_partition = partition

    return MinimumPartitionResponse(binary_distribution=binary_distribution, partition=min_partition, distance=min_distance)