import numpy as np

from . import skeleton_ops
from . import transforms
from . import bones

from bin.util.vector2d import Vector2D


class SkeletonGraph:
    def __init__(self, image: np.ndarray):
        self.image = image
        self.skeleton = transforms.skeleton_transform(image)
        self.nodes = skeleton_ops.nodes(self.skeleton)
        self.edges = skeleton_ops.distinct_edges(self.skeleton)
        self.ends = skeleton_ops.end_points(self.skeleton)
        self.branches = skeleton_ops.branch_points(self.skeleton)
        self.root = skeleton_ops.image_root(self.image, self.skeleton)
        self.bone_graph = bones.BoneGraph(self.vertices(), bones.bones(self))
        self.root_distance_map = self._root_distance_map()

    def vertices(self):
        return self.ends | self.branches | {self.root}

    def vertices_array(self):
        out = np.zeros(self.skeleton.shape, int)
        out[tuple([x for x in zip(*self.vertices())])] = 1
        return out

    def distance_to_root(self, point: Vector2D):
        assert self.skeleton[point] == 1

        return self.root_distance_map[point]

    def _root_distance_map(self):
        d_map = dict()
        stack = [(self.root, 0)]

        def unvisited_neighbours(node: Vector2D):
            return [node + (x, y) for x in range(-1, 2) for y in range(-1, 2) if
                    (x, y) != (0, 0) and legal_unvisited_neighbour(node + (x, y))]

        def legal_unvisited_neighbour(n: Vector2D):
            return 0 <= n.x < self.skeleton.shape[0] \
                   and 0 <= n.y < self.skeleton.shape[1] \
                   and self.skeleton[n] \
                   and n not in d_map.keys()

        while stack:
            curr, d = stack.pop()
            d_map[curr] = d
            stack += [(neighbour, d+1) for neighbour in unvisited_neighbours(curr)]

        return d_map


