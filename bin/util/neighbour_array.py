import numpy as np


def binary_to_array(n: int):
    arr = np.zeros((3, 3), dtype='bool')
    arr[0, 0] = n & 0b10000000
    arr[0, 1] = n & 0b00000001
    arr[0, 2] = n & 0b00000010
    arr[1, 0] = n & 0b01000000
    arr[1, 1] = 0
    arr[1, 2] = n & 0b00000100
    arr[2, 0] = n & 0b00100000
    arr[2, 1] = n & 0b00010000
    arr[2, 2] = n & 0b00001000

    return arr.astype(int)