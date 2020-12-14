import numpy as np

from bin.morphology import skeleton_ops
from bin.morphology.util import neighbour_array


def neighbour_matrix(matrix: np.ndarray):
    padded_matrix = np.pad(matrix, 1)



def edge_matrix(skeleton: np.ndarray):
    edge_m = np.zeros(skeleton.shape, dtype=int)
    for ix, iy in np.ndindex(skeleton.shape):
        if skeleton[ix, iy]:
            edge_m[ix, iy] = neighbour_array.distinct_edges(skel)