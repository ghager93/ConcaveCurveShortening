import numpy as np

import bin.image_array as image_array
import bin.image_array_ops as image_array_ops


def get_distance_transform(array: np.ndarray):
    return _by_edge_detection(array)


def _by_edge_detection(array: np.ndarray):
    out = np.zeros(array.shape)
    while array.any():
        out += array
        array -= image_array_ops.edge_detect(array)

    return out