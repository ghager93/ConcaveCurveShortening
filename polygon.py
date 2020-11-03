from dataclasses import dataclass

import numpy as np

import raytracePolygonIntersection
import singularity
from Vector2D import Vector2D
from imageMatrix import ImageMatrix


@dataclass
class Polygon(ImageMatrix):
    matrix: np.ndarray
    worldPos: Vector2D

    def __post_init__(self):
        self.rootSingularity = self.selectSingularity()
        self.kernel = self.findKernel()

    def selectSingularity(self):
        return singularity.selectSingularityEdgeDeletion(self.matrix)

    def findKernel(self):
        return raytracePolygonIntersection.intersectingLinesFromPoint(self.rootSingularity, self.matrix)
    
    def polygonAndKernelAndSingularity(self):
        ret = self.matrix.astype(int) + self.kernel.astype(int)
        ret[self.rootSingularity] += 1
        return ret