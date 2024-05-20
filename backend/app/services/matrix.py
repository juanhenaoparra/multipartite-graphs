import numpy as np
import math

def str_bin(number: int | float, size: int):
    return f'{number:0{size}b}'

def hamming_distance(a, b):
    return bin(a^b).count('1')

def get_emd(_a, _b):
    a = _a.copy()
    b = _b.copy()

    len_a = math.log2(len(a))
    len_b = math.log2(len(b))
    max_len = int(max(len_a, len_b))
    le_keys = gen_little_endian_range(max_len)

    total = 0
    a_sorter = np.argsort(a)

    while a[a_sorter[-1]] != 0:
        dB = {
            le_keys.index(str_bin(i, max_len)): e
            for i, e in enumerate(b)
            if e > 0
        }

        le_A_key: int = int(le_keys[a_sorter[-1]], 2)

        all_b_keys = {
            k: hamming_distance(k, le_A_key)
            for k, v in dB.items()
        }

        minimum = min(all_b_keys, key=all_b_keys.get)
        b_key = le_keys.index(str_bin(minimum, max_len))

        restar = min(a[a_sorter[-1]], b[b_key])
        a[a_sorter[-1]] -= restar
        b[b_key] -= restar

        total += restar * all_b_keys[minimum]

        a_sorter = np.argsort(a)

    return total

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

def mask_binary(binary: str, mask = None, unmask = None):
    if mask is not None:
        return "".join([binary[i] for i in range(len(binary)) if i in mask])

    if unmask is not None:
        return "".join([binary[i] for i in range(len(binary)) if i not in unmask])

def product_tensor(matrix: np.ndarray, row: int = None):
    """
    Do product tensor of a matrix.
    """
    m = matrix.shape[0]
    n = matrix.shape[1]
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

def gen_little_endian_range(n: int):
    return [bin(i)[2:].zfill(n)[::-1] for i in range(2**n)]

def expand_matrix(matrix: np.ndarray, tensors: int, positions: list, axis: int = 0):
    m, n = matrix.shape

    matrix_dict = {}
    for v in range(m if axis == 0 else n):
        values = matrix[v] if axis == 0 else matrix[:, v]
        matrix_dict[bin(v)[2:].zfill(tensors)[::-1]] = values

    expected_positions = gen_little_endian_range(tensors+len(positions))

    new_shape = (len(expected_positions), n) if axis == 0 else (m, len(expected_positions))
    new_m = np.zeros(new_shape)

    for pos in expected_positions:
        index = get_binary_position(pos)
        remaining_binaries = mask_binary(pos, unmask=positions)
        if axis == 0:
            new_m[index] = matrix_dict[remaining_binaries]
        else:
            new_m[:, index] = matrix_dict[remaining_binaries]

    return new_m