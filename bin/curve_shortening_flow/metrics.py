import numpy as np

import vector_diff


def curve_length(curve):
    return sum(np.linalg.norm(curve - np.roll(curve, 1, 0), axis=1))


def mean_point_length(curve):
    return curve_length(curve) / curve.shape[0]


def concavity(curve):
    return sum(np.cross(vector_diff.tangent(curve), vector_diff.normal(curve)))


