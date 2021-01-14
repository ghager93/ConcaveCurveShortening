import numpy as np


def colour_matrix_with_gradient(matrix, polygons):
    coloured_matrix = np.zeros(matrix.shape)
    for i, polygon in enumerate(polygons):
        rows, cols = zip(*polygon.points)
        coloured_matrix[rows, cols] = (i + 1)/len(polygons)

    return coloured_matrix


def colour_matrix_with_rgb(matrix, polygons):
    coloured_matrix = np.zeros(matrix.shape + (3,))
    colours = _get_n_equidistant_rgb(len(polygons))
    for i, polygon in enumerate(polygons):
        rows, cols = zip(*polygon.points)
        coloured_matrix[rows, cols, :] = colours[i]

    return coloured_matrix


def _get_n_equidistant_rgb(n: int):
    return [_get_rgb_at_angle(a) for a in 6 * (np.arange(n) + 1) / n]


def _get_rgb_at_angle(angle: float):
    assert 0 < angle <= 6

    X = 1 - abs(angle % 2 - 1)

    if np.ceil(angle) == 1:
        return 1, X, 0
    if np.ceil(angle) == 2:
        return X, 1, 0
    if np.ceil(angle) == 3:
        return 0, 1, X
    if np.ceil(angle) == 4:
        return 0, X, 1
    if np.ceil(angle) == 5:
        return X, 0, 1
    if np.ceil(angle) == 6:
        return 1, 0, X