import numpy as np
import pandas as pd
import time

from scipy.spatial import KDTree

import bin.utils.imshow
from bin import image
from bin import image_array

from bin.morphology import transforms

from bin.utils.base_dir import base_dir

im = image.open_image(base_dir + 'lib/silhouettes/afghanistan-silhouette.bmp')
im = image.scale(im, 0.05)

for i in range(4):
    arr = image_array.invert(image_array.convert_image_to_array(im))
    skl = transforms.skeleton_transform(arr)

    arr_points = image_array.convert_to_points_list(arr)
    skl_points = image_array.convert_to_points_list(skl)

    if len(arr_points) > 5000:
        idx = np.round(np.linspace(0, len(arr_points)-1, 5000)).astype(int)
        arr_points = [arr_points[x] for x in idx]

    arr2 = np.copy(arr)
    arr2[tuple(p for p in zip(*arr_points))] = 2
    bin.utils.imshow.show(arr2)

    tree = KDTree(skl_points)
    print('skl size', len(skl_points))
    print('arr size', len(arr_points))
    tstart = time.time()
    print(tree.query(arr_points))
    print('time', time.time() - tstart)

    im = image.scale(im, 2)
