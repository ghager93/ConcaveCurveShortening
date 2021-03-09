import numpy as np


def delta(v):
    return v - np.roll(v, 1, 0)


def forward_delta(v):
    return np.roll(v, -1, 0) - v


def tangent(v):
    return delta(v)


def normal(v):
    return forward_delta(delta(v))
