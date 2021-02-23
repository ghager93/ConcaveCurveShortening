import numpy as np
from PIL import Image

from bin import adj_flood_fill as flood_fill

CLOSE_METHOD_KEY_PRESS = 'key_press'

PADDED_ARRAY_DTYPE = 'int32'


def convert_image_to_array(image: Image.Image):
    return np.array(image).astype(int)


def convert_image_to_binary_array(image: Image.Image):
    return np.array(image.convert('1'))


def convert_to_image(array: np.ndarray):
    return Image.fromarray(array > 0)


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
    # array[array == 1] = 2
    # array[array == 0] = 1
    # array[array > 1] = 0
    # return array
    return np.where(array == 0, 1, 0)


def flatten(array: np.ndarray):
    array[array > 1] = 1
    return array


def find_polygons(array: np.ndarray):
    return flood_fill.get_polygons(array)