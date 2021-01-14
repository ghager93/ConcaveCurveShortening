import numpy as np

from bin import image_array as image_array
from bin.morphology._operations import binary_erosion, binary_opening
from bin.morphology.structuring_element import StructuringElement
from bin.morphology.structuring_element import _assert_structuring_element_smaller_than_or_equal_to_array
from lib.lookup.zhan_suen_neighbour_lookup import FIRST_ITERATION, BOTH_ITERATIONS, SECOND_ITERATION, NEIGHBOUR_LOOKUP

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


def zhan_suen(array: np.ndarray):
    out = np.copy(array)
    for i in range(MAX_ZHAN_SUEN_ITERATIONS):
        criteria_mask = _zs_get_criteria_mask(out)
        if not (any(out[criteria_mask == FIRST_ITERATION])
                | any(out[criteria_mask == SECOND_ITERATION])
                | any(out[criteria_mask == BOTH_ITERATIONS])):
            break
        out[criteria_mask == FIRST_ITERATION] = 0
        out[criteria_mask == BOTH_ITERATIONS] = 0

        criteria_mask = _zs_get_criteria_mask(out)
        if not (any(out[criteria_mask == FIRST_ITERATION])
                | any(out[criteria_mask == SECOND_ITERATION])
                | any(out[criteria_mask == BOTH_ITERATIONS])):
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