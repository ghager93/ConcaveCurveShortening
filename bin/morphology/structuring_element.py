import numpy as np

from bin.morphology import KERNEL_ARRAY_DTYPE, KERNEL_FILL_VALUE
from bin.util.vector2d import Vector2D


class StructuringElement:
    def __init__(self, kernel: np.ndarray, centre: Vector2D):
        self.kernel = kernel
        self.centre = centre

    def width(self):
        return self.kernel.shape[0]

    def height(self):
        return self.kernel.shape[1]


def get_circular_structuring_element(radius: int):
    return StructuringElement(_make_circular_kernel(radius), Vector2D(radius, radius))


def _make_circular_kernel(radius: int):
    filter_shape = _get_kernel_shape(radius)
    circular_kernel = np.zeros(filter_shape, dtype=KERNEL_ARRAY_DTYPE)
    xx, yy = np.mgrid[:filter_shape[0], :filter_shape[1]]
    circular_kernel[(xx - radius) ** 2 + (yy - radius) ** 2 <= radius ** 2] = KERNEL_FILL_VALUE
    return circular_kernel


def _get_kernel_shape(radius: int):
    return 2 * radius + 1, 2 * radius + 1


KERNEL_FILL_VALUE = 1
OUTPUT_FILL_VALUE = 1
KERNEL_ARRAY_DTYPE = 'int32'
OUTPUT_ARRAY_DTYPE = 'int32'