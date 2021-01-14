import numpy as np
from scipy.spatial import KDTree

from .skeleton_mapping import _array_to_points_list_wrapper


@_array_to_points_list_wrapper
def skeleton_tree_query(image, skeleton):
    return KDTree(skeleton).query(image)


