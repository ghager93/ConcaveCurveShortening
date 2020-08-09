from unittest import TestCase
from Vector2D import Vector2D
from LoopSegment import LoopSegment
from PIL import Image, ImageOps
import ImageSegmenter
from booleanFilter import MapArray
import numpy as np


class Test(TestCase):
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
        dirname = 'bin/output_images/edge_detect/with_pad/'
        filename = 'afghanistan-silhouette_circle_5_small'
        extension = '.bmp'

        image = Image.open('../' + dirname + filename + extension)
        # image = ImageOps.invert(image)
        image = image.convert("1")

        map = np.array(image)

        ImageSegmenter.segmentMap(map)

