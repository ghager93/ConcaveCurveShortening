import numpy as np

import bin.adj_image_array as image_array


FILTER_FILL_VALUE = 1

FILTER_ARRAY_DTYPE = 'int32'
OUTPUT_ARRAY_DTYPE = 'int32'


def apply_to_array(array: np.ndarray, radius: int, inverse_filter=False):
    if inverse_filter:
        array = image_array.invert(array)
    circular_filter = _make_circular_filter(radius)
    padded_array = image_array.pad_by_ones(array, radius)

    return _create_output(padded_array, circular_filter)


def _create_output(array: np.ndarray, filter: np.ndarray):
    output_array = _initialise_output_array(array.shape)
    for ix, iy in np.ndindex(_padded_array_index_shape(array.shape, filter.shape)):
        output_array[ix:ix + filter.shape[0], iy:iy + filter.shape[1]] |= \
            _filter_array_segment(array[ix:ix + filter.shape[0], iy:iy + filter.shape[1]], filter)

    return output_array


def _padded_array_index_shape(array_shape: tuple, pad_shape: tuple):
    return array_shape[0]-pad_shape[0], array_shape[1]-pad_shape[1]


def _filter_array_segment(segment: np.ndarray, filter: np.ndarray):
    assert segment.shape == filter.shape
    return filter if _filter_is_subset_of_array_segment(segment, filter) \
        else np.zeros(filter.shape, dtype=FILTER_ARRAY_DTYPE)


def _filter_is_subset_of_array_segment(segment: np.ndarray, filter: np.ndarray):
    assert segment.shape == filter.shape
    return np.array_equal(filter, segment & filter)


def _make_circular_filter(radius: int):
    filter_shape = _get_filter_shape(radius)
    circular_filter = np.zeros(filter_shape, dtype=FILTER_ARRAY_DTYPE)
    xx, yy = np.mgrid[:filter_shape[0], :filter_shape[1]]
    circular_filter[(xx - radius)**2 + (yy - radius)**2 <= radius**2] = FILTER_FILL_VALUE
    return circular_filter


def _get_filter_shape(radius: int):
    return 2*radius + 1, 2*radius + 1


def _initialise_output_array(array_shape: tuple):
    return np.zeros(array_shape, dtype=OUTPUT_ARRAY_DTYPE)
