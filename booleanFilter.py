import booleanShape
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


class MapArray:
    def __init__(self, array: np.ndarray = None, pad: int = 0):
        self.array = array
        self.pad = pad

    def toImage(self):
        return Image.fromarray(self.unpadArray()).convert("L")

    def unpadArray(self):
        return self.array[self.pad:-self.pad, self.pad:-self.pad] if self.pad else self.array

    def padArray(self, newPad):
        self.array = np.pad(self.unpadArray(), (newPad, newPad), 'constant', constant_values=(0, 0))
        self.pad = newPad

    def paddedIterationShape(self):
        return self.array.shape[0]-self.pad, self.array.shape[1]-self.pad

    def asBoolean(self):
        return self.array > 0

    def show(self):
        plt.imshow(self.array)
        plt.show()

    def asRatioOf(self, array2):
        return self.countFalse() / array2.countFalse()

    def countFalse(self):
        return self.unpadArray().size - np.count_nonzero(self.unpadArray())


class BooleanFilter:
    def __init__(self, filterType: str = 'circle', dimension: int = 10):
        if filterType == 'circle':
            self.filter = booleanShape.Circle(dimension)
        elif filterType == 'square':
            self.filter = booleanShape.Square(dimension)
        else:
            self.filter = booleanShape.Circle(dimension)

    def applyToArray(self, mapArray: MapArray):
        mapArray.padArray(self.filter.shape[0])
        booleanArray = mapArray.asBoolean()
        filteredArray = self.createFullPaddedBooleanArray(booleanArray.shape)
        for ix, iy in np.ndindex(mapArray.paddedIterationShape()):
            if self.isSubtractive(booleanArray[ix:ix + self.filter.shape[0], iy:iy + self.filter.shape[1]]):
                self.subtractFilter(filteredArray[ix:ix + self.filter.shape[0], iy:iy + self.filter.shape[1]])

        return MapArray(filteredArray, self.filter.shape[0])

    def createFullPaddedBooleanArray(self, shape):
        return np.full(shape, True)

    def isSubtractive(self, imageBlock: np.ndarray) -> bool:
        return np.array_equal(self.filter, imageBlock | self.filter)

    def subtractFilter(self, imageBlock: np.ndarray):
        imageBlock &= self.filter


def main():
    dirname = 'lib/silhouettes/'
    filename = 'afghanistan-silhouette'
    extension = '.bmp'
    filteredDirname = 'bin/output_images/'
    filterType = 'circle'
    dimension = 5

    image = Image.open(dirname + filename + extension)
    image = image.convert("1")
    image = image.resize((image.size[0]//10, image.size[1]//10))

    imageArray = MapArray(np.array(image))
    imageArray.padArray(dimension)

    booleanFilter = BooleanFilter(filterType, dimension)

    filteredImageArray = booleanFilter.applyToArray(imageArray)

    filteredImage = filteredImageArray.toImage()
    filteredImage.save(filteredDirname + 'small/' + filename + '_' + filterType + '_' + str(dimension)
                       + '_' + 'small' + extension)
    filteredImage = filteredImage.resize((image.size[0]*10, image.size[1]*10))
    filteredImage.save(filteredDirname + filename + '_' + filterType + '_' + str(dimension) + extension)

    # circleFilter = BooleanFilter('circle', dimension)
    # circleFilteredImageArray = circleFilter.applyToArray(imageArray)
    #
    # print('square ratio:', filteredImageArray.asRatioOf(imageArray))
    # print('circle ratio:', circleFilteredImageArray.asRatioOf(imageArray))


if __name__ == '__main__':
    main()