import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from old.segmenting import ImageSpace
from old.imageMatrix import xorEdgeDetect, spreadPoints


def main():
    dirname = 'out/output_images/small/'
    filename = 'afghanistan-silhouette_circle_5_small'
    extension = '.bmp'

    outputDir = 'out/output_images/edge_detect/with_pad/'

    image = Image.open(dirname + filename + extension)
    image = ImageOps.invert(image)
    image = image.convert("1")
    imageArray = ImageSpace(np.pad(np.array(image), (3, 3), 'constant', constant_values=(0, 0)))

    imageEdgeArray = xorEdgeDetect(imageArray)

    spreadImageEdgeArray = ImageSpace(spreadPoints(imageEdgeArray.matrix, 2), imageEdgeArray.pad)

    spreadImageEdge = spreadImageEdgeArray.toImage()
    spreadImageEdge.save(outputDir + filename + extension)


    plt.show()




if __name__ == '__main__':
    main()