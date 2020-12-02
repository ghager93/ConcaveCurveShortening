import numpy as np

import bin.flood_fill as flood_fill
from bin.morphology import _operations
from bin.morphology import structuring_element


def smooth(array: np.ndarray, kernel_radius: int):
    return _smooth_by_binary_opening(array, kernel_radius)


def _smooth_by_binary_opening(array: np.ndarray, kernel_radius: int):
    return _operations.binary_opening(array, structuring_element.circular_structuring_element(kernel_radius))


def find_polygons(array: np.ndarray):
    return flood_fill.get_polygons(array)
