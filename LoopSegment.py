from Vector2D import Vector2D
from typing import List
import numpy as np

class LoopSegment:
    def __init__(self, topLeft: Vector2D, bottomRight: Vector2D, points: List[Vector2D]):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.points = points

    def edgePoints(self):
        return [p for p in self.points if self.onEdge(p)]

    def onEdge(self, point: Vector2D):
        return point.x == self.topLeft.x or point.y == self.topLeft.y or \
               point.x == self.bottomRight.x or point.y == self.bottomRight.y

    def width(self):
        return self.bottomRight.x - self.topLeft.x

    def height(self):
        return self.bottomRight.y - self.topLeft.y

    def mid(self):
        return Vector2D((self.topLeft.x + self.bottomRight.x)//2, (self.topLeft.y + self.bottomRight.y)//2)

    def asMatrix(self):
        matrix = np.full((self.width()+1, self.height()+1), False)
        for point in self.points:
            matrix[point.x-self.topLeft.x, point.y-self.topLeft.y] = True

        return matrix
