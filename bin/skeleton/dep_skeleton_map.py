import numpy as np

from scipy.spatial import KDTree

from .adj_skeleton_graph import SkeletonGraph

from ..utils.image import convert_to_points_list


def skeleton_map(skeleton: SkeletonGraph):
    skeleton_points = convert_to_points_list(skeleton.skeleton)
    image_points = convert_to_points_list(skeleton.image)

    tree = KDTree(skeleton_points)
    distances, pairs = tree.query(image_points)

    distance_map = np.zeros(skeleton.image.shape)
    distance_map[tuple(p for p in zip(*image_points))] = distances

    root_map = np.zeros(skeleton.image.shape)
    root_map[tuple(p for p in zip(*image_points))] = [skeleton.distance_to_root(skeleton_points[q]) for q in pairs]

    return distance_map + root_map

