import numpy as np

import bin.image_array as image_array
from bin.util.vector2d import Vector2D


FILTER_FILL_VALUE = 1

FILTER_ARRAY_DTYPE = 'int32'
OUTPUT_ARRAY_DTYPE = 'int32'


class StructuringElement:
    def __init__(self, kernel: np.ndarray, centre: Vector2D):
        self.kernel = kernel
        self.centre = centre


def get_circular_structuring_element(radius: int):
    return StructuringElement(_make_circular_kernel(radius), Vector2D(radius, radius))


def _make_circular_kernel(radius: int):
    filter_shape = _get_kernel_shape(radius)
    circular_kernel = np.zeros(filter_shape, dtype=FILTER_ARRAY_DTYPE)
    xx, yy = np.mgrid[:filter_shape[0], :filter_shape[1]]
    circular_kernel[(xx - radius)**2 + (yy - radius)**2 <= radius**2] = FILTER_FILL_VALUE
    return circular_kernel


def _get_kernel_shape(radius: int):
    return 2*radius + 1, 2*radius + 1


def binary_opening(image: np.ndarray, structuring_element: np.ndarray):
    pass


def binary_closing(image: np.ndarray, structuring_element: np.ndarray):
    pass


def binary_erosion(image: np.ndarray, structuring_element: np.ndarray):
    pass


def binary_dilation(image: np.ndarray, structuring_element: np.ndarray):
    pass


