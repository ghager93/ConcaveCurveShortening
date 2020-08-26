import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrixOps import ImageMatrixOps
import polygonDetection
from dataclasses import dataclass
import singularity
from Vector2D import Vector2D
import math


class ImageMatrix(ImageMatrixOps):
    def __init__(self, matrix: np.ndarray = None):
        self.matrix = matrix
        self.polygons = self.getPolygons()

    @staticmethod
    def open(path: str):
        return ImageMatrix(ImageMatrix.openImageAsBooleanMatrix(path))

    def getPolygons(self):
        return polygonDetection.polygonCollection(self.matrix)


class PaddedImageMatrix(ImageMatrix):
    def __init__(self, matrix: np.ndarray = None, pad: int = 0):
        super().__init__(matrix)
        self.pad = pad

    def __init__(self, imageMatrix: ImageMatrix, pad: int = 0):
        super().__init__(imageMatrix.matrix)
        self.pad = pad

    def paddedArray(self):
        return np.pad(self.matrix, (self.pad, self.pad), 'constant', constant_values=(0, 0))

    def paddedBooleanArray(self):
        return self.paddedArray() > 0

@dataclass
class Polygon(ImageMatrixOps):
    matrix: np.ndarray
    worldPos: Vector2D

    def __post_init__(self):
        self.rootSingularity = self.selectSingularity()

    def selectSingularity(self):
        return singularity.selectSingularityEdgeDeletion(self.matrix)


def getTestImageMatrix() -> ImageMatrix:
    path = '../bin/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
    return ImageMatrix.open(path)


def main():
    path = 'bin/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
    im = ImageMatrix.open(path)
    pass


if __name__ == '__main__':
    main()