from scipy.sparse import csr_matrix
import numpy as np
from Vector2D import Vector2D
from PIL import Image, ImageOps
from typing import Tuple

class ImageMatrixOps:
    def __init__(self):
        self.matrix = None

    def booleanMatrixToPointList(self):
        csr = csr_matrix(self.matrix)
        return [Vector2D(x, y)
                for x in range(csr.shape[0])
                for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]

    def zeroPad(self, pad):
        return np.pad(self.matrix, (pad, pad), 'constant', constant_values=(0, 0))

    def xorEdgeDetect(self):
        matrix = self.zeroPad(1)

        horizontalEdgeArray = self.xorArrays(matrix[:-1, 1:], matrix[1:, 1:])
        verticalEdgeArray = self.xorArrays(matrix[1:, :-1], matrix[1:, 1:])

        return horizontalEdgeArray | verticalEdgeArray

    @staticmethod
    def openImageAsBooleanMatrix(imagePath: str):
        return np.array(ImageOps.invert(Image.open(imagePath)).convert("1"))

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