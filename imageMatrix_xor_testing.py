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
from time import time

path = 'bin/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
im = ImageMatrix.open(path)
original = ImageMatrix.open(path)

start = time()
singularity = singularity.selectSingularityEdgeDeletion(im.matrix)
print('singularity time:', time()-start)

singularity_matrix = im.matrix.astype(int)
singularity_matrix[singularity] += 1
plt.imshow(singularity_matrix)
plt.show()