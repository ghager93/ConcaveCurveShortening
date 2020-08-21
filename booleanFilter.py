import booleanShape
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


class MapArray:
    def __init__(self, array: np.ndarray = None):
        self.array = array

    def toImage(self):
        return Image.fromarray(self.array).convert("L")

    def asBoolean(self):
        return self.array > 0

    def show(self):
        plt.imshow(self.array)
        plt.show()

    def asRatioOf(self, array2):
        return self.countFalse() / array2.countFalse()

    def countFalse(self):
        return self.array.size - np.count_nonzero(self.array)


class PaddedMapArray(MapArray):
    def __init__(self, array: np.ndarray = None, pad: int = 0):
        super().__init__(array)
        self.pad = pad

    def __init__(self, mapArray: MapArray, pad: int = 0):
        super().__init__(MapArray.array)
        self.pad = pad

    def paddedArray(self):
        return np.pad(self.array, (self.pad, self.pad), 'constant', constant_values=(0, 0))

    def paddedBooleanArray(self):
        return self.paddedArray() > 0


class BooleanFilter:
    def __init__(self, filterType: str = 'circle', dimension: int = 10):
        if filterType == 'circle':
            self.filter = booleanShape.Circle(dimension)
        elif filterType == 'square':
            self.filter = booleanShape.Square(dimension)
        else:
            self.filter = booleanShape.Circle(dimension)

    def applyToArray(self, mapArray: MapArray):
        paddedMapArray = PaddedMapArray(mapArray, self.filter.shape[0])
        booleanArray = paddedMapArray.paddedBooleanArray()
        filteredArray = np.full(booleanArray.shape, True)
        for ix, iy in np.ndindex(paddedMapArray.array.shape):
            if self.isSubtractive(booleanArray[ix:ix + self.filter.shape[0], iy:iy + self.filter.shape[1]]):
                self.subtractFilter(filteredArray[ix:ix + self.filter.shape[0], iy:iy + self.filter.shape[1]])

        return PaddedMapArray(filteredArray, self.filter.shape[0])

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