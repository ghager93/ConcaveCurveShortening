import numpy as np

from bin import image_array
from bin import distance_transform
from bin import cornerness
from bin.util import neighbour_array


def ranking(array: np.ndarray):
    flat_rank = np.lexsort((cornerness.cornerness(array).flatten(),
                            distance_transform.get_distance_transform(array).flatten()))
    image_array.show(flat_rank.reshape(array.shape))
    return [[x // array.shape[0], x % array.shape[0]] for x in flat_rank]


def _test_connection_criteria():
    for n in range(256):
        if _can_delete(n):
            image_array.show(neighbour_array.binary_to_array(n))


def _create_delete_lookup_array():
    return [_can_delete(n) for n in range(256)]


def _can_delete(n: int):
    if _number_of_neighbours(n) < 3:
        return False
    return _would_not_break_connection(n)


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
