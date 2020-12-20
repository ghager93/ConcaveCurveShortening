import numpy as np
from functools import wraps
from scipy.spatial import KDTree
from typing import List
from pprint import pprint

from . import transforms

from bin.image_array import convert_to_points_list


def _array_to_points_list_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args = [convert_to_points_list(a) if type(a) is np.ndarray else a for a in args]
        kwargs = {kw: (convert_to_points_list(a) if type(a) is np.ndarray else a) for (kw, a) in kwargs.items()}
        return func(*args, **kwargs)

    return wrapper


@_array_to_points_list_wrapper
def skeleton_mapping(skeleton, edges):
    tree = KDTree(skeleton)
    dictionary = {sk: set() for sk in skeleton}

    for edge in edges:
        edge_query = tree.query(edge)
        dictionary[skeleton[edge_query[1]]].add((edge, edge_query[0]))

    return dictionary


@_array_to_points_list_wrapper
def mapping_distance_transform(image, tree):
    out = np.zeros(image.shape)
    out[tuple(p for p in zip(*image))] = tree.query(image)[0]

    return out


def _main():
    edges = np.zeros((9, 9), int)
    edges[(1, 4, 1, 5, 1, 6, 8, 2), (2, 2, 3, 3, 4, 6, 7, 8)] = 1

    skeleton = np.zeros((9, 9), int)
    skeleton[(6, 1, 6), (2, 6, 7)] = 1

    dictionary = skeleton_mapping(skeleton, edges)
    pprint(dictionary)


if __name__ == '__main__':
    _main()