import numpy as np

from . import bilinear_interp


def bilinear_interp_upsample(im: np.ndarray, resolution, upsample_factor):
    ix = np.linspace(0, resolution[1] * resolution, resolution[1], endpoint=False)
    iy = np.linspace(0, resolution[0] * resolution, resolution[0], endpoint=False)

    mx, my = np.meshgrid(ix, iy)

    return bilinear_interp.bilinear_interpolate(im, mx, my)