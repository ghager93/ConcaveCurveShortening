import numpy as np

from bin.util.neighbour_array import get_shifted_neighbour_arrays


def cornerness(array: np.ndarray):
    out = 8-sum(get_shifted_neighbour_arrays(array))
    out[array == 0] = 0

    return out
