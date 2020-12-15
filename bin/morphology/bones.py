import numpy as np

from . import skeleton_ops
from bin.util.vector2d import Vector2D

from .skeleton_graph import SkeletonGraph
from .util.neighbour_array import neighbour_coordinates


class Bone(tuple):
    def start(self):
        return self[0]

    def end(self):
        return self[-1]

    def __eq__(self, other):
        return ((self.start() == other.start()) & (self.end() == other.end()))\
               | ((self.start() == other.end()) & (self.end() == other.start()))


def bones(skeleton_graph: SkeletonGraph):
    visited = set()
    bones = list()

    for joint in skeleton_graph.joints():
        unvisited_neighbours = {joint + n for n in neighbour_coordinates(skeleton_graph.edges[joint])} - visited
        for node in unvisited_neighbours:
            bone = Bone([joint])
            while node not in skeleton_graph.joints():
                bone.append(node)
                visited.add(node)
                node = ({node + n for n in neighbour_coordinates(skeleton_graph.edges[node])}
                        - (visited | {joint})).pop()
            bone.append(node)
            if bone not in bones:
                bones.append(bone)

    return bones
