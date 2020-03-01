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
        self.location.spawn += .01
        if self.removed == 1:
            self.display_level.set('GAME OVER!', (255, 0, 0, 255))
        else:
            return super().turn()
