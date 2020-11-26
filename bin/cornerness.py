import numpy as np

from bin.image_array import pad_by_zeroes


def cornerness(array: np.ndarray):
    out = 8-sum(_get_shifted_neighbour_arrays(array))
    out[array == 0] = 0

    return out


def _get_shifted_neighbour_arrays(array: np.ndarray):
    padded_array = pad_by_zeroes(array)
    return [padded_array[x:padded_array.shape[0] + x-2, y:padded_array.shape[1] + y-2]
            for x in range(3) for y in range(3)
            if x != 1 or y != 1]
