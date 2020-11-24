from collections import namedtuple
from math import hypot

class Vector2D(namedtuple('Vector2D', ('x', 'y'))):
    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y))

    def __int__(self):
        return type(self)(int(self.x), int(self.y))

    def __add__(self, other):
        if type(other) is tuple and len(other) == 2:
            return type(self)(self.x + other[0], self.y + other[1])
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return type(self)(self.x * other.x, self.y * other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distanceTo(self, other):
        return hypot((self.x - other.x), (self.y - other.y))

    def manhattanDistanceTo(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)