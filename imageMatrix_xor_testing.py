from segmenting import ImageSpace
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from matplotlib import pyplot as plt
from imageMatrix import ImageMatrix
import polygonDetection
import singularity
from Vector2D import Vector2D
import math
from time import time

path = 'out/output_images/small/afghanistan-silhouette_circle_5_small.bmp'
im = ImageSpace.open(path)
original = ImageSpace.open(path)

start = time()
singularity = singularity.selectSingularityEdgeDeletion(im.matrix)
print('singularity time:', time()-start)

singularity_matrix = im.matrix.astype(int)
singularity_matrix[singularity] += 1
plt.imshow(singularity_matrix)
plt.show()