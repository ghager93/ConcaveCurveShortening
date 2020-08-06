from unittest import TestCase
import LoopSegment
from Vector2D import Vector2D
import numpy as np


class TestLoopSegment(TestCase):
    topLeft = Vector2D(0, 0)
    bottomRight = Vector2D(5, 5)
    pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                 Vector2D(2, 5)]
    segment = LoopSegment.LoopSegment(topLeft, bottomRight, pointList)

    def test_on_edge_true(self):
        assert self.segment.onEdge(Vector2D(1, 5))

    def test_on_edge_false(self):
        assert not self.segment.onEdge(Vector2D(3, 3))

    def test_edge_points(self):
        assert set(self.segment.edgePoints()) == {Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(5, 1),
                                                  Vector2D(2, 5)}

    def test_as_matrix(self):
        np.testing.assert_array_equal(self.segment.asMatrix(),
                                             np.array([[True,  True,  False, False, False, False],
                                                       [True,  True,  False, False, False, False],
                                                       [False, False, False, False, False,  True],
                                                       [False, False, False, False, False, False],
                                                       [False, False, False, True,  False, False],
                                                       [False, True,  False, False, False, False]]))
