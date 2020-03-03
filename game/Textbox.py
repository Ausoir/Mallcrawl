from game import Global
from pyglet.text import Label


class Textbox:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = (120, 120, 120, 180)
        self.transparent = (0, 0, 0, 0)
        self.visible = True
        self.text = Label('', x=0, y=-1000,
                          font_name='Ubuntu',
                          font_size=24,
                          group=Global.draw_group.group_gui,
                          color=self.color,
                          anchor_x='center', anchor_y='center')

    def add_batch(self):
        self.text.batch = Global.draw_group.batch

    def remove_batch(self):
        self.text.batch = None

    def bound(self, visible):
        if visible and self.visible:
            self.text.color = self.color
        else:
            self.text.color = self.transparent

    def update(self, x, y):
        self.text.x = x
        self.text.y = y

    def set(self, arg, color=None):
        self.text.text = arg
        if color:
            self.text.color = color
