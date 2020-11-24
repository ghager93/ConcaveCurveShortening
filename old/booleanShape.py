import numpy as np
from PIL import Image
import os


class BooleanShape(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(BooleanShape)
        return obj

    def saveShapeAsBmp(self, fileName):
        img = Image.fromarray(self)
        img = img.convert("L")
        img.save(os.getcwd() + '/lib/shapes/' + fileName + '.bmp')


class Square(BooleanShape):
    def __new__(cls, length):
        return super().__new__(cls, Square.buildMatrix(length))

    def buildMatrix(length):
        return np.full((length, length), False)


class Circle(BooleanShape):
    def __new__(cls, radius):
        return super().__new__(cls, Circle.buildMatrix(radius))

    def buildMatrix(radius):
        arr = np.full((2*radius, 2*radius), True)
        for ix, iy in np.ndindex(arr.shape):
            if np.sqrt((ix-radius)*(ix-radius) + (iy-radius)*(iy-radius)) < radius:
                arr[ix, iy] = 0
        return arr
