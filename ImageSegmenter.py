from LoopSegment import LoopSegment, splitSegment
from Vector2D import Vector2D
import numpy as np
from typing import List, Dict
from matrixOps import booleanMatrixToPointList


def segmentMap(map: np.ndarray):
    mapSegment = LoopSegment(Vector2D(0, 0), Vector2D(map.shape[0]-1, map.shape[1]-1),
                             booleanMatrixToPointList(map))
    segments = list()
    stack = list()
    stack.append(mapSegment)
    while stack:
        curr = stack.pop()
        half1, half2 = splitSegment(curr)
        if half1.pointsAreContinuousFunction():
            segments.append(half1)
        else:
            stack.append(half1)

        if half2.pointsAreContinuousFunction():
            segments.append(half2)
        else:
            stack.append(half2)

    return segments


class SegmentGraph:
    def __init__(self, segments: List[LoopSegment]):
        self.segments = segments
        self.adjacencyList = self.makeAdjacencyList()

    def makeAdjacencyList(self):
        adjacencyList = dict()
        for i, segment in enumerate(self.segments):
            adjacencyList[i] = self.findNeighboursOf(segment)

        return adjacencyList

    def findNeighboursOf(self, segment: LoopSegment):
        if not segment.points:
            return set()
        return {j for j, n in enumerate(self.segments) if segment.isNeighbourOf(n)}

    def findGraphLoops(self):
        loops = list()
        visited = set()
        for segment in self.adjacencyList:
            if segment not in visited and self.adjacencyList[segment]:
                loop = list()
                stack = list()
                stack.append(segment)
                visited.add(segment)
                while stack:
                    segment = stack.pop()
                    loop.append(segment)
                    for neighbour in self.adjacencyList[segment]:
                        if neighbour not in visited:
                            stack.append(neighbour)
                            visited.add(neighbour)
                loops.append(loop)

        return loops
