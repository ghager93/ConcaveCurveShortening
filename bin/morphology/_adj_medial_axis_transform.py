import numpy as np

import bin.utils.imshow
from bin import adj_image_array
from bin.morphology import _distance_transform, _adj_sharpness_transform
from bin.morphology.utils import neighbour_array


def medial_axis_transform(array: np.ndarray):
    mat = np.pad(np.copy(array), 1)
    ranked = ranking(mat)
    deletion_table = _get_deletion_table()

    for p in ranked:
        if mat[p]:
            neighbourhood_binary = neighbour_array.array_to_binary(mat[p[0] - 1:p[0] + 2, p[1] - 1:p[1] + 2])
            mat[p] = not deletion_table[neighbourhood_binary]

    return mat[1:-1, 1:-1]


def _get_deletion_table():
    deletion_table_filepath = 'lib/lookup/mat_deletion_lookup.txt'
    with open(deletion_table_filepath) as f:
        return [int(x) for x in f.readlines()]


def ranking(array: np.ndarray):
    flat_rank = np.lexsort((_adj_sharpness_transform.sharpness_transform(array).flatten(),
                            _distance_transform.distance_transform(array).flatten()))
    return [(x // array.shape[1], x % array.shape[1]) for x in flat_rank]


def _test_connection_criteria():
    for n in range(256):
        if _can_delete(n):
            bin.utils.imshow.show(neighbour_array.binary_to_array(n))


def _create_delete_lookup_array():
    return [_can_delete(n) for n in range(256)]


def _can_delete(n: int):
    return _number_of_neighbours(n) >= 3 and _would_not_break_connection(n)


def _number_of_neighbours(n: int):
    return _number_of_bits_high(n)


def _would_not_break_connection(n: int):
    if _number_of_side_neighbours(n) == 0:
        return False
    if _number_of_side_neighbours(n) == 1:
        return _number_of_neighbours(n) == 3 and \
               _count_pattern_occurrence(_add_looped_bit(n), 0b111, 0b111) > 0
    if _number_of_side_neighbours(n) == 2:
        return _would_not_break_connection_two_side_neighbours(n)
    if _number_of_side_neighbours(n) > 2:
        return True
    return False


def _would_not_break_connection_two_side_neighbours(n: int):
    if _number_of_neighbours(n) > 5:
        return False
    if _number_of_neighbours(n) == 5:
        return _five_neighbour_two_side(n)
    if _number_of_neighbours(n) == 4:
        return _four_neighbour_two_side(n)
    if _number_of_neighbours(n) == 3:
        return _three_neighbour_two_side(n)
    return False


def _five_neighbour_two_side(n: int):
    return n == 0b00011111 or n == 0b00111110 or n == 0b01111100 or n == 0b11111000 or n == 0b11110001 or \
           n == 0b11100011 or n == 0b11000111 or n == 0b11000111 or n == 0b10001111


def _four_neighbour_two_side(n: int):
    return n == 0b00001111 or n == 0b00011110 or n == 0b00111100 or n == 0b01111000 or n == 0b11110000 or \
           n == 0b11100001 or n == 0b11000011 or n == 0b10000111 or n == 0b00010111 or n == 0b01011100 or \
           n == 0b01110001 or n == 0b11000101 or n == 0b01000111 or n == 0b00011101 or n == 0b01110100 or \
           n == 0b11010001


def _three_neighbour_two_side(n: int):
    return n == 0b00000111 or n == 0b00011100 or n == 0b01110000 or n == 0b11000001 or n == 0b00001101 or \
           n == 0b00110100 or n == 0b11010000 or n == 0b01000011 or n == 0b00010110 or n == 0b01011000 or \
           n == 0b01100001


def _number_of_side_neighbours(n: int):
    side_neighbour_mask = 0b01010101

    return _number_of_bits_high(n & side_neighbour_mask)


def _count_pattern_occurrence(n: int, pattern: int, mask: int):
    mask_length = (mask + 1) // 2 - 1
    looped_n = _add_looped_bits(n, mask_length - 1)
    pattern_sum = 0
    limit = 1 << 9

    for i in range(limit):
        if mask & looped_n == pattern:
            pattern_sum += 1
        mask <<= 1
        pattern <<= 1

    return pattern_sum


def _number_of_bits_high(n: int):
    return bin(n).count('1')


def _add_looped_bit(n: int):
    return _add_looped_bits(n, 1)


def _add_looped_bits(n: int, number_bits: int):
    return n + ((n % (1 << number_bits)) << 8)
