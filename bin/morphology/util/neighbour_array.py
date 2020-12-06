import numpy as np

from bin.image_array import pad_by_zeroes


def binary_to_array(n: int):
    arr = np.zeros((3, 3), dtype='bool')
    arr[0, 0] = n & 0b10000000
    arr[0, 1] = n & 0b00000001
    arr[0, 2] = n & 0b00000010
    arr[1, 0] = n & 0b01000000
    arr[1, 1] = 0
    arr[1, 2] = n & 0b00000100
    arr[2, 0] = n & 0b00100000
    arr[2, 1] = n & 0b00010000
    arr[2, 2] = n & 0b00001000

    return arr.astype(int)


def array_to_binary(array: np.ndarray):
    assert array.shape == (3, 3)

    return array[0, 1] + (array[0, 2] << 1) + (array[1, 2] << 2) + (array[2, 2] << 3) + \
           (array[2, 1] << 4) + (array[2, 0] << 5) + (array[1, 0] << 6) + (array[0, 0] << 7)


def get_neighbour_array(array: np.ndarray):
    shifted_neighbour_arrays = get_shifted_neighbour_arrays(array)
    neighbour_array = np.zeros(array.shape, dtype='int')
    neighbour_bit_shifts = [7, 0, 1, 6, 2, 5, 4, 3]
    for i, arr in enumerate(shifted_neighbour_arrays):
        neighbour_array |= arr << neighbour_bit_shifts[i]

    return neighbour_array


def get_shifted_neighbour_arrays(array: np.ndarray):
    padded_array = pad_by_zeroes(array)
    return [padded_array[x:padded_array.shape[0] + x-2, y:padded_array.shape[1] + y-2]
            for x in range(3) for y in range(3)
            if x != 1 or y != 1]


def number_of_neighbours(e):
    if type(e) is np.ndarray:
        n = array_to_binary(e)
    else:
        n = e

    return _number_of_bits_high(n)


def _number_of_bits_high(n: int):
    return bin(n).count('1')


def number_of_connected_neighbours(e):
    if type(e) is np.ndarray:
        n = array_to_binary(e)
    else:
        n = e

    return _number_of_01_patterns_in_ordered_neighbours_set(n)


def _number_of_01_patterns_in_ordered_neighbours_set(n: int):
    mask = 0b11000000
    pattern = 0b01000000
    cnt = 0
    for i in range(7):
        if mask & n == pattern:
            cnt += 1
        mask >>= 1
        pattern >>= 1

    if 0b10000001 & n == 0b10000000:
        cnt += 1

    return cnt

