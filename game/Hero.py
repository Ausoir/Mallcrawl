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
                if self.tags.get('spd', 0) < 0:
                    self.tags.increment('spd', 1)
            self.next_action = 0
            Global.main.end = True
        elif self.location.mode > 0:
            self.location.mode += 1
        else:
            if self.removed == 1:
                self.display_level.set('ROUND: ' + str(self.tags.get('R', 1)) + ' / GAME OVER!', (255, 0, 0, 255))
                self.location.mode = 1
            else:
                return super().turn()

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
        elif s > 0:
            self.display_level.set(str(s) + ' / ' + str(req))
        else:
            self.display_level.set('Bring me the goods!')

    def supply(self, item):
        self.tags.increment('s', item.get_level())
        item.remove()
        self.update_display_level()
