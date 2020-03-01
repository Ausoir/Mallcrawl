from game.Tile import Tile


class Actions:
    basic = ['idle', 'left', 'right', 'up', 'down', 'fall', 'walk', 'use', 'attack', 'click']
    priority = ['fall']

    def __init__(self, host):
        self.host = host
        self.humanoid = False
        self.on_finish = None
        self.next_action = None
        self.delay = 1

    def turn(self):
        if self.delay > 0:
            self.delay -= 1
            return True
        else:
            if self.next_action:
                getattr(self, self.next_action)()
                self.next_action = None
            return False

    def idle(self):
        self.delay = 1

    def turn_direction(self, direction):
        self.host.face(direction)

    def left(self):
        if self.host.direction != 1:
            self.turn_direction(1)
        self.walk()

    def up(self):
        if self.host.direction != 2:
            self.turn_direction(2)
        self.walk()

    def right(self):
        if self.host.direction != 3:
            self.turn_direction(3)
        self.walk()

    def down(self):
        if self.host.direction != 4:
            self.turn_direction(4)
        self.walk()

    def walk(self):
        front = self.host.get_front_tile(self.host.direction)
        if front and not front.is_land([Tile.COLLIDE_TERRAIN]):
            if self.attack(front):
                return
            else:
                speed = self.host.tags.get('spd', 0) + 4
                if front.type < 10:
                    speed += front.type
                if speed < 10:
                    if self.host.move_toward(self.host.direction):
                        self.delay = max(1, speed)
                        if not self.grab():
                            self.host.location.play_sound('step')

    def attack(self, front):
        for thing in reversed(front.things):
            level = thing.get_level()
            if level > 0 and thing.tags.get('ob', -1) != Tile.COLLIDE_ITEM:
                self.host.vec += (front - self.host.pos) * 15
                self.host.location.play_sound('hit')
                if thing.get_level() <= self.host.get_level():
                    self.host.decay()
                    thing.remove()
                else:
                    thing.decay()
                    if self.host.weapon:
                        self.host.decay()
                    else:
                        self.host.remove()
                self.delay = 4
                return True

    def fall(self):
        def rise():
            self.host.obstruct_type = t
        t = self.host.obstruct_type
        self.host.obstruct_type = Tile.COLLIDE_ITEM
        self.on_finish = rise
        self.delay = 18

    def grab(self):
        from game.Item import Item
        for thing in reversed(self.host.pos.things):
            if thing != self.host and thing != self.host.weapon and isinstance(thing, Item):
                self.host.location.play_sound('grab')
                self.host.wield(thing)
                self.delay += 4
                return True
