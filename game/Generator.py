from random import Random

from game.Factory import Factory
from game.Location import Location
from game.Tile import Tile


class Generator:
    BLOCKED = ['D', 'S', 'X', 'W']

    @classmethod
    def generate(cls, x, y):
        location = cls(x, y)
        r = location.publish()
        location.place_mobs(r, [['Shopper', 20]])
        return r

    def __init__(self, x, y):
        self.random = Random()
        self.floor = 'b'
        self.display_floor = 'w'
        self.outside_floor = '.'
        self.wall = 'B'
        self.theme = {'D': 'Door', 'd': 'Gate', 'W': 'Window', 'E': 'Elevator',
                      '1': 'Bottle', '2': 'Lamp', '3': 'Bed', '4': 'Sofa', '5': 'TV'}
        self.background = {'!': self.display_floor}
        self.divide = 8
        self.thickness = 4
        self.width = x
        self.height = y
        self.str_map = self.make_map(x, y)

    def __str__(self):
        r = []
        for y in self.str_map:
            row = ''
            for x in y:
                if x in self.theme:
                    terrain = self.theme[x]
                    if len(terrain) > 1:
                        row += x
                    else:
                        row += self.theme[x]
                else:
                    row += x
            r.append(row)
        return '\n'.join(r)

    def to_location(self):
        location = Location()
        req_height = max(self.height, len(location.tiles))
        for y in range(req_height):
            if y >= len(location.tiles):
                location.tiles.append([])
            req_width = max(self.width, len(location.tiles[0]))
            for x in range(req_width):
                if x >= len(location.tiles[y]):
                    location.tiles[y].append(Tile(location, '?', x, y))
        for self_y in range(self.height):
            for self_x in range(self.width):
                terrain = self.theme.get(self.str_map[self_y][self_x])
                if not terrain:
                    terrain = self.str_map[self_y][self_x]
                if len(terrain) > 1:
                    background = self.background.get(terrain)
                    if not background:
                        background = self.background['!']
                    location.tiles[self_y][self_x].set_terrain(background)
                    Factory.make(terrain, location.get_tile(self_x, self_y))
                else:
                    location.tiles[self_y][self_x].set_terrain(terrain)
        return location

    def run(self):
        estate, garden = self.iterate(6, 0, self.width - 7, 8)
        estate2, garden2 = self.iterate(0, 10, self.width, self.height)
        self.build_entrance()
        for rect in garden + estate + garden2 + estate2:
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            buildable = [rect[0], rect[1], rect[2] - 1, rect[3] - 1]
            if 4 < width < 10 and 4 < height < 10:
                self.build_pillar(buildable)
            elif 2 < width and 2 < height:
                self.build_display(buildable)
            else:
                self.build_isle(buildable)

    def iterate(self, px, py, px2, py2):
        estate = []
        garden = []
        ratio = self.random.random() * .8 + .1
        new_height = (py2 - py) * ratio
        new_height_iv = (py2 - py) * (1 - ratio)
        new_width = (px2 - px) * ratio
        new_width_iv = (px2 - px) * (1 - ratio)
        if max(new_width, new_width_iv) > max(new_height, new_height_iv):
            area = [px, py, px + new_width, py2]
            area2 = [px + new_width, py, px + new_width + new_width_iv, py2]
            if new_width > self.thickness:
                new_estate, new_garden = self.iterate(area[0], area[1], area[2], area[3])
                if not new_estate:
                    estate.append([int(x) for x in area])
                else:
                    estate += new_estate
                    garden += new_garden
            else:
                garden.append([int(x) for x in area])
            if new_width_iv > self.thickness:
                new_estate, new_garden = self.iterate(area2[0], area2[1], area2[2], area2[3])
                if not new_estate:
                    estate.append([int(x) for x in area2])
                else:
                    estate += new_estate
                    garden += new_garden
            else:
                garden.append([int(x) for x in area2])
        else:
            area = [px, py, px2, py + new_height]
            area2 = [px, py + new_height, px2, py + new_height + new_height_iv]
            if new_height > self.thickness:
                new_estate, new_garden = self.iterate(area[0], area[1], area[2], area[3])
                if not new_estate:
                    estate.append([int(x) for x in area])
                else:
                    estate += new_estate
                    garden += new_garden
            else:
                garden.append([int(x) for x in area])
            if new_height_iv > self.thickness:
                new_estate, new_garden = self.iterate(area2[0], area2[1], area2[2], area2[3])
                if not new_estate:
                    estate.append([int(x) for x in area2])
                else:
                    estate += new_estate
                    garden += new_garden
            else:
                garden.append([int(x) for x in area2])
        return estate, garden

    def build_entrance(self):
        for x in range(6):
            for y in range(8):
                if x == 5 or y == 7:
                    if x == 3:
                        self.str_map[y][x] = 'd'
                    else:
                        rand = self.random.randint(1, 16)
                        if rand == 1:
                            self.str_map[y][x] = 'W'
                        else:
                            self.str_map[y][x] = self.wall
                else:
                    self.str_map[y][x] = self.outside_floor
        for x in range(self.width - 6, self.width):
            for y in range(8):
                if x == self.width - 6 or y == 7:
                    if x == self.width - 4:
                        self.str_map[y][x] = 'd'
                    else:
                        rand = self.random.randint(1, 16)
                        if rand == 1:
                            self.str_map[y][x] = 'W'
                        else:
                            self.str_map[y][x] = self.wall
                else:
                    self.str_map[y][x] = self.outside_floor
        self.str_map[3][self.width - 4] = 'E'

    def build_display(self, estate):
        item = str(self.random.randint(1, 5))
        for y in range(estate[1], estate[3]):
            for x in range(estate[0], estate[2]):
                if x == estate[0] or x == estate[2] - 1 or y == estate[1] or y == estate[3] - 1:
                    rand = self.random.randint(1, 3)
                    if rand != 1:
                        self.str_map[y][x] = item
                    else:
                        self.str_map[y][x] = self.display_floor
                else:
                    self.str_map[y][x] = self.wall

    def build_isle(self, estate):
        for y in range(estate[1], estate[3]):
            for x in range(estate[0], estate[2]):
                if x == estate[0] or x == estate[2] - 1 or y == estate[1] or y == estate[3] - 1:
                    rand = self.random.randint(0, 30)
                    if rand == 30:
                        self.str_map[y][x] = 'E'
                    elif rand % 2 == 0:
                        self.str_map[y][x] = ':'
                    else:
                        self.str_map[y][x] = ';'
                else:
                    self.str_map[y][x] = 'C'

    def build_pillar(self, estate):
        for y in range(estate[1] + 1, estate[3] - 1):
            for x in range(estate[0] + 1, estate[2] - 1):
                self.str_map[y][x] = 'w'
        for x in range(estate[0], estate[2]):
            self.str_map[estate[1]][x] = self.wall
            self.str_map[estate[3] - 1][x] = self.wall
        for y in range(estate[1], estate[3]):
            self.str_map[y][estate[0]] = self.wall
            self.str_map[y][estate[2] - 1] = self.wall
        door_pos = self.random.randint(1, 4)
        door_ry = self.random.randint(estate[1] + 2, estate[3] - 2)
        door_rx = self.random.randint(estate[0] + 2, estate[2] - 2)
        door = 'D'
        if self.random.randint(1, 2) == 1:
            x = estate[0] + int((estate[2] - estate[0]) / 2)
            y = estate[1] + int((estate[3] - estate[1]) / 2)
            self.str_map[y][x] = 'E'
            door = self.display_floor
        if door_pos == 1:
            self.str_map[door_ry][estate[0]] = door
        elif door_pos == 2:
            self.str_map[estate[1]][door_rx] = door
        elif door_pos == 3:
            self.str_map[door_ry][estate[2] - 1] = door
        elif door_pos == 4:
            self.str_map[estate[3] - 1][door_rx] = door

    def get_volume(self, arg):
        return (arg[2] - arg[0]) * (arg[3] - arg[1])

    def publish(self):
        self.run()
        return self.to_location()

    def make_map(self, size_x, size_y):
        r = []
        for y in range(size_y):
            row = []
            for x in range(size_x):
                row.append(self.floor)
            r.append(row)
        return r

    def flip(self, flip_x, flip_y):
        if flip_y:
            self.str_map.reverse()
        if flip_x:
            r = []
            for y in self.str_map:
                r.append(y[::-1])
            self.str_map = r

    def place_mobs(self, location, mobs):
        for mob_data in mobs:
            for i in range(mob_data[1]):
                x = self.random.randint(1, len(location.tiles[0]) - 2)
                y = self.random.randint(1, len(location.tiles) - 2)
                tile = location.get_tile(x, y)
                if not tile.is_land(Tile.CHECK_SOLID):
                    Factory.make(mob_data[0], tile)
