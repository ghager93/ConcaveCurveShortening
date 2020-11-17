import numpy as np

import bin.image_array as image_array
import bin.morphology as morphology
import bin.flood_fill as flood_fill


def smooth(array: np.ndarray, kernel_radius: int):
    return _smooth_by_binary_opening(array, kernel_radius)


def _smooth_by_binary_opening(array: np.ndarray, kernel_radius: int):
    return morphology.binary_opening(array, morphology.get_circular_structuring_element(kernel_radius))


def edge_detect(array: np.ndarray):
    return _xor_edge_detect(array)


def _xor_edge_detect(array: np.ndarray):
    array = image_array.pad_by_zeroes(array, 1)
    return array[1:-1, 1:-1] & np.invert(array[1:-1, :-2] & array[1:-1, 2:] &
                                         array[:-2, 1:-1] & array[2:, 1:-1])


def _morphology_edge_detect(array: np.ndarray):
    eroded_array = morphology.binary_erosion(array, morphology.get_circular_structuring_element(radius=3))
    return array - eroded_array


def find_polygons(array: np.ndarray):
    return flood_fill.get_polygons(array)


def skeletonise(array: np.ndarray):
    pass
