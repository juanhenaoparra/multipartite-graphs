import numpy as np

def product_tensor(matrix: np.ndarray, row: int = None):
    """
    Do product tensor of a matrix with m rows and n columns. Being n columns with 2 states.

    The resultant matrix shape will be: (m , 2^(n/2))

    If the row parameter is passed, the resultant matrix shape will be: (1, 2^(n/2))
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
