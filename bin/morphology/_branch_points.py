import numpy as np

from bin.morphology.utils import neighbour_array


def remove_points_with_2_connected_neighbours(array: np.ndarray):
    out = np.copy(array)
    padded_array = np.pad(array, 1)
    for ix, iy in np.ndindex(array.shape):
        if padded_array[ix+1, iy+1] \
                and neighbour_array.number_of_connected_neighbours(padded_array[ix:ix+3, iy:iy+3]) == 2:
            out[ix, iy] = 0

    return out



