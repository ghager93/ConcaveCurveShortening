import numpy as np

from bin import image_array
from bin.util import neighbour_array


def _test_connection_criteria():
    for n in range(256):
        if _can_delete(n):
            image_array.show(neighbour_array.binary_to_array(n))


def _can_delete(n: int):
    return _more_than_two_neighbours(n) & _would_not_break_connection(n)


def _more_than_two_neighbours(n: int):
    return _number_of_bits_high(n) > 2


def _number_of_bits_high(n: int):
    return bin(n).count('1')


def _would_not_break_connection(n: int):
    return _count_100_patterns(n) <= 1


def _count_100_patterns(n: int):
    circular_n = _add_zeroth_bit_as_ninth_bit(n)
    pattern_sum = 0

    mask = 0b111
    pattern = 0b100

    for i in range(6):
        if mask & circular_n == pattern:
            pattern_sum += 1
        mask <<= 1
        pattern <<= 1

    return pattern_sum


def _add_zeroth_bit_as_ninth_bit(n: int):
    return n + ((n % 2) << 8)
