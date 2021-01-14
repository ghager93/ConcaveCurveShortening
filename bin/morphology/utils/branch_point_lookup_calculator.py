import numpy as np

from . import neighbour_array
from bin.utils.base_dir import base_dir


UPPER_LIMIT = 256


def load_lut(path: str = base_dir + '/lib/lookup/branch_point_lut.txt'):
    with open(path, 'r') as f:
        return [int(x) for x in f.readlines()]


def create_lut(path: str = base_dir + '/lib/lookup/branch_point_lut.txt'):
    with open(path, 'w') as f:
        f.write('\n'.join([str(int(x)) for x in _build_array()]))


def _build_array():
    return [_is_branch_point(n) for n in range(UPPER_LIMIT)]


def _is_branch_point(n: int):
    return neighbour_array.number_of_connected_neighbours(n) > 2 or neighbour_array.is_top_left_corner_of_square(n)