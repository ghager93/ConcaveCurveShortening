from collections import namedtuple
from math import hypot, sqrt


class Vector2D(namedtuple('Vector2D', ('x', 'y'))):
    EUCLIDEAN = 0
    QUASI_EUCLIDEAN = 1
    MANHATTAN = 2
    CHESS = 3

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __int__(self):
        return type(self)(int(self.x), int(self.y))

    def __add__(self, other):
        other = self._convert_other(other)
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other = self._convert_other(other)
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        other = self._convert_other(other)
        return type(self)(self.x * other.x, self.y * other.y)

    def dot(self, other):
        other = self._convert_other(other)
        return self.x * other.x + self.y * other.y

    def distance_to(self, other, metric='euclidean'):
        other = self._convert_other(other)
        if metric == 'euclidean':
            return hypot((self.x - other.x), (self.y - other.y))
        if metric == 'quasi-euclidean':
            abs_x = abs(self.x - other.x)
            abs_y = abs(self.y - other.y)
            return max(abs_x, abs_y) + (sqrt(2) - 1)*min(abs_x, abs_y)
        if metric == 'manhattan':
            return abs(self.x - other.x) + abs(self.y - other.y)
        if metric == 'chess':
            return max(abs(self.x - other.x), abs(self.y - other.y))

    def manhattan_distance_to(self, other):
        other = self._convert_other(other)
        return abs(self.x - other.x) + abs(self.y - other.y)

    @staticmethod
    def _convert_other(other):
        if type(other) is tuple and len(other) == 2:
            return Vector2D(other[0], other[1])
        return other
