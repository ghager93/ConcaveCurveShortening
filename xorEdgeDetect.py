import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from booleanFilter import MapArray


def xorEdgeDetect(map: MapArray):
    if not map.pad:
        map.padArray(1)

    horizontalEdgeArray = xorArrays(map.array[:-1, 1:], map.array[1:, 1:])
    verticalEdgeArray = xorArrays(map.array[1:, :-1], map.array[1:, 1:])

    return MapArray(horizontalEdgeArray | verticalEdgeArray, map.pad)


def xorArrays(array1: np.ndarray, array2: np.ndarray):
    return array1 ^ array2


def spreadPoints(array: np.ndarray, spread: int):
    convolvedArray = np.copy(array)
    for ix in range(array.shape[0]-spread):
        convolvedArray[ix, :] = np.convolve(convolvedArray[ix, :-spread+1], np.full(spread, True))

    for iy in range(array.shape[1]-spread):
        convolvedArray[:, iy] = np.convolve(convolvedArray[:-spread+1, iy], np.full(spread, True))

    return convolvedArray


def main():
    dirname = 'bin/output_images/small/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'

    outputDir = 'bin/output_images/edge_detect/'

    image = Image.open(dirname + filename + extension)
    image = ImageOps.invert(image)
    image = image.convert("1")

    imageArray = MapArray(np.array(image))

    imageEdgeArray = xorEdgeDetect(imageArray)

    spreadImageEdgeArray = MapArray(spreadPoints(imageEdgeArray.array, 2), imageEdgeArray.pad)

    spreadImageEdge = spreadImageEdgeArray.toImage()
    spreadImageEdge.save(outputDir + filename + extension)


    plt.show()




if __name__ == '__main__':
    main()
