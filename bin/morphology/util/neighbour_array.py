import numpy as np
from functools import wraps

from bin.image_array import pad_by_zeroes


def binary_to_array(b: int):
    arr = np.zeros((3, 3), dtype='bool')
    arr[0, 0] = b & 0b10000000
    arr[0, 1] = b & 0b00000001
    arr[0, 2] = b & 0b00000010
    arr[1, 0] = b & 0b01000000
    arr[1, 1] = 0
    arr[1, 2] = b & 0b00000100
    arr[2, 0] = b & 0b00100000
    arr[2, 1] = b & 0b00010000
    arr[2, 2] = b & 0b00001000

    return arr.astype(int)


def array_to_binary(array: np.ndarray):
    assert array.shape == (3, 3)

    return array[0, 1] + (array[0, 2] << 1) + (array[1, 2] << 2) + (array[2, 2] << 3) \
           + (array[2, 1] << 4) + (array[2, 0] << 5) + (array[1, 0] << 6) + (array[0, 0] << 7)


def second_neighbours_array_to_binary(arr: np.ndarray):
    assert arr.shape == (5, 5)

    mask = np.array([[2 ** 15, 1, 2, 4, 8],
                     [2 ** 14, 0, 0, 0, 16],
                     [2 ** 13, 0, 0, 0, 32],
                     [2 ** 12, 0, 0, 0, 64],
                     [2 ** 11, 1024, 512, 256, 128]])

    return np.sum(mask * arr)


def get_neighbour_array(array: np.ndarray):
    shifted_neighbour_arrays = get_shifted_neighbour_arrays(array)
    neighbour_array = np.zeros(array.shape, dtype='int')
    neighbour_bit_shifts = [7, 0, 1, 6, 2, 5, 4, 3]
    for i, arr in enumerate(shifted_neighbour_arrays):
        neighbour_array |= arr << neighbour_bit_shifts[i]

    return neighbour_array


def get_shifted_neighbour_arrays(array: np.ndarray):
    padded_array = pad_by_zeroes(array)
    return [padded_array[x:padded_array.shape[0] + x - 2, y:padded_array.shape[1] + y - 2]
            for x in range(3) for y in range(3)
            if x != 1 or y != 1]


