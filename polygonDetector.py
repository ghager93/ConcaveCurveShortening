import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

from polygonDetection import neighbouringPoints
from segmenting import ImageMatrix
from imageMatrixOps import booleanMatrixToPointList, xorEdgeDetect


def main():
    dirname = 'bin/output_images/small/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'


    image = Image.open(dirname + filename + extension)
    image = ImageOps.invert(image)
    image = image.convert("1")

    map = ImageMatrix(np.array(image))

    edgeDetectedMap = xorEdgeDetect(map)

    # sparseMap = csr_matrix(edgeDetectedMap.array)
    # pointList = [Vector2D(x, y)
    #              for x in range(sparseMap.shape[0])
    #              for y in sparseMap.indices[sparseMap.indptr[x]:sparseMap.indptr[x+1]]]
    pointList = booleanMatrixToPointList(edgeDetectedMap.array)

    polygons = neighbouringPoints(pointList)
    imList = list()
    for polygon in polygons:
        polygonMap = np.full(map.array.shape, False)
        for point in polygon:
            polygonMap[point.x, point.y] = True
        imList.append(plt.imshow(polygonMap))

    plt.show()
    pass
    # print(neighbouringPoints(pointList))
    # sparseImage = np.full(map.array.shape, False)
    # for point in pointList:
    #     sparseImage[point.x, point.y] = True
    #
    # plt.imshow(sparseImage)
    # plt.show()


if __name__ == '__main__':
    main()