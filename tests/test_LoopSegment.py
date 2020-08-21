from unittest import TestCase
import LoopSegment
from Vector2D import Vector2D
import numpy as np
import time


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

    def test_is_neighbour_on_right_side_true(self):
        neighbourPoints = [Vector2D(6, 1), Vector2D(7, 3)]
        neighbour = LoopSegment.LoopSegment(Vector2D(6, 1), Vector2D(7, 7), neighbourPoints)
        assert self.segment.isNeighbourOf(neighbour)

    def test_is_neighbour_on_right_side_false(self):
        neighbourPoints = [Vector2D(6, 7), Vector2D(7, 3)]
        neighbour = LoopSegment.LoopSegment(Vector2D(6, 1), Vector2D(7, 7), neighbourPoints)
        assert not self.segment.isNeighbourOf(neighbour)

    def test_is_neighbour_on_top_side_true(self):
        neighbourPoints = [Vector2D(1, -3), Vector2D(1, -1)]
        neighbour = LoopSegment.LoopSegment(Vector2D(0, -5), Vector2D(5, -1), neighbourPoints)
        assert self.segment.isNeighbourOf(neighbour)

    def test_is_neighbour_time(self):
        neighbourPoints = [Vector2D(x, 7) for x in range(1, 7)]
        neighbour = LoopSegment.LoopSegment(Vector2D(1, 6), Vector2D(7, 7), neighbourPoints)

        start1 = time.time()
        for i in range(100):
            assert not self.segment.isNeighbourOf(neighbour)
        end1 = time.time()
        print('time 1', end1 - start1)
