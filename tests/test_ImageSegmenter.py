from unittest import TestCase
from Vector2D import Vector2D
from LoopSegment import LoopSegment
from PIL import Image, ImageOps
import ImageSegmenter
from booleanFilter import MapArray
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

class Test(TestCase):
    dirname = 'bin/output_images/edge_detect/with_pad/'
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

        left, right = ImageSegmenter.splitSegmentHorizontally(segment)
        assert left.topLeft == Vector2D(0, 0) and left.bottomRight == Vector2D(5, 6)

    def test_split_segment_horizontally_right_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(10, 6)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        left, right = ImageSegmenter.splitSegmentHorizontally(segment)
        assert right.topLeft == Vector2D(6, 0) and right.bottomRight == Vector2D(10, 6)

    def test_split_segment_vertically_upper_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(6, 11)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        upper, lower = ImageSegmenter.splitSegmentVertically(segment)
        assert upper.topLeft == Vector2D(0, 0) and upper.bottomRight == Vector2D(6, 5)

    def test_split_segment_vertically_lower_segment(self):
        topLeft = Vector2D(0, 0)
        bottomRight = Vector2D(6, 11)
        pointList = [Vector2D(0, 0), Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1), Vector2D(4, 3), Vector2D(5, 1),
                     Vector2D(2, 5)]
        segment = LoopSegment(topLeft, bottomRight, pointList)

        upper, lower = ImageSegmenter.splitSegmentVertically(segment)
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

        start1 = time.time()
        for i in range(5):
            segmentNeighbours = [ImageSegmenter.findNeighbours(segments, s) for s in segments]
        end1 = time.time()

        print('time 1', end1 - start1)

