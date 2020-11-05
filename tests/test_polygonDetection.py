from unittest import TestCase
import polygonDetection
from Vector2D import Vector2D
import numpy as np
import segmenting


class Test(TestCase):
    im = segmenting.getTestImageMatrix()

    def test_unvisited_neighbours(self):
        visited = {Vector2D(0, 0), Vector2D(3, 3)}
        curr = Vector2D(1, 0)
        matrix = np.array([[1, 1, 0, 0],
                           [1, 1, 0, 0],
                           [0, 0, 0, 0]])
        assert polygonDetection.getUnvisitedNeighbours(matrix, curr, visited) == [Vector2D(1, 1)]

    def test_polygon_collection(self):
        polygons = polygonDetection.polygonCollection()