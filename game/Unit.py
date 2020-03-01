from game.Actions import Actions
from game.Item import Item


class Unit(Item):
    def __init__(self, location):
        super().__init__(location)
        self.draw_frame = 0
        self.action = Actions(self)
        self.direction = 3
        self.next_action = 'idle'
        self.weapon = None

    def input(self, action):
        self.action.next_action = action

    def turn(self):
        if self.weapon:
            if self.weapon.removed == 1:
                self.weapon = None
                self.update_display_level()
        return self.action.turn()

    def face(self, direction):
        self.direction = direction

    def face_toward(self, pos):
        diff = pos - self.pos
        horizontal = abs(diff.x) >= abs(diff.y)
        if horizontal:
            if diff.x < 0:
                self.direction = 1
            else:
                self.direction = 3
        else:
            if diff.y < 0:
                self.direction = 2
            else:
                self.direction = 4

    def get_level(self):
        level = super().get_level()
        if self.weapon:
            return level + self.weapon.level
        else:
            return level

    def relocate(self, x, y, force=0):
        super().relocate(x, y, force)
        if self.weapon:
            self.weapon.relocate(x, y, force)

    def wield(self, weapon):
        if self.weapon:
            self.weapon.display_level.visible = True
        if weapon is not None:
            self.weapon = weapon
            self.weapon.display_level.visible = False
        self.update_display_level()

    def decay(self):
        if self.weapon:
            self.weapon.decay()

    def remove(self):
        if self.weapon:
            self.weapon.display_level.visible = True
            self.weapon = None
        from game.Factory import Factory
        Factory.make('Corpse', self.pos)
        super().remove()

    def update(self):
        self.draw_synchronize()
        super().update()

    def draw_synchronize(self):
        from game import Global
        if self.draw_frame != Global.map_view.draw_frame:
            self.update_vec()
            self.draw_frame = Global.map_view.draw_frame
        self.draw_frame += 1
