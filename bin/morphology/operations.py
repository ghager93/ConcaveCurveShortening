import numpy as np

from bin.morphology import _operations
from bin.morphology import _skeletonisation
from bin.morphology.structuring_element import StructuringElement

from bin.utils.vector2d import Vector2D


def erosion(array: np.ndarray, structuring_element: StructuringElement):
    return _operations.binary_erosion(array, structuring_element)


def dilation(array: np.ndarray, structuring_element: StructuringElement):
    return _operations.binary_dilation(array, structuring_element)


def opening(array: np.ndarray, structuring_element: StructuringElement):
    return _operations.binary_opening(array, structuring_element)


def closing(array: np.ndarray, structuring_element: StructuringElement):
    return _operations.binary_closing(array, structuring_element)


def skeletonisation(array: np.ndarray, structuring_element: StructuringElement):
    return _skeletonisation.binary_skeletonisation(array, structuring_element)