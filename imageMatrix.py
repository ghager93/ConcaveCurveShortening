from scipy.sparse import csr_matrix
import numpy as np
from Vector2D import Vector2D
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple

@dataclass
class ImageMatrix:
    matrix: np.ndarray

    def booleanMatrixToPointList(self):
        csr = csr_matrix(self.matrix)
        return [Vector2D(x, y)
                for x in range(csr.shape[0])
                for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]

    def zeroPaddedMatrix(self, pad):
        return np.pad(self.matrix, (pad, pad), 'constant', constant_values=(0, 0))

    def xorEdgeDetect2(self):
        matrix = self.zeroPaddedMatrix(1)

        horizontalEdgeArray = self.xorArrays(matrix[:-1, 1:], matrix[1:, 1:])
        verticalEdgeArray = self.xorArrays(matrix[1:, :-1], matrix[1:, 1:])

        xor = horizontalEdgeArray[:-1, :-1] | verticalEdgeArray[:-1, :-1]
        xor_shifted = np.full(xor.shape, False)
        xor_shifted[:-1, :-1] = xor[1:, 1:]

        return matrix[1:-1, 1:-1] & (xor | xor_shifted)

    def xorEdgeDetect(self):
        matrix = self.zeroPaddedMatrix(1)
        return matrix[1:-1, 1:-1] & np.invert(matrix[1:-1, :-2] & matrix[1:-1, 2:] &
                                              matrix[:-2, 1:-1] & matrix[2:, 1:-1])

    def shape(self):
        return self.matrix.shape

    def width(self):
        return self.matrix.shape[0]

    def height(self):
        return self.matrix.shape[1]

    def toImage(self):
        return Image.fromarray(self.matrix).convert("L")

    def asBoolean(self):
        return self.matrix > 0

    def showForNSeconds(self, n: int = 1):
        plt.imshow(self.matrix)
        plt.show(block=False)
        plt.pause(n)
        plt.close()

    def showUntilKeyPress(self):
        plt.imshow(self.matrix)
        plt.show(block=False)
        plt.waitforbuttonpress(0)
        plt.close()

    def asRatioOf(self, matrix2):
        return self.countFalse() / matrix2.countFalse()

    def countFalse(self):
        return self.matrix.size - np.count_nonzero(self.matrix)

    @staticmethod
    def openImageAsBooleanMatrix(imagePath: str):
        return np.invert(np.array(Image.open(imagePath).convert("1")))

    @staticmethod
    def xorArrays(array1: np.ndarray, array2: np.ndarray):
        return array1 ^ array2

    @staticmethod
    def spreadPoints(array: np.ndarray, spread: int):
        convolvedArray = np.copy(array)
        for ix in range(array.shape[0]-spread):
            convolvedArray[ix, :] = np.convolve(convolvedArray[ix, :-spread+1], np.full(spread, True))

        for iy in range(array.shape[1]-spread):
            convolvedArray[:, iy] = np.convolve(convolvedArray[:-spread+1, iy], np.full(spread, True))

        return convolvedArray


def xorEdgeDetect(matrix: np.ndarray):
    im = ImageMatrix(matrix)
    return im.xorEdgeDetect()


def booleanMatrixToPointList(matrix: np.ndarray):
    csr = csr_matrix(matrix)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]