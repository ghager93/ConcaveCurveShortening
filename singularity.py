import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrix import ImageMatrix
import imageMatrix
from dataclasses import dataclass
import random
from Vector2D import Vector2D
import math


def selectSingularityManually(matrix: np.ndarray):
    print('Select x value between 0 and', matrix.shape[0])
    x = int(input())
    print('Select y value between 0 and', matrix.shape[1])
    y = int(input())

    return Vector2D(x, y)


def selectSingularityEdgeDeletion(matrix: np.ndarray):
    def findCandidateSingularitiesViaEdgeDeletion():
        nonlocal matrix
        matrix = np.copy(matrix)
        while True:
            edge = imageMatrix.xorEdgeDetect(matrix)
            if not (matrix & np.invert(edge)).any():
                break
            matrix &= np.invert(edge)

        return imageMatrix.booleanMatrixToPointList(matrix)

    return random.choice(findCandidateSingularitiesViaEdgeDeletion())
