from random import Random

from game import Global
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
        self.action.next_action = ('idle', 'left', 'up', 'right', 'down')[self.random.randint(0, 4)]
        r = self.action.turn()
        if self.action.delay == 0 and not r:
            return True
        return r


class Elevator(Shopper):
    def __init__(self, location):
        super().__init__(location)
        self.delay = 0

    def add(self):
        r = super().add()
        Turn.add(1, self.turn)
        return r

    def remove(self):
        Turn.remove(self.turn)
        super().remove()

    def turn(self):
        if self.delay > 0:
            self.delay -= 1
        elif self.location.spawn >= 1 and self.random.randint(1, 16) == 1:
            self.location.spawn -= 1
            from game.Factory import Factory
            Factory.make('Cop', self.pos)
            self.delay = 40
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
        self.action.next_action = 'idle'
        self.task.update()
        self.task.perform()
        r = self.action.turn()
        if self.action.delay == 0 and not r:
            return True
        return r
