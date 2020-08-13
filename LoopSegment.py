from Vector2D import Vector2D
from typing import List
import numpy as np

class LoopSegment:
    def __init__(self, topLeft: Vector2D, bottomRight: Vector2D, points: List[Vector2D]):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.points = points

    def __eq__(self, other):
        if not isinstance(other, LoopSegment):
            return False
        return other.topLeft == self.topLeft and \
               other.bottomRight == self.bottomRight and \
               other.points == self.points

    def entryAndExits(self):
        return self.mergeNeighbouringPoints(self.edgePoints())

    def edgePoints(self):
        return [p for p in self.points if self.onEdge(p)]

    def onEdge(self, point: Vector2D):
        return self.onTopEdge(point) or self.onBottomEdge(point) or \
               self.onLeftEdge(point) or self.onRightEdge(point)

    def onTopEdge(self, point: Vector2D):
        return point.y == self.topLeft.y

    def onBottomEdge(self, point: Vector2D):
        return point.y == self.bottomRight.y

    def onLeftEdge(self, point: Vector2D):
        return point.x == self.topLeft.x

    def onRightEdge(self, point: Vector2D):
        return point.x == self.bottomRight.x

    @staticmethod
    def mergeNeighbouringPoints(points: List[Vector2D]):
        points = set(points)
        mergedPoints = set()
        visited = set()
        for point in points:
            if point not in visited:
                neighbourhood = set()
                stack = list()
                stack.append(point)
                while stack:
                    point = stack.pop()
                    visited.add(point)
                    neighbourhood.add(point)
                    for neighbour in points-visited:
                        if point.manhattanDistanceTo(neighbour) == 1:
                            stack.append(neighbour)
                mergedPoints.add(min(neighbourhood))

        return mergedPoints

    def width(self):
        return self.bottomRight.x - self.topLeft.x + 1

    def height(self):
        return self.bottomRight.y - self.topLeft.y + 1

    def mid(self):
        return Vector2D((self.topLeft.x + self.bottomRight.x)//2, (self.topLeft.y + self.bottomRight.y)//2)

    def asMatrix(self):
        matrix = np.full((self.width(), self.height()), False)
        for point in self.points:
            matrix[point.x-self.topLeft.x, point.y-self.topLeft.y] = True

        return matrix

    # def pointsAreSubSetOfFunction(self):
    #     return len(self.points) == len(set(p.x for p in self.points)) or \
    #            len(self.points) == len(set(p.y for p in self.points))

    def pointsAreFunction(self):
        return not self.points or \
               self.horizontalLinesAreConsecutive() or self.verticalLinesAreConsecutive()

    def horizontalLinesAreConsecutive(self):
        points = sorted(self.points, key=lambda p: p.y)
        currFirst = points[0]
        currEnum = 0

        for e, p in enumerate(points):
            if p.y != currFirst.y:
                currFirst = p
                currEnum = e
            elif p.x - currFirst.x != e - currEnum:
                return False

        return True

    def verticalLinesAreConsecutive(self):
        points = sorted(self.points, key=lambda p: p.x)
        currFirst = points[0]
        currEnum = 0

        for e, p in enumerate(points):
            if p.x != currFirst.x:
                currFirst = p
                currEnum = e
            elif p.y - currFirst.y != e - currEnum:
                return False

        return True

    def pointsAreContinuous(self):
        return len(self.entryAndExits()) <= 2

    def pointsAreContinuousFunction(self):
        return self.pointsAreContinuous() and self.pointsAreFunction()

    def asOutlinedMatrix(self):
        matrix = self.asMatrix()
        matrix[0, :] = True
        matrix[:, 0] = True
        matrix[-1, :] = True
        matrix[:, -1] = True
        return matrix

    def isNeighbour(self, other: 'LoopSegment'):
        selfBorderPoints = set()
        otherBorderPoints = set()
        if other == self:
            return False
        if self.topLeft.x == other.bottomRight.x + 1:
            selfBorderPoints = {p for p in self.points if self.onLeftEdge(p)}
            otherBorderPoints = {p for p in other.points if other.onRightEdge(p)}
        if self.topLeft.y == other.bottomRight.y + 1:
            selfBorderPoints = {p for p in self.points if self.onTopEdge(p)}
            otherBorderPoints = {p for p in other.points if other.onBottomEdge(p)}
        if self.bottomRight.x == other.topLeft.x - 1:
            selfBorderPoints = {p for p in self.points if self.onRightEdge(p)}
            otherBorderPoints = {p for p in other.points if other.onLeftEdge(p)}
        if self.bottomRight.y == other.topLeft.y - 1:
            selfBorderPoints = {p for p in self.points if self.onBottomEdge(p)}
            otherBorderPoints = {p for p in other.points if other.onTopEdge(p)}

        return any([p1.manhattanDistanceTo(p2) == 1 for p2 in otherBorderPoints
                    for p1 in selfBorderPoints])