def array_to_binary_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = [array_to_binary(a) if type(a) is np.ndarray else a for a in args]
        kwargs = {kw: (array_to_binary(a) if type(a) is np.ndarray else a) for (kw, a) in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper


@array_to_binary_wrapper
def number_of_neighbours(n):
    return _number_of_bits_high(n)


def number_of_second_neighbours(arr: np.ndarray):
    assert arr.shape == (5, 5)

    mask = np.array([[1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1]])

    return np.count_nonzero(mask & arr)


def _number_of_bits_high(b: int):
    return bin(b).count('1')


@array_to_binary_wrapper
def number_of_connected_neighbours(b):
    return _number_of_01_patterns_in_ordered_neighbours_set(b)


@array_to_binary_wrapper
def number_of_connected_second_neighbours(b):
    return _number_of_01_patterns_in_ordered_second_neighbours_set(b)


def _number_of_01_patterns_in_ordered_neighbours_set(b: int):
    mask = 0b11000000
    pattern = 0b01000000
    cnt = 0
    for i in range(7):
        if mask & b == pattern:
            cnt += 1
        mask >>= 1
        pattern >>= 1

    if 0b10000001 & b == 0b10000000:
        cnt += 1

    return cnt


def _number_of_01_patterns_in_ordered_second_neighbours_set(b):
    mask = 0b1100000000000000
    pattern = 0b0100000000000000
    cnt = 0
    for i in range(15):
        if mask & b == pattern:
            cnt += 1
        mask >>= 1
        pattern >>= 1

    if 0b1000000000000001 & b == 0b1000000000000000:
        cnt += 1

    return cnt


@array_to_binary_wrapper
def is_top_left_corner_of_square(b):
    mask = 0b00011100
    return mask & b == mask


@array_to_binary_wrapper
def number_of_side_neighbours(b):
    mask = 0b01010101
    return bin(mask & b).count('1')


@array_to_binary_wrapper
def number_of_diagonal_neighbours(b):
    mask = 0b10101010
    return bin(mask & b).count('1')


@array_to_binary_wrapper
def distinct_edges(b):
    edges = 0
    i = 0

    if b & 0b00000111 == 0b00000111:
        edges |= 0b00000001
        b &= 0b11111000
    if b & 0b11000001 == 0b11000001:
        edges |= 0b10000000
        b &= 0b00111110
    if b & 0b01110000 == 0b01110000:
        edges |= 0b01000000
        b &= 0b10001111

    while b:
        edge_mask = 1 << (i % 7)
        if b & edge_mask:
            edges |= edge_mask
            b &= 0b11111111 - ((1 << (7 + i) % 8)
                               + (1 << (1 + i) % 8)
                               + (1 << i % 8))
        i += 2

    return edges


def distinct_edge_array(array: np.ndarray):
    neighbour_array = get_neighbour_array(array)
    neighbour_array[array == 0] = 0
    return _distinct_edges_vectorised(neighbour_array)


def _distinct_edges_vectorised(b: np.ndarray):
    edges = np.zeros(b.shape, dtype=int)
    i = 0

    def binary_array(n):
        return np.full(b.shape, n)

    square_mask = b & binary_array(0b00000111) == binary_array(0b00000111)
    edges = np.where(square_mask, edges | binary_array(0b00000001), edges)
    b = np.where(square_mask, b & binary_array(0b11111000), b)

    square_mask = b & binary_array(0b11000001) == binary_array(0b11000001)
    edges = np.where(square_mask, edges | binary_array(0b10000000), edges)
    b = np.where(square_mask, b & binary_array(0b00111110), b)

    square_mask = b & binary_array(0b01110000) == binary_array(0b01110000)
    edges = np.where(square_mask, edges | binary_array(0b01000000), edges)
    b = np.where(square_mask, b & binary_array(0b10001111), b)

    edge_mask_cycle = [0b00000001,
                       0b00000100,
                       0b00010000,
                       0b01000000,
                       0b00000010,
                       0b00001000,
                       0b00100000,
                       0b10000000]

    b_mask_cycle = [0b01111100,
                    0b11110001,
                    0b11000111,
                    0b00011111,
                    0b11111000,
                    0b11100011,
                    0b10001111,
                    0b00111110]

    while b.any():
        edge_mask = b & binary_array(edge_mask_cycle[i])
        edges = np.where(edge_mask, edges | edge_mask, edges)
        b = np.where(edge_mask, b & binary_array(b_mask_cycle[i]), b)
        i += 1

    return edges


def _distinct_edges_vectorised2(b: np.ndarray):
    edges = np.zeros(b.shape, dtype=int)
    i = 0

    binary_map = np.array([np.full(b.shape, 1 << i) for i in range(8)])

    def binary_array(n):
        out = np.zeros(b.shape, dtype=int)
        for j in range(8):
            out += (n & (1 << j)) * binary_map[j]
        return out

    square_mask = b & binary_array(0b00000111) == binary_array(0b00000111)
    edges = np.where(square_mask, edges | binary_array(0b00000001), edges)
    b = np.where(square_mask, b & binary_array(0b11111000), b)

    square_mask = b & binary_array(0b11000001) == binary_array(0b11000001)
    edges = np.where(square_mask, edges | binary_array(0b10000000), edges)
    b = np.where(square_mask, b & binary_array(0b00111110), b)

    square_mask = b & binary_array(0b01110000) == binary_array(0b01110000)
    edges = np.where(square_mask, edges | binary_array(0b01000000), edges)
    b = np.where(square_mask, b & binary_array(0b10001111), b)

    while b.any():
        edge_mask = b & binary_array(1 << (i % 7))
        edges = np.where(edge_mask, edges | edge_mask, edges)
        b = np.where(edge_mask,
                     b & binary_array(0b11111111 - ((1 << (7 + i) % 8)
                                                    + (1 << (1 + i) % 8)
                                                    + (1 << i % 8))),
                     b)
        i += 2

    return edges
