import numpy as np

from scipy.spatial import KDTree

from util import get_test_objects

from morphology import transforms
from morphology import skeleton_graph

from image_array import convert_to_points_list, show


image_array = get_test_objects.get_test_image_array('test2.bmp')

skeleton = skeleton_graph.SkeletonGraph(image_array)

skeleton_points = convert_to_points_list(skeleton.skeleton)
image_points = convert_to_points_list(image_array)

tree = KDTree(skeleton_points)
distances, pairs = tree.query(image_points)

distance_map = np.zeros(image_array.shape)
distance_map[tuple(p for p in zip(*image_points))] = distances

root_map = np.zeros(image_array.shape)
root_map[tuple(p for p in zip(*image_points))] = [skeleton.distance_to_root(skeleton_points[q]) for q in pairs]

show(distance_map + root_map)
