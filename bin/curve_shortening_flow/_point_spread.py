import numpy as np

from scipy.ndimage import gaussian_filter1d


def gaussian(x, sigma):
    return gaussian_filter1d(x, sigma, axis=0, mode='wrap')


def gaussian_func(sigma):
    return lambda x: gaussian_filter1d(x, sigma, axis=0, mode='wrap')
