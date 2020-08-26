import numpy as np
from Vector2D import Vector2D
import random
from time import time

DIM = 10000
REPEAT = 100

loop_matrix = np.full((DIM, DIM), False)

vector_list = [Vector2D(x, random.randrange(0, DIM))
               for x in random.sample(range(DIM), DIM)]

loop_start = time()
for i in range(REPEAT):
    for v in vector_list:
        loop_matrix[v] ^= True
print('loop time:', time()-loop_start)

index_matrix = np.full((DIM, DIM), False)

index_start = time()
for i in range(REPEAT):
    index_matrix[[v[0] for v in vector_list], [v[1] for v in vector_list]] ^= True
print('index time:', time()-index_start)

zip_matrix = np.full((DIM, DIM), False)

zip_start = time()
for i in range(REPEAT):
    zip_matrix[tuple(zip(*vector_list))] ^= True
print('zip time:', time()-zip_start)

assert np.equal(loop_matrix, index_matrix).all()
assert np.equal(loop_matrix, zip_matrix).all()