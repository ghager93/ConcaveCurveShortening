import numpy as np
from typing import Tuple, Set

from bin.morphology import skeleton_ops
from bin.morphology.util import neighbour_array


class SkeletonGraph:
    def __init__(self, skeleton: np.ndarray, root: Tuple):
        self.skeleton = skeleton
        self.root = root
        self.points = skeleton_ops.node_list(skeleton)
        self.branch_points = set(skeleton_ops.branch_points(skeleton))
        self.end_points = set(skeleton_ops.end_points(skeleton))
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = list()
        for point in self.points:
            if point in self.branch_points:
                graph.append(self._build_node_branch_point(point))
            elif point in self.end_points:
                graph.append(self._build_node_end_point(point))
            else:
                graph.append(self._build_node_normal_point(point))

    def _build_node_branch_point(self, point: Tuple):
        pass

    def _build_node_end_point(self, point: Tuple):


    def _build_node_normal_point(self, point: Tuple):

    def _node_edges_branch_point(self, point: Tuple):

    def _node_edges_end_point(self, point: Tuple):

    def _node_edges_normal_point(self, point: Tuple):


class SkeletonNode:
    def __init__(self, point: Tuple, edges: Set):
        self.point = point
        self.edges = edges

class SkeletonNodeBranchPoint(SkeletonNode):
    def __init__(self, point: Tuple):
        super().__init__(point, self._edges(point))

    def _edges(self, point):
        return None


class SkeletonNodeEndPoint(SkeletonNode):
    def __init__(self, point: Tuple, edges: Set, neighbourhood_binary: int):
        super().__init__(point, self._edges(point, neighbourhood_binary))

    @staticmethod
    def _edges(point, neighbourhood_binary):
        if neighbour_array.number_of_side_neighbours(neighbourhood_binary) == 1

class SkeletonNodeNormalPoint(SkeletonNode):



