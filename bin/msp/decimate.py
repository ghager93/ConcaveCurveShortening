import numpy as np


def decimate(im: np.ndarray, ratio):
    out = np.zeros(im.shape, int)
    id = int(1 / ratio)
    out[::id, ::id] = im[::id, ::id]

    return out


def decimate_to_n_points(im: np.ndarray, n: int):
    out = np.zeros(im.shape, int)
    id = int(np.sqrt(np.count_nonzero(im) / n))
    out[::id, ::id] = im[::id, ::id]

    return out


def downsize(im: np.ndarray, ratio):
    id = int(1 / ratio)
    return im[::id, ::id]


def downsize_to_n_points(im: np.ndarray, n: int):
    id = int(np.sqrt(np.count_nonzero(im) / n))
    return im[::id, ::id]
