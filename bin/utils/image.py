from functools import wraps

import numpy as np
from scipy.sparse import csr_matrix

from bin.utils.vector2d import Vector2D


def convert_to_points_list(array: np.ndarray):
    return _convert_to_points_list2(array)


def _convert_to_points_list(array: np.ndarray):
    csr = csr_matrix(array)
    return [Vector2D(x, y)
            for x in range(csr.shape[0])
            for y in csr.indices[csr.indptr[x]:csr.indptr[x + 1]]]


def _convert_to_points_list2(array: np.ndarray):
    return [Vector2D(p[0], p[1]) for p in zip(*np.where(array))]


def point_map_to_image(point_map: dict, shape):
    image = np.zeros(shape, int)
    image[tuple(p for p in zip(*point_map.keys()))] = list(point_map.values())

    return image


def _array_to_points_list_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = [convert_to_points_list(a) if type(a) is np.ndarray else a for a in args]
        kwargs = {kw: (convert_to_points_list(a) if type(a) is np.ndarray else a) for (kw, a) in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper