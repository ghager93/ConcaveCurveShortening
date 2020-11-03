import numpy as np
from imageMatrix import ImageMatrix
from polygonDetection import polygonCollection
import matplotlib.pyplot as plt

class ImageSpace(ImageMatrix):
    def __init__(self, matrix: np.ndarray = None):
        self.matrix = matrix
        self.polygons = self.getPolygons()

    @staticmethod
    def open(path: str):
        return ImageSpace(ImageSpace.openImageAsBooleanMatrix(path))

    def getPolygons(self):
        return polygonCollection(self.matrix)


class PaddedImageMatrix(ImageSpace):
    def __init__(self, matrix: np.ndarray = None, pad: int = 0):
        super().__init__(matrix)
        self.pad = pad

    def __init__(self, imageMatrix: ImageSpace, pad: int = 0):
        super().__init__(imageMatrix.matrix)
        self.pad = pad

    def paddedArray(self):
        return np.pad(self.matrix, (self.pad, self.pad), 'constant', constant_values=(0, 0))

    def paddedBooleanArray(self):
        return self.paddedArray() > 0


def getTestImageMatrix() -> ImageSpace:
    path = '../out/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
    return ImageSpace.open(path)


def main():
    path = 'out/output_images/small/polygons.bmp'
    im = ImageSpace.open(path)
    pass


if __name__ == '__main__':
    main()