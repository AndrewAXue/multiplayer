import json
from map.graphics import *
from basic_vars.vars import *


class Map:
    def __init__(self, map_name: str):
        '''
        Used for drawing STATIC things and for interactions between things
        Drawing entities should be a different thing
        :param map_name: 
        '''
        json_data = None
        try:
            with open(f'map/data/{map_name}', 'r') as f:
                json_data = json.load(f)
        except:
            print(f'Problem loading data/{map_name}, check if it exists')
        self._map_name = json_data['map_name']
        self._length = json_data['length']
        self._height = json_data['height']
        self._stage = json_data['stage']
        self._spawn_point = Coordinate(json_data['spawn_x'], json_data['spawn_y'])
        self._colour_map = {
            AIR: 'white',
            SOLID: 'green',
            DEATH: 'red',
            PLAYER: 'blue'
            # Player's color is decided elsewhere. The blue is a place holder.
        }

    @property
    def length(self):
        return self._length

    @property
    def height(self):
        return self._height

    @property
    def map_name(self):
        return self._map_name

    @property
    def spawn_point(self):
        return self._spawn_point

    def draw_line(self, x1, x2, y, color: str, win):
        line = Line(Point(x1, y), Point(x2, y))
        line.setFill(color)
        line.draw(win)

    def draw_stage(self, win: GraphWin):
        for y in range(self._height):
            prev_x = 0
            prev_col = self._stage[y][0]
            for x in range(self._length):
                if self._stage[y][x] != prev_col:
                    self.draw_line(prev_x, x - 1, y, self._colour_map[self._stage[y][x - 1]], win)
                    prev_x = x
                    prev_col = self._stage[y][x]
            self.draw_line(prev_x, self._length, y, self._colour_map[self._stage[y][self._length - 1]], win)

    def spawn_player(self, player: Player):
        for i in range(player.height):
            for j in range(player.width):
                self._stage[self._spawn_point.y + i][self._spawn_point.x + j] = PLAYER
