import numpy as np

from bin.morphology.utils.neighbour_array import get_shifted_neighbour_arrays


def sharpness_transform(array: np.ndarray):
    out = 8-sum(get_shifted_neighbour_arrays(array))
    out[array == 0] = 0

    return out
