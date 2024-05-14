from typing import Dict, Tuple
import numpy as np
from pydantic import BaseModel
from .matrix import get_binary_position, product_tensor_with_cut, marginalize

class Memo(BaseModel):
    matrix: Dict[Tuple, Dict[Tuple, np.ndarray]] = {}

    class Config:
        arbitrary_types_allowed = True

    def get(self, effect: tuple, cause: tuple):
        try:
            m = self.matrix[effect][cause]
            return m
        except:
            return None

    def add(self, effect: tuple, cause: tuple, m):
        if self.get(effect=effect, cause=cause) is not None:
            return

        if self.matrix.get(effect) is None:
            self.matrix[effect] = {}

        self.matrix[effect][cause] = m

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

    diff_target_cause = list(set(base_cause).difference(target_cause))
    diff_target_cause.sort()

    leftmost_row_index = get_binary_position(binary=binary_distribution)
    leftmost_resultant = p_matrix[leftmost_row_index, [leftmost_target*2, (leftmost_target*2)+1]][np.newaxis, :]

    if len(diff_target_cause) > 0:
        memoized_left_matrix = memo.get((leftmost_target,), target_cause)
        if memoized_left_matrix:
            leftmost_resultant = memoized_left_matrix
        else:
            leftmost_resultant = marginalize(matrix=leftmost_resultant, tensors=len(base_cause), positions=diff_target_cause, axis=1)
            memo.add((leftmost_target,), target_cause, leftmost_resultant)

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

    memo.add(target_effect, target_cause, r)

    return r