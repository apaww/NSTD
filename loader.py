from settings import *
from levels.config import *
import json


class Board:
    def __init__(self, level):
        self.level = level
        self.board = [[[0] for __ in range(COLS)] for _ in range(ROWS)]
        self.cell_size = TILE_SIZE

    def load(self):
        with open(f'./levels/{self.level}/level.json', mode='r') as f:
            level_data = json.load(f)
        self.level_data = level_data

        default = [0, 0]
        waypoint_data = []

        for layer in self.level_data['layers']:
            if layer['type'] == 'tilelayer':
                self.tile_map = layer['data']
            elif layer['name'] == 'waypoints':
                for point in layer['objects']:
                    waypoint_data = point['polyline']
                    default = [point.get('x'), point.get('y')]

        self.waypoints = [(waypoint.get('x') + default[0], waypoint.get('y') + default[1])
                          for waypoint in waypoint_data]

    def fill_board(self):
        for i in range(COLS):
            for j in range(ROWS):
                if self.tile_map[(j * COLS) + i] in EMPTY[self.level - 1]:
                    self.board[j][i][0] = 1

    def check(self, tile):
        return self.board[tile[1]][tile[0]][0] and len(self.board[tile[1]][tile[0]]) == 1

    def get_waypoints(self):
        return self.waypoints

    def take_tile(self, tile):
        self.board[tile[1]][tile[0]].append(0)

    def get_board(self):
        return self.board
