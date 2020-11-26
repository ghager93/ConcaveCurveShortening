import numpy as np

import bin.image_array as image_array
import bin.image_array_ops as image_array_ops
from bin.morphology import basic_ops


def get_distance_transform(array: np.ndarray):
    return _by_edge_detection(array)


def _by_edge_detection(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array -= image_array_ops.edge_detect(copy_array)

    return out.astype(int)


def _by_erosion(array: np.ndarray):
    copy_array = np.copy(array)
    out = np.zeros(copy_array.shape)
    while copy_array.any():
        out += copy_array
        copy_array = basic_ops.binary_erosion(copy_array)

    return out
