import numpy as np
from scipy.ndimage import morphology as sp_morphology

from bin import image_array as image_array
from bin.morphology.structuring_element import _assert_structuring_element_smaller_than_or_equal_to_array, \
    KERNEL_FILL_VALUE, OUTPUT_ARRAY_DTYPE, get_circular_structuring_element
from bin.morphology.structuring_element import StructuringElement


def binary_opening(array: np.ndarray, structuring_element: StructuringElement = get_circular_structuring_element()):
    return binary_dilation(binary_erosion(array, structuring_element), structuring_element)


def binary_closing(array: np.ndarray, structuring_element: StructuringElement = get_circular_structuring_element()):
    return binary_erosion(binary_dilation(array, structuring_element), structuring_element)


def binary_erosion(array: np.ndarray, structuring_element: StructuringElement = get_circular_structuring_element()):
    return sp_morphology.binary_erosion(array, structuring_element.kernel).astype(int)


def _binary_erosion(array: np.ndarray, structuring_element: StructuringElement):
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


def binary_dilation(array: np.ndarray, structuring_element: StructuringElement = get_circular_structuring_element()):
    return sp_morphology.binary_dilation(array, structuring_element.kernel).astype(int)


def _binary_dilation(array: np.ndarray, structuring_element: StructuringElement):
    _assert_structuring_element_smaller_than_or_equal_to_array(array, structuring_element)
    padded_array = image_array.pad_by_zeroes(array, structuring_element.centre.x)
    output_array = _initialise_output_array(padded_array.shape)
    for ix, iy in _padded_array_index(padded_array.shape, structuring_element.centre.x):
        if padded_array[ix + structuring_element.centre.x, iy + structuring_element.centre.y] == KERNEL_FILL_VALUE:
            output_array[ix:ix + structuring_element.width(), iy:iy + structuring_element.height()] |= \
                structuring_element.kernel

    return image_array.remove_pad(output_array, structuring_element.centre.x)


def _kernel_is_subset_of_array_segment(kernel: np.ndarray, array_segment: np.ndarray):
    return np.array_equal(kernel, array_segment & kernel)


def _initialise_output_array(array_shape: tuple):
    return np.zeros(array_shape, dtype=OUTPUT_ARRAY_DTYPE)


def _padded_array_index(padded_array_shape: tuple, pad: int):
    return np.ndindex(padded_array_shape[0] - 2 * pad, padded_array_shape[1] - 2 * pad)