from game.Camera import Camera
from game.Space import Space
from game.Tag import Tag


class Prop:
    def __init__(self, location):
        self.location = location
        self.name = None
        self.form = None
        self.form_name = ''
        self.pos = None
        self.vec = Space()
        self.hittable = 1
        self.obstruct_type = None
        self.tags = Tag()
        self.removed = 1
        self.draw_frame = 0

    def draw_synchronize(self):
        from game import Global
        if self.draw_frame != Global.map_view.draw_frame:
            self.update_vec()
            self.draw_frame = Global.map_view.draw_frame
        self.draw_frame += 1

    def add(self):
        if self.removed == 1:
            self.removed = 0
            self.show(True)
            self.relocate(self.pos.x, self.pos.y, force=1)
            self.location.population.append(self)
            return self

    def remove(self):
        if self.removed == 0:
            self.removed = 1
            self.show(False)
            self.location.population.remove(self)
            self.pos.things.remove(self)
            del self

    def show(self, visible):
        self.form.show(visible)

    def bound(self, visible):
        self.form.bound(visible)

    def get_front_tile(self, direction, mag=1, limit=False):
        coord = [[-1, 0], [0, -1], [1, 0], [0, 1]][direction - 1]
        return self.pos.get_neighbor(coord[0] * mag, coord[1] * mag, limit=limit)

    def move_toward(self, direction):
        coord = [[-1, 0], [0, -1], [1, 0], [0, 1]][direction - 1]
        target = self.pos + coord
        from game.Tile import Tile
        if not self.get_front_tile(direction).is_land(Tile.CHECK_SOLID):
            self.relocate(target.x, target.y)
            return True

    def relocate(self, x, y, force=0):
        if self.removed == 0:
            diff = [x - self.pos.x, y - self.pos.y]
            if self in self.pos.things:
                self.pos.things.remove(self)
            new = self.location.get_tile(self.pos.x + diff[0], self.pos.y + diff[1], limit=True)
            new.things.append(self)
            self.pos = new
            if force:
                self.update_vec()

    def update_vec(self):
        self.vec.load(self.pos.get_center())

    def set_form(self, arg):
        from game.Data import Data
        self.form_name = arg
        self.form = Data.get_form(arg)

    def update(self):
        self.draw_synchronize()
        diff = self.pos.get_center() - self.vec
        self.vec += diff * .3
        bound_x, bound_y = Camera.get_relative_pos(self.vec.x, self.vec.y)
        self.form.place(bound_x, bound_y)

    def center_camera(self):
        Camera.target = self

    def get_level(self):
        return self.tags.get('L', 0)

    def decay(self):
        self.tags.increment('L', -1)
        if self.tags.get('L', 0) <= 0:
            self.remove()
