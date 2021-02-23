import numpy as np
import math

from bin.morphology.utils import neighbour_array
from bin.edge_loop import EdgeLoop


def _curvature0(points):
    points = np.array(points)
    previous_neighbours = neighbour_array.relative_neighbour_binary(points, np.roll(points, 1, 0))
    next_neighbours = neighbour_array.relative_neighbour_binary(points, np.roll(points, -1, 0))

    return ((next_neighbours - previous_neighbours) % 8) * np.pi / 4


def curvature_n(points, n):
    c0 = _curvature0(points)
    return sum([math.comb(2*n, i) * np.roll(c0, 2*n - i) for i in range(2*n+1)]) / (4**n)
