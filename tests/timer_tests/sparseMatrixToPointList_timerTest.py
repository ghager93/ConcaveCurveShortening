from scipy.sparse import csr_matrix
import numpy as np
import matplotlib.pyplot as plt
from time import time
from Vector2D import Vector2D

matrix = np.empty(1000 * 1000)
matrix.fill(False)
matrix[:200 * 200] = True
np.random.shuffle(matrix)
matrix = matrix.reshape((1000, 1000))

start_csr = time()
for i in range(1):
    csr = None
    pointList_csr = None
    csr = csr_matrix(matrix)
    pointList_csr = [Vector2D(x, y)
                 for x in range(csr.shape[0])
                 for y in csr.indices[csr.indptr[x]:csr.indptr[x+1]]]
end_csr = time()

start_loop = time()
for i in range(1):
    pointList_loop = None
    pointList_loop = [Vector2D(ix, iy) for ix, iy in np.ndindex(matrix.shape)
                 if matrix[ix, iy]]
end_loop = time()

assert set(pointList_csr) == set(pointList_loop)
print('csr', (end_csr - start_csr))
print('loop', (end_loop - start_loop))
