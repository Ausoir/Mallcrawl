from game import Global
from pyglet.text import Label


class Textbox:
    color = (40, 40, 40, 200)
    transparent = (0, 0, 0, 0)

    def __init__(self):
        self.x = 0
        self.y = 0
        self.visible = True
        self.text = Label('', x=0, y=-1000,
                          font_size=24,
                          group=Global.draw_group.group_gui,
                          color=Textbox.color,
                          anchor_x='center', anchor_y='center')

    def add_batch(self):
        self.text.batch = Global.draw_group.batch

    def remove_batch(self):
        self.text.batch = None

    def bound(self, visible):
        if visible and self.visible:
            self.text.color = Textbox.color
        else:
            self.text.color = Textbox.transparent

    def update(self, x, y):
        self.text.x = x
        self.text.y = y

    def set(self, arg, color=None):
        self.text.text = arg
        if color:
            self.text.color = color
