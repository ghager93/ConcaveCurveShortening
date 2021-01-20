import numpy as np

from bin import adj_image_array as image_array
from bin.morphology import _adj_operations, adj_structuring_element


def edge_detect(array: np.ndarray):
    return _xor_edge_detect(array)


def _xor_edge_detect(array: np.ndarray):
    array = image_array.pad_by_zeroes(array, 1)
    return array[1:-1, 1:-1] & np.invert(array[1:-1, :-2] & array[1:-1, 2:] &
                                         array[:-2, 1:-1] & array[2:, 1:-1])


def _morphology_edge_detect(array: np.ndarray):
    eroded_array = _adj_operations.binary_erosion(array, adj_structuring_element.circular_structuring_element(radius=3))
    return array - eroded_array