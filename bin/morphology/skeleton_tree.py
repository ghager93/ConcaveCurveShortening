import numpy as np
from scipy.spatial import KDTree

from .skeleton_mapping import _array_to_points_list_wrapper


class SkeletonMap:
    @_array_to_points_list_wrapper
    def __init__(self, skeleton, image):
        super().__init__(skeleton)
        self.distances, self.map = self.query(image)

