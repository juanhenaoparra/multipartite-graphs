from itertools import combinations as iter_combinations

def calculate_negative_set(m, a, b):
    """
    Calculate the negative set for a given matrix.
    """
    negative_a = set(m[0]).difference(a)
    negative_b = set(m[1]).difference(b)

    return tuple(negative_a), tuple(negative_b)

def cartesian_product(a, b, len_a, len_b, include_negative_set=False, m=None):
  """
  Calculates the Cartesian product of two lists `a` and `b`.

  The Cartesian product of two sets A and B is the set of ordered pairs (a, b) where a belongs to A and b belongs to B.

  Args:
      a (list): The first list of elements.
      b (list): The second list of elements.
      len_a (int): The length of the first list (assumed to be pre-calculated for efficiency).
      len_b (int): The length of the second list (assumed to be pre-calculated for efficiency).

  Returns:
      list: A list containing all possible combinations (ordered pairs) from the Cartesian product of `a` and `b`.
  """
  prod = []
  items_pushed = set()

  for i in range(len(a)):
      for j in range(len(b)):
          if len(a[i]) == 1 and str(a[i]) not in items_pushed:
              neg_a, neg_b = calculate_negative_set(m, a[i], tuple())
              prod.append([a[i], tuple(), neg_a, neg_b])
              items_pushed.add(str(a[i]))
          if len(b[j]) == 1 and str(b[j]) not in items_pushed:
              neg_a, neg_b = calculate_negative_set(m, tuple(), b[j])
              prod.append([tuple(), b[j], neg_a, neg_b])
              items_pushed.add(str(b[j]))

          neg_a, neg_b = calculate_negative_set(m, a[i], b[j])
          prod.append([a[i], b[j], neg_a, neg_b])

  return prod

def gen_system_partitions(m):
    """
    Generates all possible system partitions for a given matrix `m`.

    Args:
        m (list): A 2D list representing the matrix for which to generate system partitions.

    Returns:
        list: A list containing all possible system partitions represented as a list of lists.
            Each inner list represents a group of related elements (a subset of a row).

    Raises:
        ValueError: If the input matrix `m` is not a 2D list.
    """
    all_combinations =[[], []]

    for i, row in enumerate(m):
      for j in range(1, len(row)): # 1 to n-1 because we don't want to include the full or empty row
          for combination in iter_combinations(row, j):
              all_combinations[i].append(combination)

    return cartesian_product(*all_combinations, len_a=len(m[0]), len_b=len(m[1]), include_negative_set=True, m=m)