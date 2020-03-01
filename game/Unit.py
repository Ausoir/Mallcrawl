from game.Item import Item


class Unit(Item):
    def __init__(self, location):
        super().__init__(location)
        self.direction = 3
        self.next_action = 0
        self.weapon = None
        self.delay = 1
        self.display_level.color = (40, 40, 40, 200)

    def set_form(self, arg):
        super().set_form(arg)
        self.form.z = 0

    def turn(self):
        if self.weapon:
            if self.weapon.removed == 1:
                self.weapon = None
        r = self.action()
        self.update_display_level()
        return r

    def action(self):
        if self.delay > 0:
            self.delay -= 1
            return True
        else:
            if self.next_action:
                self.walk()
                self.next_action = 0
            return False

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
            return level + self.weapon.get_level()
        else:
            return level

    def relocate(self, x, y, force=0):
        if self.weapon:
            self.weapon.relocate(x, y, force)
        super().relocate(x, y, force)

    def wield(self, weapon):
        if self.weapon:
            self.weapon.display_level.visible = True
        self.weapon = weapon
        if weapon is not None:
            self.weapon.display_level.visible = False

    def decay(self):
        if self.weapon:
            self.weapon.decay()
            if self.weapon.removed:
                self.weapon = None

    def remove(self):
        if self.weapon:
            self.weapon.display_level.visible = True
            self.weapon = None
        from game.Factory import Factory
        dead = Factory.make('Corpse', self.pos)
        self.form.rotation = 90
        dead.form = self.form
        super().remove()
        dead.form.show(True)
        dead.form.bound(False)

    def sound(self, track):
        pass

    def walk(self):
        front = self.get_front_tile(self.direction)
        if front:
            from game.Tile import Tile
            if front.is_land(Tile.CHECK_FIRM) and self.weapon and self.weapon.name == 'Pickaxe':
                for i in front.things.copy():
                    i.remove()
                self.sound('hit')
                front.set_terrain('b')
            elif self.attack(front):
                return
            speed = self.tags.get('spd', 0) + 4
            if front.type < 10:
                speed += front.type
            if speed < 10:
                if self.move_toward(self.direction):
                    self.delay = max(1, speed)
                    if not self.grab():
                        self.sound('step')

    def attack(self, front):
        for thing in reversed(front.things):
            level = thing.get_level()
            if level > 0 and thing.tags.get('ob', 0) != 4:
                self.vec += (front - self.pos) * 15
                self.sound('hit')
                if thing.get_level() <= self.get_level():
                    self.decay()
                    thing.remove()
                else:
                    thing.decay()
                    if self.weapon:
                        self.decay()
                    else:
                        self.remove()
                if self.get_level() <= 0:
                    print('level<0')
                self.delay = 4
                return True

    def grab(self):
        for thing in reversed(self.pos.things):
            if thing != self and thing != self.weapon:
                if thing.obstruct_type == 4:
                    self.sound('grab')
                    self.wield(thing)
                    self.delay *= 2
                    return True
                elif thing.name == 'Van' and self.weapon:
                    thing.supply(self.weapon)
                    self.weapon = None
                    self.update_display_level()
                elif not self.weapon or self.weapon.name != 'Pickaxe':
                    if thing.name == 'Food':
                        self.sound('buff')
                        thing.remove()
                        self.tags.increment('L', 1)
                        self.update_display_level()
                        self.delay *= 2
                        return True
                    elif thing.name == 'Drink':
                        self.sound('buff')
                        thing.remove()
                        self.tags.increment('spd', -1, add=True)
                        self.delay *= 2
                        return True
