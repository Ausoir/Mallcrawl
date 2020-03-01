from game.Camera import Camera
from game.Prop import Prop
from game.Textbox import Textbox


class Item(Prop):
    def __init__(self, location):
        super().__init__(location)
        self.display_level = Textbox()

    def add(self):
        r = super().add()
        self.display_level.add_batch()
        self.update_display_level()
        return r

    def remove(self):
        self.display_level.remove_batch()
        super().remove()

    def bound(self, visible):
        super().bound(visible)
        self.display_level.bound(visible)

    def update_display_level(self):
        level = self.get_level()
        if level > 0:
            self.display_level.set(str(level))

    def update(self):
        diff = self.pos.get_center() - self.vec
        self.vec += diff * .2
        bound_x, bound_y = Camera.get_relative_pos(self.vec.x, self.vec.y)
        self.form.place(bound_x, bound_y)
        self.display_level.update(bound_x + 15, bound_y + 25)

    def decay(self):
        super().decay()
        self.update_display_level()
