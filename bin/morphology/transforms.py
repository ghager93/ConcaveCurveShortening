import numpy as np

from skimage.morphology import skeletonize

from . import _distance_transform
from . import _adj_edge_detection
from . import _adj_medial_axis_transform
from . import _adj_sharpness_transform
from . import _adj_skeletonisation
from . import adj_operations

from .adj_structuring_element import circular_structuring_element
from .utils import neighbour_array


def skeleton_transform(array: np.ndarray):
    return skeletonize(array)


def medial_axis_transform(array: np.ndarray):
    return _adj_medial_axis_transform.medial_axis_transform(array)


def distance_transform(array: np.ndarray):
    return _distance_transform.distance_transform(array)


def sharpness_transform(array: np.ndarray):
    return _adj_sharpness_transform.sharpness_transform(array)


def edge_transform(array: np.ndarray):
    return _adj_edge_detection.edge_detect(array)


def neighbours_transform(array: np.ndarray, hang: bool = True):
    if hang:
        return neighbour_array.get_neighbour_array(array)
    else:
        return neighbour_array.get_neighbour_array_no_hang(array)


def smooth(array: np.ndarray, factor: int):
    return adj_operations.opening(array, circular_structuring_element(factor))



