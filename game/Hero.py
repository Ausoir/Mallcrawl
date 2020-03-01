from game import Global
from game.Item import Item
from game.Unit import Unit


class Hero(Unit):
    def remove(self):
        if self.removed == 0:
            self.removed = 1
            self.form.rotation = 90

    def update(self):
        Item.update(self)

    def turn(self):
        if self.location.mode > 70:
            if self.removed:
                super().remove()
            else:
                self.wield(None)
                self.tags.increment('R', 1)
            Global.main.end = True
        elif self.location.mode > 0:
            self.location.mode += 1
        else:
            if self.removed == 1:
                self.display_level.set('ROUND: ' + str(self.tags.get('R', 1)) + ' / GAME OVER!', (255, 0, 0, 255))
                self.location.mode = 1
            else:
                return super().turn()

    def attack(self, front):
        for thing in reversed(front.things):
            level = thing.get_level()
            if level > 0 and thing.tags.get('ob', 0) != 4:
                self.vec += (front - self.pos) * 15
                self.location.play_sound('hit')
                if thing.get_level() <= self.get_level():
                    if thing.name == 'Corpse' and self.weapon and self.weapon.name == 'Shovel':
                        from game.Factory import Factory
                        Factory.make('Grave', thing.pos)
                        self.weapon.tags.increment('L', 1)
                    elif thing.name == 'Airhorn':
                        to_remove = []
                        from game.AI import Cop
                        from game.AI import Shopper
                        for i in self.location.population:
                            if i != self and i.tags.get('L', 0) > 0 and (isinstance(i, Cop) or isinstance(i, Shopper)):
                                to_remove.append(i)
                        for i in to_remove:
                            i.remove()
                    else:
                        self.decay()
                    thing.remove()
                elif self.weapon:
                    thing.decay()
                    self.decay()
                self.delay = 4
                return True

    def sound(self, track):
        self.location.play_sound(track)


class Van(Item):
    def __init__(self, location):
        super().__init__(location)
        self.display_level.color = (20, 120, 20, 255)

    def update_display_level(self):
        s = self.tags.get('s', 0)
        req = self.tags.get('req', 1)
        if s >= req:
            self.display_level.set('Round ' + str(Global.player.tags.get('R')) + ' Clear!')
            self.location.mode = 1
        else:
            self.display_level.set(str(s) + ' / ' + str(req))

    def supply(self, item):
        self.tags.increment('s', item.get_level())
        item.remove()
        self.update_display_level()
