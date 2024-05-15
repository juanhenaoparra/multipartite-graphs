import numpy as np
import math

def get_emd(a, b):
    """
    Calculate the Earth Mover's Distance between two sets of points.
    EMD being defined by:
    EMD0 = 0
    EMDi+1 = (Ai+EMDi) - Bi
    """
    n = max(len(a), len(b))

    if len(a) < n:
        a += [0] * (n - len(a))
    elif len(b) < n:
        b += [0] * (n - len(b))

    d = np.zeros(n+1, dtype=np.float128)
    d_sum = 0

    for i in range(1, n+1):
        d[i] = (a[i-1] + d[i-1]) - b[i-1]
        d_sum += d[i]

    return d_sum

def get_binary_position(binary: str, mask=None, unmask=None):
    if mask is not None:
        binary = "".join([binary[i] for i in range(len(binary)) if i in mask])
        if binary == "":
            return 0
    elif unmask is not None:
        binary = "".join([binary[i] for i in range(len(binary)) if i not in unmask])
        if binary == "":
            return 0

    return int(binary[::-1], 2)

def product_tensor_with_cut(matrix: np.ndarray, row: int, cut: int, left_side_exp: list[int]):
    """
    Do product tensor of a matrix given a cut column. The cut column is the column where the matrix will be divided.

    matrix: np.ndarray    -> matrix to do the product tensor
    row: int              -> row to do the product tensor
    cut: int              -> column to do the cut
    left_side_exp: int    -> exponent of the left side of the cut, this is used to calculate the position of  the resulting tensor
    """
    m, n = matrix.shape
    columns = cut * (n - cut)

    vector_tensor = np.full((1, columns), np.nan)
    tensors = round(math.log2(columns))

    if m == 1:
        row = 0

    for i in range(columns):
        full_bin = bin(i)[2:].zfill(tensors)[::-1]
        left_index = get_binary_position(full_bin, mask=left_side_exp)
        right_index = get_binary_position(full_bin, unmask=left_side_exp)

        vector_tensor[0][i] = matrix[row][left_index] * matrix[row][cut+right_index]

    return vector_tensor

def marginalize(matrix: np.ndarray, tensors: int, positions: list, axis: int):
    """
    Marginalize a matrix along an axis removing the position element.

    params:
    matrix: np.ndarray    -> matrix to marginalize
    tensors: int          -> number of tensors
    position: List[int]   -> positions to remove
    axis: int             -> 0: row, 1: column
    """
    m, n = matrix.shape

    if axis == 1:
        new_m = 2 ** (tensors-len(positions))
        new_n = n
    else:
        new_m = m
        new_n = 2 ** (tensors-len(positions))

    new_matrix = np.full((new_m, new_n), np.nan)
    sum_count = 2 ** len(positions)
    top_limit = 0
    step_size = math.inf

    for x in positions:
        x_exp = 2**x
        top_limit += x_exp

        if x_exp < step_size:
            step_size = x_exp

    walked_rows = 0
    counter = 0
    bottom = 0

    max_size = m if axis == 1 else n
    iterator = {x for x in range(max_size)}

    while walked_rows < max_size:
        bottom = min(iterator)
        top = bottom+top_limit
        rows_to_sum = []

        for _ in range(round(sum_count/2)):
            iterator.remove(bottom)
            iterator.remove(top)
            rows_to_sum.append(bottom)
            rows_to_sum.append(top)

            walked_rows += 2
            bottom += step_size
            top -= step_size

        if axis == 1:
            new_matrix[counter , :] = matrix[rows_to_sum , :].sum(axis=0) / 2
        else:
            new_matrix[: , counter] = matrix[: , rows_to_sum].sum(axis=1) / 2

        counter += 1

    return new_matrix

def recursive_marginalization(matrix: np.ndarray, tensors: int, positions: list, axis: int):
    left, *rights = positions

    matrix = marginalize(matrix=matrix, tensors=tensors, positions=[left], axis=axis)
    # TODO: add memoization

    if rights is None or len(rights) == 0:
        return matrix

    decreased_rights = [x-1 for x in rights]

    return recursive_marginalization(matrix=matrix, tensors=tensors-1, positions=decreased_rights, axis=axis)