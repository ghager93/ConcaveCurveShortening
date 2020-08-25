from segmenting import ImageMatrix
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrixOps import ImageMatrixOps
import polygonDetection
import singularity

from Vector2D import Vector2D
import math

path = 'bin/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
im = ImageMatrix.open(path)
original = ImageMatrix.open(path)

# while im.matrix.any():
#     remainder = np.copy(im.matrix)
#     xor_shifted = np.full(im.shape(), False)
#     xor_shifted[:-1, :-1] = im.xorEdgeDetect()[1:, 1:]
#     edge = im.xorEdgeDetect() | xor_shifted
#     im.matrix &= np.invert(edge)

points = singularity.selectSingularityEdgeDeletion(im.matrix)
pass

    # plt.imshow(im.matrix)
    # plt.show(block=False)
    # plt.pause(1)
    # plt.close()

# plt.imshow(remainder)
# plt.show()