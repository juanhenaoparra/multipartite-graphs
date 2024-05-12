from typing import List
import numpy as np
import math

def product_tensor(matrix: np.ndarray, row: int = None):
    """
    Do product tensor of a matrix with m rows and n columns. Being n columns with 2 states.

    The resultant matrix shape will be: (m , 2^(n/2))

    If the row parameter is passed, the resultant matrix shape will be: (1, 2^(n/2))
    """
    m, n = matrix.shape
    components = int(n/2)
    columns = 2**components

    rows = m if row is None else 1

    m_tensor = np.full((rows, columns), np.nan)
    binary_values_j = {}

    for i in range(m_tensor.shape[0]):
        i_matrix = i
        if row is not None:
            i_matrix = row

        for j in range(m_tensor.shape[1]):
            if j not in binary_values_j:
                binary_values_j[j] = bin(j)[2:].zfill(components)

            positions = [(2*(components-(x+1)) + int(y)) if x < components-1 else int(y) for x, y in enumerate(binary_values_j[j])]

            cell_product = 1

            for k in positions:
                cell_product *= matrix[i_matrix][k]

            m_tensor[i][j] = cell_product

    return m_tensor

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

def marginalize(matrix: np.ndarray, tensors: int, positions: list, axis: int):
    """
    Marginalize a matrix along an axis removing the position element.

    params:
    @matrix: np.ndarray    -> matrix to marginalize
    @position: List[int]   -> positions to remove
    @axis: int             -> 0: row, 1: column
    @significant_side: int -> 0: left, 1: right
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
