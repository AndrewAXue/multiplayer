from collections import namedtuple

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return Coordinate(self.x, self.y)

class Player:
    def __init__(self, coord, height, width, color):
        self.coord = coord
        self.height = height
        self.width = width
        self.color = color
AIR = 0
SOLID = 1
DEATH = 2
PLAYER = 3
