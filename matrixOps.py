from scipy.sparse import csr_matrix
import numpy as np
from Vector2D import Vector2D
from PIL import Image, ImageOps
from typing import Tuple


def openImageAsBooleanMatrix(imagePath: str):
    return np.array(ImageOps.invert(Image.open(imagePath)).convert("1"))

# def openImageAsBooleanMatrix(imagePath: str, matrixDimensions: Tuple[int]):
#     image = openImageAsBooleanMatrix(imagePath)
#     return image.resize(matrixDimensions)

def booleanMatrixToPointList(matrix):
    csr = csr_matrix(matrix)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]
