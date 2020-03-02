from random import Random

from game import Global
from game.Item import Item
from game.Task import Attack
from game.Turn import Turn
from game.Unit import Unit


class Shopper(Unit):
    def __init__(self, location):
        super().__init__(location)
        self.random = Random()
        self.delay = 0

    def add(self):
        r = super().add()
        Turn.add(1, self.turn)
        return r

    def remove(self):
        Turn.remove(self.turn)
        super().remove()

    def turn(self):
        self.direction = self.random.randint(1, 4)
        self.next_action = self.random.randint(0, 1)
        r = self.action()
        self.update_display_level()
        if self.delay == 0 and not r:
            return True
        return r


class Scanner(Unit):
    def __init__(self, location):
        super().__init__(location)

    def add(self):
        r = super().add()
        Turn.add(1, self.turn)
        return r

    def remove(self):
        Item.remove(self)
        Turn.remove(self.turn)

    def turn(self):
        threshold = self.tags.get('v', 0)
        for i in self.pos.things.copy():
            if i != self and isinstance(i, Unit) and i.weapon and i.weapon.get_level() <= threshold:
                i.weapon.remove()
                i.wield(None)
        return True


class Elevator(Unit):
    def __init__(self, location):
        super().__init__(location)
        self.delay = 0
        self.random = Random()

    def add(self):
        r = super().add()
        Turn.add(1, self.turn)
        return r

    def remove(self):
        Item.remove(self)
        Turn.remove(self.turn)

    def decay(self):
        Item.decay(self)

    def turn(self):
        self.delay += 1
        if self.delay > 99 and self.random.randint(1, 16) == 1:
            from game.Factory import Factory
            level = Global.player.tags.get('R')
            rating = self.random.randint(0, level)
            if rating < 2:
                Factory.make('Cop', self.pos)
            elif rating < 4:
                Factory.make('Dog', self.pos)
            elif rating < 7:
                Factory.make('Agent', self.pos)
            else:
                Factory.make('K9Alpha', self.pos)
            self.delay -= 100
        self.update_display_level()
        return True


class Cop(Shopper):
    def __init__(self, location):
        super().__init__(location)
        self.task = Attack(self)

    def add(self):
        r = super().add()
        self.task.target = Global.player
        return r

    def turn(self):
        self.next_action = 0
        self.task.update()
        self.task.perform()
        r = self.action()
        self.update_display_level()
        if self.delay == 0 and not r:
            return True
        return r
