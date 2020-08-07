from scipy.sparse import csr_matrix
import numpy as np
from Vector2D import Vector2D


def booleanMatrixToPointList(matrix):
    csr = csr_matrix(matrix)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]
