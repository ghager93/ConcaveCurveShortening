from typing import Collection

from bin.utils.vector2d import Vector2D

from .utils.neighbour_array import neighbour_coordinates


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

    def distance_between(self, p1, p2):
        assert p1 in self and p2 in self

        return abs(self.index(p1) - self.index(p2))


class BoneGraph(dict):
    def __init__(self, vertices: Collection[Vector2D], bones: Collection[Bone]):
        super().__init__()
        self.vertices = vertices
        self.bones = bones
        self.distance_dictionary = dict()
        self._build_graph()

    def _build_graph(self):
        for vertex in self.vertices:
            self[vertex] = set()

        for bone in self.bones:
            self[bone.start()].add(bone.end())
            self[bone.end()].add(bone.start())


def bones(skeleton_graph):
    visited = set()
    bones = set()

    # for vertex in skeleton_graph.vertices():
    #     unvisited_vertex_neighbours = {vertex + n for n in
    #                                    neighbour_coordinates(skeleton_graph.edges[vertex])} - visited
    #     for node in unvisited_vertex_neighbours:
    #         bone = [vertex]
    #         while node not in skeleton_graph.vertices():
    #             bone.append(node)
    #             visited.add(node)
    #             unvisited_node_neighbours = {node + n for n in
    #                                          neighbour_coordinates(skeleton_graph.edges[node])} - visited
    #             if len(bone) <= 2:
    #                 unvisited_node_neighbours -= {vertex}
    #             node = unvisited_node_neighbours.pop()
    #         bone.append(node)
    #         bones.add(Bone(bone))

    for vertex in skeleton_graph.vertices():
        vertex_edges = {vertex + p for p in neighbour_coordinates(skeleton_graph.edges[vertex])}
        for edge in vertex_edges:
            if edge not in visited:
                bone = [vertex]
                while edge not in skeleton_graph.vertices():
                    bone.append(edge)
                    visited.add(edge)
                    edge, = {edge + n for n in neighbour_coordinates(skeleton_graph.edges[edge])} - {bone[-2]}
                bone.append(edge)
                bones.add(Bone(bone))

    return bones

