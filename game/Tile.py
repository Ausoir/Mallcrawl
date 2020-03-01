from game import Global
from game.Space import Space


class Tile(Space):
    CHECK_NONE = []
    CHECK_ANY = [1, 2, 3, 4, 5, 6]
    CHECK_FIRM = [1, 2, 5]
    CHECK_SOLID = [1, 2, 3, 5]
    CHECK_SIGHT = [1, 2, 6]
    COLLIDE_TERRAIN = 1
    COLLIDE_OBJECT = 2
    COLLIDE_UNIT = 3
    COLLIDE_ITEM = 4
    COLLIDE_WINDOW = 5
    COLLIDE_FOG = 6
    DICTIONARY = {'.': ['dirt', 'g_1x0', 0],
                  ',': ['grass', 'g_2x0', 1],
                  'B': ['brick', 'g_3x0', 10],
                  'b': ['floor', 'g_11x0', 0],
                  'w': ['wood', 'g_4x0', 0],
                  'm': ['mat', 'g_0x1', 0],
                  'C': ['crate', 'g_2x1', 10],
                  ':': ['shelf', 'g_5x0', 11],
                  ';': ['shelf2', 'g_2x0', 10]
                  }

    def __init__(self, location, terrain, x, y):
        super().__init__(x, y)
        self.location = location
        self.terrain = terrain
        data = Tile.DICTIONARY.get(terrain)
        if data:
            self.name = data[0]
            self.image = data[1]
            self.type = data[2]
        else:
            self.name = 'None'
            self.image = 'g_0x0'
            self.type = 10
        self.direction = 0
        self.things = []
        self.light = 0

    @staticmethod
    def get_collision_by_name(num):
        if num == Tile.COLLIDE_TERRAIN:
            return 'Terrain'
        elif num == Tile.COLLIDE_OBJECT:
            return 'Object'
        elif num == Tile.COLLIDE_UNIT:
            return 'Unit'
        elif num == Tile.COLLIDE_ITEM:
            return 'Item'
        elif num == Tile.COLLIDE_WINDOW:
            return 'Window'
        elif num == Tile.COLLIDE_FOG:
            return 'Fog'

    def set_terrain(self, terrain):
        data = Tile.DICTIONARY.get(terrain)
        if data:
            self.terrain = terrain
            self.name = data[0]
            self.image = data[1]
            self.type = data[2]
            self.direction = 0
            return True

    def get_image(self):
        return self.image

    def get_depth(self):
        if self.terrain:
            if self.type == 10:
                return 2
            return 1
        return 0

    def get_neighbor(self, x, y, limit=False):
        return self.location.get_tile(self.x + x, self.y + y, limit=limit)

    def get_vec(self):
        return self * Global.BLOCK

    def get_center(self):
        return self.get_vec() + Global.HALF_BLOCK

    def get_bottom(self):
        return self + [Global.HALF_BLOCK, Global.BLOCK]

    def is_land(self, check):
        if self.type == 10 and Tile.COLLIDE_TERRAIN in check:
            return 1
        elif self.type == 11 and Tile.COLLIDE_WINDOW in check:
            return 1
        for i in self.things:
            if i.obstruct_type in check:
                return 1
        return 0
