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
                                      np.array([[True, True, False, False, False, False],
                                                [True, True, False, False, False, False],
                                                [False, False, False, False, False, True],
                                                [False, False, False, False, False, False],
                                                [False, False, False, True, False, False],
                                                [False, True, False, False, False, False]]))

    def test_merge_neighbouring_points(self):
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(6, 0), Vector2D(7, 0), Vector2D(0, 1), Vector2D(9, 5),
                     Vector2D(9, 4), Vector2D(9, 6), Vector2D(9, 9)]
        assert set(LoopSegment.LoopSegment.mergeNeighbouringPoints(pointList)) == \
               {Vector2D(0, 0), Vector2D(6, 0), Vector2D(9, 4), Vector2D(9, 9)}

    def test_horizontal_lines_are_consecutive_true(self):
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(1, 2), Vector2D(2, 3), Vector2D(3, 3)]
        assert LoopSegment.LoopSegment(None, None, pointList).horizontalLinesAreConsecutive()

    def test_horizontal_lines_are_consecutive_false(self):
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(1, 2), Vector2D(2, 3), Vector2D(3, 3), Vector2D(5, 0)]
        assert not LoopSegment.LoopSegment(None, None, pointList).horizontalLinesAreConsecutive()

    def test_vertical_lines_are_consecutive_true(self):
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(1, 2), Vector2D(2, 3), Vector2D(3, 3), Vector2D(1, 1)]
        assert LoopSegment.LoopSegment(None, None, pointList).horizontalLinesAreConsecutive()

    def test_vertical_lines_are_consecutive_false(self):
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(1, 2), Vector2D(2, 3), Vector2D(3, 3), Vector2D(5, 0)]
        assert not LoopSegment.LoopSegment(None, None, pointList).horizontalLinesAreConsecutive()
