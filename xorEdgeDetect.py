import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from segmenting import ImageMatrix


def xorEdgeDetect(map: ImageMatrix):
    if not map.pad:
        map.padArray(1)

    horizontalEdgeArray = xorArrays(map.array[:-1, 1:], map.array[1:, 1:])
    verticalEdgeArray = xorArrays(map.array[1:, :-1], map.array[1:, 1:])

    return ImageMatrix(horizontalEdgeArray | verticalEdgeArray, map.pad)


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

    outputDir = 'bin/output_images/edge_detect/with_pad/'

    image = Image.open(dirname + filename + extension)
    image = ImageOps.invert(image)
    image = image.convert("1")
    imageArray = ImageMatrix(np.pad(np.array(image), (3, 3), 'constant', constant_values=(0, 0)))

    imageEdgeArray = xorEdgeDetect(imageArray)

    spreadImageEdgeArray = ImageMatrix(spreadPoints(imageEdgeArray.array, 2), imageEdgeArray.pad)

    spreadImageEdge = spreadImageEdgeArray.toImage()
    spreadImageEdge.save(outputDir + filename + extension)


    plt.show()




if __name__ == '__main__':
    main()
