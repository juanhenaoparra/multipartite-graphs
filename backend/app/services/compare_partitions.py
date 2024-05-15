from typing import Dict, Tuple
import numpy as np
from pydantic import BaseModel
from .matrix import get_binary_position, product_tensor_with_cut, recursive_marginalization

class Memo(BaseModel):
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

def find_insertion_pos(l, to_insert):
    for i, num in enumerate(l):
        if num >= to_insert:
            return i

    return len(l)

def get_probability_distribution(p_matrix: np.ndarray, binary_distribution: str, target_effect: tuple, target_cause:tuple, base_cause: tuple, memo: Memo):
    if not target_effect or len(target_effect) == 0:
        return None

    memoized_matrix = memo.get(target_effect, target_cause)
    if memoized_matrix:
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

    r = product_tensor_with_cut(concatenated_matrix, row_index, cut=cut, left_side_exp=insert_position)

    memo.add(target_effect, target_cause, r) # memoize resultant

    return r