import numpy as np

from bin.morphology.util import neighbour_array, branch_point_lookup_calculator
from bin.morphology.transforms import distance_transform


def branch_points(skeleton: np.ndarray):
    padded_skeleton = np.pad(skeleton, 1)

    branch_lut = branch_point_lookup_calculator.load_lut()

    def is_branch_point(ix, iy):
        return padded_skeleton[ix + 1, iy + 1] \
               and branch_lut[neighbour_array.array_to_binary(padded_skeleton[ix:ix + 3, iy:iy + 3])]

    return {(ix, iy) for ix, iy in np.ndindex(skeleton.shape) if is_branch_point(ix, iy)}


def end_points(skeleton: np.ndarray):
    padded_skeleton = np.pad(skeleton, 1)

    def is_end_point(ix, iy):
        return padded_skeleton[ix + 1, iy + 1] \
            and neighbour_array.number_of_connected_neighbours(padded_skeleton[ix:ix + 3, iy:iy + 3]) == 1

    return {(ix, iy) for ix, iy in np.ndindex(skeleton.shape) if is_end_point(ix, iy)}


def image_root(image: np.ndarray, skeleton: np.ndarray):
    argmax = _argmax_random_tiebreak(distance_transform(image) * skeleton)

    return argmax // image.shape[1], argmax % image.shape[1]


def _argmax_random_tiebreak(array: np.ndarray):
    return np.random.choice(np.flatnonzero(array == array.max()))


def node_list(skeleton: np.ndarray):
    return np.argwhere(skeleton).tolist()
