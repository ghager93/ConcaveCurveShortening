import numpy as np


# Based on https://pytorch.org/docs/stable/torchvision/utils.html
def make_grid(images, nrow=8, pad=2, normalise=False):
    if images.shape == 2:
        return np.pad(images, pad)

    if images.shape != 3:
        return -1

    nimages, height, width = images.shape

    out_shape = (height + 2*pad) * np.ceil(nimages / nrow), (width + 2*pad) * nrow
    out = np.zeros(out_shape, dtype=images.dtype)

    for i in range(nimages):
        out[i*(height + 2*pad):(i+1)*(height + 2*pad), i*(width + 2*pad):(i+1)*(width + 2*pad)] = np.pad(images[i], pad)

    return out


def make_square_grid(images, padding=2, normalise=False, pad_value=0):
    nrow = np.ceil(images.shape[0])
    return make_grid(images, nrow, padding, normalise, pad_value)
