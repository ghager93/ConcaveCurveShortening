import numpy as np
from PIL import Image
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

from bin.util.vector2d import Vector2D


CLOSE_METHOD_KEY_PRESS = 'key_press'
CLOSE_METHOD_TIMER = 'timer'
CLOSE_TIME_DEFAULT = 1

PADDED_ARRAY_DTYPE = 'int32'


def convert_image_to_array(image: Image.Image):
    return np.array(image)


def convert_image_to_binary_array(image: Image.Image):
    return np.array(image.convert('1'))


def convert_to_image(array: np.ndarray):
    return Image.fromarray(array > 0)


def convert_to_points_list(array: np.ndarray):
    csr = csr_matrix(array)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x + 1]]]


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


def show(array: np.ndarray, close_method: str=CLOSE_METHOD_KEY_PRESS, close_time: int=CLOSE_TIME_DEFAULT):
    if close_method == CLOSE_METHOD_KEY_PRESS:
        _show_until_key_press(array)
    if close_method == CLOSE_METHOD_TIMER:
        _show_for_n_seconds(array, close_time)


def _show_for_n_seconds(array: np.ndarray, n: int):
    plt.imshow(array)
    plt.show(block=False)
    plt.pause(n)
    plt.close()


def _show_until_key_press(array: np.ndarray):
    plt.imshow(array)
    plt.show(block=False)
    plt.waitforbuttonpress(0)
    plt.close()