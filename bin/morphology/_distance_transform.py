import numpy as np
import os
import sys

# print(os.getcwd())
# print(sys.path)

import bin.morphology._adj_edge_detection
from bin.morphology import _adj_operations

# import _adj_edge_detection
# import _adj_operations


def distance_transform(array: np.ndarray):
    return _by_edge_detection(array)


def _by_edge_detection(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array -= bin.morphology._adj_edge_detection.edge_detect(copy_array)
        # copy_array -= _adj_edge_detection.edge_detect(copy_array)

    return out.astype(int)


def _by_erosion(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array = _adj_operations.binary_erosion(copy_array)

    return out
