import numpy as np

from . import skeleton_ops
from bin.util.vector2d import Vector2D

from .skeleton_graph import SkeletonGraph
from .util.neighbour_array import neighbour_coordinates


def bones(skeleton: SkeletonGraph):
    visited = set()
    bones = list()

    for joint in skeleton.joints():
        unvisited_neighbours = {joint + n for n in neighbour_coordinates(skeleton.edges[joint])} - visited
        for node in unvisited_neighbours:
            bone = [joint]
            while node not in skeleton.joints():
                bone.append(node)
                visited.add(node)
                node = ({node + n for n in neighbour_coordinates(skeleton.edges[node])} - (visited | {joint})).pop()
            bone.append(node)
            bones.append(bone)

    return bones
