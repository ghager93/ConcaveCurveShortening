import numpy as np

from bin.msp import _bilinear_interp


def upsample(image: np.ndarray, resolution, ratio):
    return _bilinear_interp_upsample(image, resolution, ratio)


def _bilinear_interp_upsample(im: np.ndarray, resolution, ratio):
    ix = np.linspace(0, resolution[1] * ratio, resolution[1], endpoint=False)
    iy = np.linspace(0, resolution[0] * ratio, resolution[0], endpoint=False)

    mx, my = np.meshgrid(ix, iy)

    return _bilinear_interp.bilinear_interpolate(im, mx, my)
