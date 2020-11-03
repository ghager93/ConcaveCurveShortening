from unittest import TestCase

import LoopSegment
from Vector2D import Vector2D
from LoopSegment import LoopSegment
from PIL import Image, ImageOps
import ImageSegmenter
from segmenting import ImageSpace
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time
import cv2


class Test(TestCase):
    dirname = 'out/output_images/edge_detect/with_pad/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'

    image = Image.open('../' + dirname + filename + extension)
    # image = ImageOps.invert(image)
    image = image.convert("1")

    map = np.array(image)

    def test_split_segment_horizontally_left_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(10, 6)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        left, right = segment.splitSegmentHorizontally()
        assert left.topLeft == Vector2D(0, 0) and left.bottomRight == Vector2D(5, 6)

    def test_split_segment_horizontally_right_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(10, 6)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        left, right = segment.splitSegmentHorizontally()
        assert right.topLeft == Vector2D(6, 0) and right.bottomRight == Vector2D(10, 6)

    def test_split_segment_vertically_upper_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(6, 11)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        upper, lower = segment.splitSegmentVertically()
        assert upper.topLeft == Vector2D(0, 0) and upper.bottomRight == Vector2D(6, 5)

    def test_split_segment_vertically_lower_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(6, 11)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        upper, lower = segment.splitSegmentVertically()
        assert lower.topLeft == Vector2D(0, 6) and lower.bottomRight == Vector2D(6, 11)

    def test_segment_map(self):
        segments = ImageSegmenter.segmentMap(self.map)

        with open('segment_map_test.pkl', 'rb') as file:
            correct = pickle.load(file)

        assert set(segments) == set(correct)
        # segmentedMatrix = np.full(self.map.shape, False)
        # for segment in segments:
        #     segmentedMatrix[segment.topLeft.x:segment.bottomRight.x+1,
        #     segment.topLeft.y:segment.bottomRight.y+1] = segment.asOutlinedMatrix()
        #
        # plt.imshow(segmentedMatrix)
        # plt.show()

    def test_find_neighbours(self):
        with open('segment_map_test.pkl', 'rb') as file:
            segments = pickle.load(file)

        segmentGraph = ImageSegmenter.SegmentGraph(segments)
        segmentNeighbours = [segmentGraph.findNeighboursOf(s) for s in segments]

        with open('find_neighbours_test.pkl', 'rb') as file:
            segmentNeighboursCorrect = pickle.load(file)

        assert segmentNeighbours == segmentNeighboursCorrect

        # segmentedMatrix = np.zeros(self.map.shape, np.int8)
        # for segment in segments:
        #     segmentedMatrix[segment.topLeft.x:segment.bottomRight.x + 1,
        #     segment.topLeft.y:segment.bottomRight.y + 1] += segment.asMatrix().astype(int) \
        #                                                     + 2*segment.boundaryMatrix().astype(int)
        #
        # for i, neighbours in enumerate(segmentNeighbours):
        #     neighbourScreen = np.zeros(self.map.shape, np.int8)
        #     neighbourScreen[segments[i].topLeft.x:segments[i].bottomRight.x + 1,
        #     segments[i].topLeft.y:segments[i].bottomRight.y + 1] += 2
        #     for n in neighbours:
        #         neighbourScreen[segments[n].topLeft.x:segments[n].bottomRight.x + 1,
        #         segments[n].topLeft.y:segments[n].bottomRight.y + 1] += 1
        #
        #     segmentedMatrix += neighbourScreen
        #     plt.imshow(segmentedMatrix)
        #     plt.show()
        #     segmentedMatrix -= neighbourScreen

    def test_find_graph_loops(self):
        with open('segment_map_test.pkl', 'rb') as file:
            segments = pickle.load(file)

        segmentGraph = ImageSegmenter.SegmentGraph(segments)
        loops = segmentGraph.findGraphLoops()

        segmentedMatrix = np.zeros(self.map.shape, np.int8)
        for segment in segments:
            segmentedMatrix[segment.topLeft.x:segment.bottomRight.x + 1,
            segment.topLeft.y:segment.bottomRight.y + 1] += segment.asMatrix().astype(int) \
                                                            + 2*segment.boundaryMatrix().astype(int)

        for loop in loops:
            loopScreen = np.zeros(self.map.shape, np.int8)
            for i in loop:
                for p in segments[i].points:
                    loopScreen[p.x, p.y] += 2

            segmentedMatrix += loopScreen
            plt.imshow(segmentedMatrix)
            plt.show()
            segmentedMatrix -= loopScreen
