from unittest import TestCase
from Vector2D import Vector2D
from LoopSegment import LoopSegment
from PIL import Image, ImageOps
import ImageSegmenter
from segmenting import ImageMatrix
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time
import cv2


dirname = 'bin/output_images/edge_detect/with_pad/'
filename = 'afghanistan-silhouette_circle_5_small'
extension = '.bmp'

image = Image.open(dirname + filename + extension)
# image = ImageOps.invert(image)
image = image.convert("1")

map = np.array(image)

loops = list()
visited = set()
stack = list()

for ix, iy in np.ndindex(map.shape):
    if map[ix, iy] and Vector2D(ix, iy) not in visited:
        loop = list()
        curr = Vector2D(ix, iy)
        stack.append(curr)
        visited.add(curr)
        while stack:
            curr = stack.pop()
            loop.append(curr)
            if curr.x < map.shape[0]-1 and map[curr.x+1, curr.y] and Vector2D(curr.x+1, curr.y) not in visited:
                stack.append(Vector2D(curr.x+1, curr.y))
                visited.add(Vector2D(curr.x+1, curr.y))
            if curr.y < map.shape[1]-1 and map[curr.x, curr.y+1] and Vector2D(curr.x, curr.y+1) not in visited:
                stack.append(Vector2D(curr.x, curr.y+1))
                visited.add(Vector2D(curr.x, curr.y+1))
            if curr.x > 0 and map[curr.x-1, curr.y] and Vector2D(curr.x-1, curr.y) not in visited:
                stack.append(Vector2D(curr.x-1, curr.y))
                visited.add(Vector2D(curr.x-1, curr.y))
            if curr.y > 0 and map[curr.x, curr.y-1] and Vector2D(curr.x, curr.y-1) not in visited:
                stack.append(Vector2D(curr.x, curr.y-1))
                visited.add(Vector2D(curr.x, curr.y-1))
        loops.append(loop)

map = map.astype(int)

for loop in loops:
    loopScreen = np.zeros(map.shape, np.int8)
    for p in loop:
        loopScreen[p.x, p.y] += 2

    map += loopScreen
    plt.imshow(map)
    plt.show()
    map -= loopScreen
