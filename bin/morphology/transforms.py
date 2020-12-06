import numpy as np

from . import _distance_transform, _sharpness_transform
from . import _edge_detection, _medial_axis_transform
from . import _skeletonisation


def skeleton_transform(array: np.ndarray):
    return _skeletonisation.zhan_suen(array)


def medial_axis_transform(array: np.ndarray):
    return _medial_axis_transform.medial_axis_transform(array)


def distance_transform(array: np.ndarray):
    return _distance_transform.distance_transform(array)


def sharpness_transform(array: np.ndarray):
    return _sharpness_transform.sharpness_transform(array)


def edge_transform(array: np.ndarray):
    return _edge_detection.edge_detect(array)



