import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrixOps import ImageMatrixOps
import imageMatrixOps
import polygonDetection
from dataclasses import dataclass
import segmenting
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
            xor = imageMatrixOps.xorEdgeDetect(matrix)
            xor_shifted = np.full(matrix.shape, False)
            xor_shifted[:-1, :-1] = xor[1:, 1:]
            edge = xor | xor_shifted
            if not (matrix & np.invert(edge)).any():
                break
            matrix &= np.invert(edge)

        return imageMatrixOps.booleanMatrixToPointList(matrix)

    return random.choice(findCandidateSingularitiesViaEdgeDeletion())
