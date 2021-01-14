import numpy as np

import bin.image_array as image_array
import bin.morphology._edge_detection
from bin.morphology import _operations


def distance_transform(array: np.ndarray):
    return _by_edge_detection(array)


def _by_edge_detection(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array -= bin.morphology._edge_detection.edge_detect(copy_array)

    return out.astype(int)


def _by_erosion(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array = _operations.binary_erosion(copy_array)

    return out
