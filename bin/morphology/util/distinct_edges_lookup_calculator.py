import numpy as np

from . import neighbour_array
from bin.util.base_dir import base_dir

UPPER_LIMIT = 256


def load_lut(path: str = base_dir + '/lib/lookup/distinct_edges_lut.txt'):
    with open(path, 'r') as f:
        return [int(x) for x in f.readlines()]


def create_lut(path: str = base_dir + '/lib/lookup/distinct_edges_lut.txt'):
    with open(path, 'w') as f:
        f.write('\n'.join([str(int(x)) for x in _build_array()]))


def _build_array():
    return [_distinct_edges(n) for n in range(UPPER_LIMIT)]


def _distinct_edges(b: int):
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

    edge_masks = [0b00000001,
                  0b00000100,
                  0b00010000,
                  0b01000000,
                  0b00000010,
                  0b00001000,
                  0b00100000,
                  0b10000000]

    b_masks = [0b01111100,
               0b11110001,
               0b11000111,
               0b00011111,
               0b11111000,
               0b11100011,
               0b10001111,
               0b00111110]

    while b:
        if b & edge_masks[i]:
            edges |= edge_masks[i]
            b &= b_masks[i]

        i += 1

    return edges
