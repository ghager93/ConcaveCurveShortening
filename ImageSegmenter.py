from LoopSegment import LoopSegment
from Vector2D import Vector2D
import numpy as np
import matplotlib as plt
from typing import List


def splitSegment(segment: LoopSegment):
    if segment.width() > segment.height():
        return splitSegmentHorizontally(segment)
    else:
        return splitSegmentVertically(segment)


def splitSegmentHorizontally(segment: LoopSegment):
    leftPoints = [p for p in segment.points if p.x <= segment.mid().x]
    rightPoints = [p for p in segment.points if p.x > segment.mid().x]

    leftSegment = LoopSegment(segment.topLeft, Vector2D(segment.mid().x, segment.bottomRight.y), leftPoints)
    rightSegment = LoopSegment(Vector2D(segment.mid().x, segment.topLeft.y), segment.bottomRight, rightPoints)

    return leftSegment, rightSegment

def splitSegmentVertically(segment: LoopSegment):
    upperPoints = [p for p in segment.points if p.y <= segment.mid().y]
    lowerPoints = [p for p in segment.points if p.y > segment.mid().y]

    upperSegment = LoopSegment(segment.topLeft, Vector2D())

def segmentImage(image):