import numpy as np
from matplotlib import pyplot as plt

from bin.adj_image_array import CLOSE_METHOD_KEY_PRESS

CLOSE_TIME_DEFAULT = 1


def show(array: np.ndarray, close_method: str=CLOSE_METHOD_KEY_PRESS, close_time: int=CLOSE_TIME_DEFAULT):
    plt.imshow(array)
    if close_method == CLOSE_METHOD_KEY_PRESS:
        _show_until_key_press()
    if close_method == CLOSE_METHOD_TIMER:
        _show_for_n_seconds(close_time)


def show_multiple(arrays: list):
    columns = int(np.ceil(np.sqrt(len(arrays))))
    rows = int(len(arrays)//columns + 1)

    fig = plt.figure()
    for i, array in enumerate(arrays):
        fig.add_subplot(rows, columns, i+1)
        plt.imshow(array)

    _show_until_key_press()


def _show_for_n_seconds(n: int):
    plt.show(block=False)
    plt.pause(n)
    plt.close()


def _show_until_key_press():
    plt.show(block=False)
    button_press = False
    while not button_press:
        button_press = plt.waitforbuttonpress(0)
    plt.close()


CLOSE_METHOD_TIMER = 'timer'
CLOSE_METHOD_NO_BLOCK = 'no_block'