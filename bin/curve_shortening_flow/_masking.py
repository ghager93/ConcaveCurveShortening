import numpy as np

def heaviside(x):
    return np.heaviside(x, 0)

def continuous_heaviside_non_negative(x, k=5):
    return np.where(x > 0, 2/(1 + np.exp(-k*x)) - 1, 0)
