import numpy as np
from scipy.ndimage import morphology as sp_morphology

import bin.image_array as image_array
from bin.util.vector2d import Vector2D
from lib.lookup.zhan_suen_neighbour_lookup import FIRST_ITERATION, SECOND_ITERATION, BOTH_ITERATIONS
from lib.lookup.zhan_suen_neighbour_lookup import NEIGHBOUR_LOOKUP

KERNEL_FILL_VALUE = 1
OUTPUT_FILL_VALUE = 1

KERNEL_ARRAY_DTYPE = 'int32'
OUTPUT_ARRAY_DTYPE = 'int32'

MAX_LANTUEJOULS_ITERATIONS = 500
MAX_ZHAN_SUEN_ITERATIONS = 500

ZHAN_SUEN_POSITION_SHIFTS = {
    0: (1, 0),
    1: (2, 0),
    2: (2, 1),
    3: (2, 2),
    4: (1, 2),
    5: (0, 2),
    6: (0, 1),
    7: (0, 0)
}

ZS_P2 = 0
ZS_P3 = 1
ZS_P4 = 2
ZS_P5 = 3
ZS_P6 = 4
ZS_P7 = 5
ZS_P8 = 6
ZS_P9 = 7
ZHAN_SUEN_NEIGHBOURHOOD_SIZE = 3


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


def binary_dilation(array: np.ndarray, structuring_element: StructuringElement):
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


def binary_skeletonisation(array: np.ndarray, structuring_element: StructuringElement):
    _assert_structuring_element_smaller_than_or_equal_to_array(array, structuring_element)
    return _lantuejouls2(array, structuring_element)


def _lantuejouls(array: np.ndarray, structuring_element: StructuringElement):
    erosions = _get_erosions_up_to_k_times(array, structuring_element, 20)
    return [_get_skeleton_subset(erosions[k], structuring_element) for k in range(20)]


def _lantuejouls2(array: np.ndarray, structuring_element: StructuringElement):
    skeleton_subsets = list()

    skeleton_subset = array
    for i in range(MAX_LANTUEJOULS_ITERATIONS):
        # new_skeleton_subset = _get_skeleton_subset(array, structuring_element)
        # if np.array_equal(new_skeleton_subset, skeleton_subset):
        #     break
        # skeleton_subset = new_skeleton_subset
        # skeleton_subsets.append(skeleton_subset)
        # array = binary_erosion(array, structuring_element)

        skeleton_subsets.append(_get_skeleton_subset(array, structuring_element))
        new_array = binary_erosion(array, structuring_element)
        if np.array_equal(new_array, array):
            break
        array = new_array

    return skeleton_subsets


def _get_skeleton_subset(array_erosion: np.ndarray, structuring_element: StructuringElement):
    return array_erosion - binary_opening(array_erosion, structuring_element)


def _erode_k_times(array: np.ndarray, structuring_element: StructuringElement, k: int):
    for i in range(k):
        array = binary_erosion(array, structuring_element)

    return array


def _get_erosions_up_to_k_times(array: np.ndarray, structuring_element: StructuringElement, k: int):
    erosions = list()
    for i in range(k):
        array = binary_erosion(array, structuring_element)
        erosions.append(array)

    return erosions


def _assert_structuring_element_smaller_than_or_equal_to_array(array: np.ndarray,
                                                               structuring_element: StructuringElement):
    assert array.shape[0] >= structuring_element.kernel.shape[0] \
           and array.shape[1] >= structuring_element.kernel.shape[1]


def zhan_suen(array: np.ndarray):
    out = np.copy(array)
    for i in range(MAX_ZHAN_SUEN_ITERATIONS):
        criteria_mask = _zs_get_criteria_mask(out)
        if not (any(out[criteria_mask == FIRST_ITERATION]) | any(out[criteria_mask == BOTH_ITERATIONS])):
            break
        out[criteria_mask == FIRST_ITERATION] = 0
        out[criteria_mask == BOTH_ITERATIONS] = 0

        criteria_mask = _zs_get_criteria_mask(out)
        if not (any(out[criteria_mask == SECOND_ITERATION]) | any(out[criteria_mask == BOTH_ITERATIONS])):
            break
        out[criteria_mask == SECOND_ITERATION] = 0
        out[criteria_mask == BOTH_ITERATIONS] = 0

    return out


def _zs_get_criteria_mask(array: np.ndarray):
    neighbour_array = _zs_calculate_neighbour_array(array)
    array_flat = np.ndarray.flatten(neighbour_array)
    return np.reshape([NEIGHBOUR_LOOKUP[x] for x in array_flat], neighbour_array.shape)


def _zs_calculate_neighbour_array(array: np.ndarray):
    padded_array = image_array.pad_by_zeroes(array)
    return _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P2]) | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P3]) << 1 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P4]) << 2 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P5]) << 3 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P6]) << 4 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P7]) << 5 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P8]) << 6 | \
           _zs_array_shift(padded_array, ZHAN_SUEN_POSITION_SHIFTS[ZS_P9]) << 7


def _zs_array_shift(array: np.ndarray, shift: tuple):
    return array[shift[1]:(array.shape[0]+shift[1]-2), shift[0]:(array.shape[1]+shift[0] - 2)]
