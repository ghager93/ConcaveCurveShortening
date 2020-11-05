import numpy as np

import bin.image_array as image_array
from bin.util.vector2d import Vector2D

KERNEL_FILL_VALUE = 1
OUTPUT_FILL_VALUE = 1

KERNEL_ARRAY_DTYPE = 'int32'
OUTPUT_ARRAY_DTYPE = 'int32'


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


def binary_opening(array: np.ndarray, structuring_element: StructuringElement):
    return binary_dilation(binary_erosion(array, structuring_element), structuring_element)


def binary_closing(array: np.ndarray, structuring_element: StructuringElement):
    return binary_erosion(binary_dilation(array, structuring_element), structuring_element)


def binary_erosion(array: np.ndarray, structuring_element: StructuringElement):
    _assert_structuring_element_smaller_than_or_equal_to_array(array, structuring_element)
    padded_array = image_array.pad_by_ones(array, structuring_element.centre.x)
    output_array = _initialise_output_array(padded_array.shape)
    for ix, iy in _padded_array_index(padded_array.shape, structuring_element.centre.x):
        if _kernel_is_subset_of_array_segment(
                structuring_element.kernel,
                padded_array[ix:ix + structuring_element.width(), iy:iy + structuring_element.height()]
        ):
            output_array[ix:ix + structuring_element.centre.x, iy:iy + structuring_element.centre.y] = KERNEL_FILL_VALUE

    return image_array.remove_pad(output_array, structuring_element.centre.x)


def binary_dilation(array: np.ndarray, structuring_element: StructuringElement):
    _assert_structuring_element_smaller_than_or_equal_to_array(array, structuring_element)
    padded_array = image_array.pad_by_zeroes(array, structuring_element.centre.x)
    output_array = _initialise_output_array(padded_array.shape)
    for ix, iy in _padded_array_index(padded_array.shape, structuring_element.centre.x):
        if padded_array[ix + structuring_element.centre.x, iy + structuring_element.centre.y] == KERNEL_FILL_VALUE:
            output_array[ix:ix + structuring_element.width(), iy:iy + structuring_element.height()] |= \
                structuring_element.kernel

    return image_array.remove_pad(output_array, structuring_element.centre.x)


def _assert_structuring_element_smaller_than_or_equal_to_array(array: np.ndarray,
                                                               structuring_element: StructuringElement):
    assert array.shape[0] >= structuring_element.kernel.shape[0] \
           and array.shape[1] >= structuring_element.kernel.shape[1]


def _kernel_is_subset_of_array_segment(kernel: np.ndarray, array_segment: np.ndarray):
    return np.array_equal(kernel, array_segment & kernel)


def _initialise_output_array(array_shape: tuple):
    return np.zeros(array_shape, dtype=OUTPUT_ARRAY_DTYPE)


def _padded_array_index(padded_array_shape: tuple, pad: int):
    return np.ndindex(padded_array_shape[0] - 2*pad, padded_array_shape[1] - 2*pad)

