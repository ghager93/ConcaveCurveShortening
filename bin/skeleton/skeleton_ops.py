import numpy as np
from scipy.spatial import KDTree

from bin.utils.image import _array_to_points_list_wrapper
from bin.utils.vector2d import Vector2D
from bin.morphology.utils import neighbour_array, branch_point_lookup_calculator, distinct_edges_lookup_calculator
from bin.morphology.transforms import distance_transform, neighbours_transform


def branch_points(skeleton: np.ndarray):
    sk_neighbours_transform = neighbours_transform(skeleton)
    branch_lut = branch_point_lookup_calculator.load_lut()

    def is_branch_point(ix, iy):
        return skeleton[ix, iy] \
               and branch_lut[sk_neighbours_transform[ix, iy]]

    return {Vector2D(ix, iy) for ix, iy in np.ndindex(skeleton.shape) if is_branch_point(ix, iy)}


def end_points(skeleton: np.ndarray):
    padded_skeleton = np.pad(skeleton, 1)

    def is_end_point(ix, iy):
        return padded_skeleton[ix + 1, iy + 1] \
            and neighbour_array.number_of_connected_neighbours(padded_skeleton[ix:ix + 3, iy:iy + 3]) == 1

    return {Vector2D(ix, iy) for ix, iy in np.ndindex(skeleton.shape) if is_end_point(ix, iy)}


def image_root(image: np.ndarray, skeleton: np.ndarray):
    argmax = _argmax_random_tiebreak(distance_transform(image) * skeleton)

    return Vector2D(argmax // image.shape[1], argmax % image.shape[1])


def _argmax_random_tiebreak(array: np.ndarray):
    return np.random.choice(np.flatnonzero(array == array.max()))


def nodes(skeleton: np.ndarray):
    return {Vector2D(n[0], n[1]) for n in np.argwhere(skeleton)}


def distinct_edges(skeleton: np.ndarray):
    sk_neighbours_transform = neighbours_transform(skeleton, hang=False)
    distinct_edges_lut = distinct_edges_lookup_calculator.load_lut()

    return np.take(distinct_edges_lut, sk_neighbours_transform)


def skeleton_to_root_distance_map(root: Vector2D, skeleton: np.ndarray):
    d_map = dict()
    stack = [(root, 0)]

    def unvisited_neighbours(node: Vector2D):
        return [node + (x, y) for x in range(-1, 2) for y in range(-1, 2) if
                (x, y) != (0, 0) and legal_unvisited_neighbour(node + (x, y))]

    def legal_unvisited_neighbour(n: Vector2D):
        return 0 <= n.x < skeleton.shape[0] \
               and 0 <= n.y < skeleton.shape[1] \
               and skeleton[n] \
               and n not in d_map.keys()

    while stack:
        curr, d = stack.pop()
        d_map[curr] = d
        stack += [(neighbour, d + 1) for neighbour in unvisited_neighbours(curr)]

    return d_map


@_array_to_points_list_wrapper
def skeleton_tree_query(image, skeleton):
    return KDTree(skeleton).query(image)