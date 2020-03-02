from random import Random

from game.Factory import Factory
from game.Location import Location
from game.Tile import Tile


class Generator:
    @classmethod
    def generate(cls, x, y, level):
        location = cls(x, y, level)
        r = location.publish()
        location.place_mobs(r, [['Shopper', 20 + level, 'b'],
                                ['Hobo', level * 5 - 10, 'b'],
                                ['Shoppest', level * 4 - 20, 'b']])
        return r

    def __init__(self, x, y, level):
        self.random = Random()
        self.level = level
        self.floor = 'b'
        self.display_floor = 'w'
        self.outside_floor = '.'
        self.wall = 'B'
        self.theme = {'D': 'Door', 'W': 'Window', 'E': 'Elevator'}
        self.appliance = ['Bed', 'Sofa', 'Clothing', 'Toilet', 'Sink', 'Kitchen', 'Crate',
                          'Workshop', 'Lamp', 'Cart', 'TV', 'Chair']
        self.loot = ['Drink', 'Food', 'Shovel', 'Pickaxe', 'Airhorn', 'Bat', 'Money']
        self.background = {'!': self.display_floor, 'Van': self.outside_floor}
        self.elevators = level - 1
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
                    r = Factory.make(terrain, location.get_tile(self_x, self_y))
                    if r.name == 'Van':
                        r.tags.set('req', self.level * 3)
                        r.update_display_level()
                    elif r.name == 'K9Alpha':
                        r.tags.increment('L', self.level)
                    elif r.name == 'Elevator':
                        r.tags.increment('L', self.level)
                        r.update_display_level()
                    elif r.name == 'Scanner':
                        r.tags.set('v', self.level - 1)
                else:
                    location.tiles[self_y][self_x].set_terrain(terrain)
        return location

    def run(self):
        estate, garden = self.iterate(6, 1, self.width - 7, 8)
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
        if self.level < 2:
            gate = 'Gate'
        else:
            gate = 'Scanner'
        for x in range(6):
            for y in range(8):
                if x == 5 or y == 7:
                    if x == 3:
                        self.str_map[y][x] = gate
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
                        self.str_map[y][x] = gate
                    else:
                        rand = self.random.randint(1, 16)
                        if rand == 1:
                            self.str_map[y][x] = 'W'
                        else:
                            self.str_map[y][x] = self.wall
                else:
                    self.str_map[y][x] = self.outside_floor
        if self.level == 1:
            self.str_map[2][3] = 'Van'
            self.str_map[6][3] = 'Food'
        else:
            self.str_map[4][3] = 'Van'
        self.str_map[8][3] = 'm'
        self.str_map[3][self.width - 4] = 'E'

    def build_display(self, estate):
        item = self.appliance[self.random.randint(0, len(self.appliance) - 1)]
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
                    if rand == 20 and self.elevators > 0:
                        self.str_map[y][x] = 'E'
                        self.elevators -= 1
                    elif rand == 19:
                        self.str_map[y][x] = 'Register'
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
        door = 'D'
        cx = estate[0] + int((estate[2] - estate[0]) / 2)
        cy = estate[1] + int((estate[3] - estate[1]) / 2)
        buff = self.random.randint(1, 2 + self.level)
        if buff == 1:
            for y in range(estate[1] + 1, estate[3] - 1):
                for x in range(estate[0] + 1, estate[2] - 1):
                    self.str_map[y][x] = self.appliance[self.random.randint(0, len(self.appliance) - 1)]
        elif buff == 2:
            if self.random.randint(0, 1) == 1:
                self.str_map[cy][cx] = 'Drink'
            else:
                self.str_map[cy][cx] = 'Food'
        elif buff == 3:
            self.str_map[cy][cx] = 'Airhorn'
        elif buff == 4:
            if self.random.randint(0, 1) == 1:
                self.str_map[cy][cx] = 'Pickaxe'
            else:
                self.str_map[cy][cx] = 'Shovel'
        elif buff == 5:
            buff_item = self.random.randint(0, 1)
            if buff_item == 1:
                self.str_map[cy][cx] = 'Money'
            else:
                self.str_map[cy][cx] = 'Bat'
        else:
            if self.elevators <= 0:
                for y in range(estate[1] + 1, estate[3] - 1):
                    for x in range(estate[0] + 1, estate[2] - 1):
                        self.str_map[y][x] = 'Crate'
                return
            self.str_map[cy][cx] = 'E'
            self.elevators -= 1
            door = self.display_floor
        for x in range(estate[0], estate[2]):
            wall = self.wall
            if estate[0] < x < estate[2] - 1 and self.random.randint(1, 4) == 1:
                wall = 'W'
            self.str_map[estate[1]][x] = wall
            self.str_map[estate[3] - 1][x] = wall
        for y in range(estate[1], estate[3]):
            wall = self.wall
            if estate[1] < y < estate[3] - 1 and self.random.randint(1, 12) == 1:
                wall = 'W'
            self.str_map[y][estate[0]] = wall
            self.str_map[y][estate[2] - 1] = wall
        door_pos = self.random.randint(1, 4)
        door_ry = self.random.randint(estate[1] + 2, estate[3] - 2)
        door_rx = self.random.randint(estate[0] + 2, estate[2] - 2)
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
            count = mob_data[1]
            tries = mob_data[1] + 5
            while count > 0 and tries > 0:
                x = self.random.randint(1, len(location.tiles[0]) - 2)
                y = self.random.randint(1, len(location.tiles) - 2)
                tile = location.get_tile(x, y)
                if tile.terrain == mob_data[2] and not tile.is_land(Tile.CHECK_SOLID):
                    Factory.make(mob_data[0], tile)
                    count -= 1
                else:
                    tries -= 1
