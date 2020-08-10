from LoopSegment import LoopSegment
from Vector2D import Vector2D
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from booleanMatrixToPointList import booleanMatrixToPointList


def splitSegment(segment: LoopSegment):
    if segment.width() > segment.height():
        return splitSegmentHorizontally(segment)
    else:
        return splitSegmentVertically(segment)


def splitSegmentHorizontally(segment: LoopSegment):
    leftPoints = [p for p in segment.points if p.x <= segment.mid().x]
    rightPoints = [p for p in segment.points if p.x > segment.mid().x]

    leftSegment = LoopSegment(segment.topLeft, Vector2D(segment.mid().x, segment.bottomRight.y), leftPoints)
    rightSegment = LoopSegment(Vector2D(segment.mid().x+1, segment.topLeft.y), segment.bottomRight, rightPoints)

    return leftSegment, rightSegment


def splitSegmentVertically(segment: LoopSegment):
    upperPoints = [p for p in segment.points if p.y <= segment.mid().y]
    lowerPoints = [p for p in segment.points if p.y > segment.mid().y]

    upperSegment = LoopSegment(segment.topLeft, Vector2D(segment.bottomRight.x, segment.mid().y), upperPoints)
    lowerSegment = LoopSegment(Vector2D(segment.topLeft.x, segment.mid().y+1), segment.bottomRight, lowerPoints)

    return upperSegment, lowerSegment


def segmentMap(map: np.ndarray):
    mapSegment = LoopSegment(Vector2D(0, 0), Vector2D(map.shape[0]-1, map.shape[1]-1),
                             booleanMatrixToPointList(map))
    segments = list()
    stack = list()
    stack.append(mapSegment)
    while stack:
        curr = stack.pop()
        half1, half2 = splitSegment(curr)
        if half1.pointsAreContinuousFunction():
            segments.append(half1)
        else:
            stack.append(half1)

        if half2.pointsAreContinuousFunction():
            segments.append(half2)
        else:
            stack.append(half2)

    segmentedMatrix = np.full(map.shape, False)
    for segment in segments:
        segmentedMatrix[segment.topLeft.x:segment.bottomRight.x+1,
        segment.topLeft.y:segment.bottomRight.y+1] = segment.asOutlinedMatrix()

    plt.imshow(segmentedMatrix)
    plt.show()
