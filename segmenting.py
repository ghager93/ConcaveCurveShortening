import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrixOps import ImageMatrixOps

from Vector2D import Vector2D
import math


class ImageMatrix(ImageMatrixOps):
    def __init__(self, matrix: np.ndarray = None):
        self.matrix = matrix

    def width(self):
        return self.matrix.shape[0]

    def height(self):
        return self.matrix.shape[1]

    def toImage(self):
        return Image.fromarray(self.matrix).convert("L")

    def asBoolean(self):
        return self.matrix > 0

    def show(self):
        plt.imshow(self.matrix)
        plt.show()

    def asRatioOf(self, array2):
        return self.countFalse() / array2.countFalse()

    def countFalse(self):
        return self.matrix.size - np.count_nonzero(self.matrix)

    def getPolygons(self):
        pass


class PaddedImageMatrix(ImageMatrix):
    def __init__(self, matrix: np.ndarray = None, pad: int = 0):
        super().__init__(matrix)
        self.pad = pad

    def __init__(self, mapArray: ImageMatrix, pad: int = 0):
        super().__init__(ImageMatrix.array)
        self.pad = pad

    def paddedArray(self):
        return np.pad(self.matrix, (self.pad, self.pad), 'constant', constant_values=(0, 0))

    def paddedBooleanArray(self):
        return self.paddedArray() > 0