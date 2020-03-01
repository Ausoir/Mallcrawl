import math
from pyglet.media import Player

from game import Global
from game.Tile import Tile


class Location:
    def __init__(self):
        self.identity = 0
        self.update_frame = 0
        self.population = []
        self.delay = 8
        self.tiles = [[Tile(self, '.', 0, 0)]]
        self.header = None
        self.track = Player()
        self.spawn = 0

    def play_sound(self, sound):
        from game.Data import Data
        self.track.queue(Data.get_track(sound))
        if self.track.playing:
            self.track.next_source()
        else:
            self.track.pause()
        self.track.play()

    def get_tile(self, x, y, limit=False):
        if self.is_inbound(x, y):
            return self.tiles[y][x]
        elif limit:
            x = max(0, min(len(self.tiles[0]) - 1, x))
            y = max(0, min(len(self.tiles) - 1, y))
            return self.tiles[y][x]

    def is_inbound(self, x, y):
        return 0 <= x < len(self.tiles[0]) and 0 <= y < len(self.tiles)

    def get_tile_from_vec(self, x, y):
        x = math.floor(x / Global.BLOCK)
        y = math.floor(y / Global.BLOCK)
        return self.get_tile(x, y, limit=True)

    def flip(self, flip_x, flip_y):
        if flip_y:
            self.tiles.reverse()
        if flip_x:
            r = []
            for y in self.tiles:
                r.append(y[::-1])
            self.tiles = r
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                self.tiles[y][x].x = x
                self.tiles[y][x].y = y
                for thing in self.tiles[y][x].things:
                    thing.update_vec()

    def rotate(self):
        copy = []
        for x in self.tiles[0]:
            copy.append([None] * len(self.tiles))
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                copy[x][y] = self.tiles[y][x]
        self.tiles = copy
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[0])):
                self.tiles[y][x].x = x
                self.tiles[y][x].y = y
                for thing in self.tiles[y][x].things:
                    thing.update_vec()

    def stretch(self, new_x, new_y):
        for y in range(new_y):
            if y >= len(self.tiles):
                self.tiles.append([])
            for x in range(new_x):
                if x >= len(self.tiles[y]):
                    self.tiles[y].append(Tile(self, '?', x, y))

    def collide_land(self, pos1, pos2, flag=Tile.CHECK_SOLID, distance=10):
        degree = math.atan2(pos2.y - pos1.y, pos2.x - pos1.x)
        current = [pos1.x * Global.BLOCK + Global.HALF_BLOCK, pos1.y * Global.BLOCK + Global.HALF_BLOCK]
        prev_tile = self.get_tile(pos1.x, pos1.y, limit=True)
        while distance > 0 and (prev_tile.x != pos2.x or prev_tile.y != pos2.y):
            distance -= 1
            dx = math.cos(degree) * Global.BLOCK
            dy = math.sin(degree) * Global.BLOCK
            current[0] = current[0] + dx
            current[1] = current[1] + dy
            tile = self.get_tile_from_vec(current[0], current[1])
            if tile and tile.is_land(flag):
                return tile
            prev_tile = tile
        return prev_tile
