import numpy as np

from . import skeleton_ops
from bin.util.vector2d import Vector2D

from .skeleton_graph import SkeletonGraph
from .util.neighbour_array import neighbour_coordinates


class Bone(tuple):
    def __eq__(self, other):
        return ((self.start() == other.start()) & (self.end() == other.end()))\
               | ((self.start() == other.end()) & (self.end() == other.start()))

    def __hash__(self):
        hash_ = 0
        if len(self) > 0:
            hash_ += super.__hash__(tuple([self[0]]))
        if len(self) > 1:
            hash_ += super.__hash__(tuple([self[-1]]))
        if len(self) > 2:
            hash_ += super.__hash__(tuple([self[1:-1]]))

        return hash_

    def start(self):
        return self[0]

    def end(self):
        return self[-1]


class JointGraph(dict):
    def __init__(self, joints, bones):
        super().__init__()
        self.joints = joints
        self.bones = bones
        self._build_graph()

    def _build_graph(self):
        for joint in self.joints:
            self[joint] = set()

        for bone in self.bones:
            self[bone.start()].add(bone.end())
            self[bone.end()].add(bone.start())


def bones(skeleton_graph: SkeletonGraph):
    visited = set()
    bones = set()

    for joint in skeleton_graph.joints():
        unvisited_neighbours = {joint + n for n in neighbour_coordinates(skeleton_graph.edges[joint])} - visited
        for node in unvisited_neighbours:
            bone = [joint]
            while node not in skeleton_graph.joints():
                bone.append(node)
                visited.add(node)
                node = ({node + n for n in neighbour_coordinates(skeleton_graph.edges[node])}
                        - (visited | {joint})).pop()
            bone.append(node)
            bones.add(Bone(bone))

    return bones
