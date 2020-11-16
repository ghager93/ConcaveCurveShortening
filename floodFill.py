from unittest import TestCase
from Vector2D import Vector2D
from LoopSegment import LoopSegment
from PIL import Image, ImageOps
import ImageSegmenter
from segmenting import ImageSpace
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time
import cv2
from collections import namedtuple


dirname = 'out/output_images/edge_detect/with_pad/'
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


class _FloodFillObject:
    def __init__(self, matrix: np.ndarray):
        _assert_matrix_is_2d(matrix)

        self.matrix = matrix
        self.visited = set()
        self.stack = list()

    def get_polygons(self):
        polygons = list()
        self.visited = set()
        for ix, iy in np.ndindex(self.matrix):
            start = Vector2D(ix, iy)
            if self.is_unvisited(start):
                polygons.append(Polygon(self.get_points_in_polygon_by_dfs(start)))

        return polygons

    def get_points_in_polygon_by_dfs(self, start: Vector2D):
        points = list()
        self.stack = list()
        self.add_point_to_stack_and_visited_if_legal_and_unvisited(start)
        while stack:
            curr = self.stack.pop()
            points.append(curr)
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (1, 0))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (-1, 0))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (0, 1))
            self.add_point_to_stack_and_visited_if_legal_and_unvisited(curr + (0, -1))

        return points

    def is_unvisited(self, point: Vector2D):
        return point not in self.visited

    def is_in_matrix(self, point: Vector2D):
        return 0 <= point.x < self.matrix.shape[0] and \
               0 <= point.y < self.matrix.shape[1]

    def is_non_zero(self, point: Vector2D):
        return self.matrix[point]

    def is_legal(self, point, Vector2D):
        return self.is_in_matrix(point) and self.is_non_zero(point)

    def add_point_to_stack_and_visited_if_legal_and_unvisited(self, point: Vector2D):
        if  self.is_legal(point) and self.is_unvisited(point):
            self.visited.add(point)
            self.stack.append(point)


class PolygonBoundary(namedtuple('PolygonBoundary', ('xmin', 'ymin', 'xmax', 'ymax'))):
    def upper_left(self):
        return Vector2D(self.xmin, self.ymin)

    def lower_right(self):
        return Vector2D(self.xmax, self.ymax)

    def width(self):
        return self.xmax - self.xmin

    def height(self):
        return self.ymax - self.ymin

    def shape(self):
        return self.width(), self.height()

    def size(self):
        return self.width() * self.height()


class Polygon(PolygonBoundary):
    def __init__(self, points):
        self.points = points
        self.xmin = self._find_xmin()
        self.xmax = self._find_xmax()
        self.ymin = self._find_ymin()
        self.ymax = self._find_ymax()

    def as_array(self):
        array = np.zeros(self.shape())
        for point in self.points:
            array[point - self.upper_left()] = 1

        return array

    def _find_xmin(self):
        return min([p[0] for p in self.points])

    def _find_xmax(self):
        return max([p[0] for p in self.points])

    def _find_ymin(self):
        return min([p[1] for p in self.points])

    def _find_ymax(self):
        return max([p[1] for p in self.points])


def flood_fill(matrix: np.ndarray):
    _assert_matrix_is_2d(matrix)

    polygons = _FloodFillObject(matrix).get_polygons()


def colour_matrix_with_single_value(matrix, polygons):
    coloured_matrix = np.zeros(matrix.shape)
    for i, polygon in enumerate(polygons):
        rows, cols = zip(*polygon.points)
        coloured_matrix[rows, cols] = i/len(polygons)

    return coloured_matrix

def colour_matrix_with_rgb(matrix, polygons):
    coloured_matrix = np.zeros(matrix.shape)
    for i, polygon in enumerate(polygons):



def _assert_matrix_is_2d(matrix: np.ndarray):
    assert len(matrix.shape) == 2
