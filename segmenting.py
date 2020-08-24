import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt

from Vector2D import Vector2D
import math


class ImageMatrix:
    def __init__(self, array: np.ndarray = None):
        self.array = array

    def width(self):
        return self.array.shape[0]

    def height(self):
        return self.array.shape[1]

    def toImage(self):
        return Image.fromarray(self.array).convert("L")

    def asBoolean(self):
        return self.array > 0

    def show(self):
        plt.imshow(self.array)
        plt.show()

    def asRatioOf(self, array2):
        return self.countFalse() / array2.countFalse()

    def countFalse(self):
        return self.array.size - np.count_nonzero(self.array)

    def getPolygons(self):



class PaddedImageMatrix(ImageMatrix):
    def __init__(self, array: np.ndarray = None, pad: int = 0):
        super().__init__(array)
        self.pad = pad

    def __init__(self, mapArray: ImageMatrix, pad: int = 0):
        super().__init__(ImageMatrix.array)
        self.pad = pad

    def paddedArray(self):
        return np.pad(self.array, (self.pad, self.pad), 'constant', constant_values=(0, 0))

    def paddedBooleanArray(self):
        return self.paddedArray() > 0