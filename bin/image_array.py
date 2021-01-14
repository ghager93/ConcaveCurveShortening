import numpy as np
from PIL import Image
from scipy.sparse import csr_matrix
import matplotlib

from bin import flood_fill as flood_fill

matplotlib.use('TkAgg')

from bin.utils.vector2d import Vector2D


CLOSE_METHOD_KEY_PRESS = 'key_press'
CLOSE_METHOD_TIMER = 'timer'
CLOSE_METHOD_NO_BLOCK = 'no_block'
CLOSE_TIME_DEFAULT = 1

PADDED_ARRAY_DTYPE = 'int32'


def convert_image_to_array(image: Image.Image):
    return np.array(image).astype(int)


def convert_image_to_binary_array(image: Image.Image):
    return np.array(image.convert('1'))


def convert_to_image(array: np.ndarray):
    return Image.fromarray(array > 0)


def convert_to_points_list(array: np.ndarray):
    return _convert_to_points_list2(array)


def _convert_to_points_list(array: np.ndarray):
    csr = csr_matrix(array)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x + 1]]]


def _convert_to_points_list2(array: np.ndarray):
    return [Vector2D(p[0], p[1]) for p in zip(*np.where(array))]


def from_points_list(points, shape):
    arr = np.zeros(shape, int)
    arr[tuple(p for p in zip(*points))] = 1
    return arr


def boolean_sum(array: np.ndarray):
    return np.sum(array > 0)


def boolean_ratio(array1: np.ndarray, array2: np.ndarray):
    assert boolean_sum(array2) > 0
    return boolean_sum(array1) / boolean_sum(array2)


def is_boolean_subset_of(subset_array: np.ndarray, set_array: np.ndarray):
    assert subset_array.shape == set_array.shape
    boolean_subset_array = subset_array > 0
    boolean_set_array = set_array > 0
    boolean_and_array = boolean_subset_array & boolean_set_array
    return boolean_sum(boolean_and_array) > 0 and np.array_equal(boolean_subset_array, boolean_and_array)


def pad_by_zeroes(array: np.ndarray, pad: int = 1):
    padded_array = np.zeros((array.shape[0] + 2*pad, array.shape[1] + 2*pad),
                            dtype=PADDED_ARRAY_DTYPE)
    padded_array[pad:-pad, pad:-pad] = array
    return padded_array


def pad_by_ones(array: np.ndarray, pad: int = 1):
    padded_array = np.ones((array.shape[0] + 2*pad, array.shape[1] + 2*pad),
                           dtype=PADDED_ARRAY_DTYPE)
    padded_array[pad:-pad, pad:-pad] = array
    return padded_array


def remove_pad(array: np.ndarray, pad: int = 1):
    assert array.shape[0] > 2*pad and array.shape[1] > 2*pad
    return array[pad:-pad, pad:-pad]


def invert(array: np.ndarray):
    array[array == 1] = 2
    array[array == 0] = 1
    array[array > 1] = 0
    return array


def flatten(array: np.ndarray):
    array[array > 1] = 1
    return array


def point_map_to_image(point_map: dict, shape):
    image = np.zeros(shape, int)
    image[tuple(p for p in zip(*point_map.keys()))] = list(point_map.values())

    return image


def find_polygons(array: np.ndarray):
    return flood_fill.get_polygons(array)