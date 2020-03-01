from game import Global
import pyglet
from game.Camera import Camera
from game.Data import Data
from game.DrawGroup import DrawGroup
from game.Factory import Factory
from game.Generator import Generator
from game.MapView import MapView
from game.Turn import Turn
from pyglet.gl import *


# noinspection PyAbstractClass
class Execute(pyglet.window.Window):
    input_map = {'w': 2, 'a': 1, 's': 4, 'd': 3}

    def __init__(self):
        super(Execute, self).__init__(1000, 600, 'Mallcrawl', vsync=False, resizable=False)
        self.dt = 0
        self.fps = 1/60.0
        self.end = False
        Global.main = self
        Global.map_view = MapView()
        Global.draw_group = DrawGroup()
        Data.init()
        Execute.start()
        glEnable(pyglet.gl.GL_BLEND)
        glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 0)

    @staticmethod
    def start():
        Turn.init()
        if Global.player and Global.player.removed == 0:
            level = Global.player.tags.get('R')
            Global.land = Generator.generate(20 * level, 15 * level, level)
            Global.player.location = Global.land
            Global.player.relocate(3, 5)
        else:
            Global.land = Generator.generate(30, 12, 1)
            Global.player = Factory.make_user(Global.land.tiles[5][3])
        Turn.add(0, Global.player.turn)
        Turn.add(0, Global.map_view.update_region)
        Turn.add(0, Global.map_view.turn)
        Turn.update()
        Turn.update()
        Turn.update()
        Global.map_view.on_sight_change()

    def on_text_motion(self, motion):
        text = pyglet.window.key.symbol_string(motion)
        self.input(text)

    def on_text(self, text):
        self.input(text)

    @staticmethod
    def input(text):
        if text in Execute.input_map:
            action = Execute.input_map[text]
            Global.player.direction = action
            Global.player.next_action = 1

    def on_resize(self, width, height):
        Global.DISPLAY = (int(width / 2) * 2, int(height / 2) * 2)
        Global.CENTER = (int(Global.DISPLAY[0] / 2), int(Global.DISPLAY[1] / 2))
        Global.SCREEN_TILES = (int(Global.DISPLAY[0] / Global.BLOCK), int(Global.DISPLAY[1] / Global.BLOCK))
        glViewport(0, 0, Global.DISPLAY[0], Global.DISPLAY[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        horizontal = int(Global.DISPLAY[0] / 2)
        vertical = int(Global.DISPLAY[1] / 2)
        glOrtho(-horizontal, horizontal, -vertical, vertical, -1000, 4)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(-Global.OFFSET[0] - 1, -Global.OFFSET[1], 0)

    def loop(self, dt):
        self.dt += dt
        if self.dt > self.fps:
            self.dt = 0
            Camera.update()
            Turn.update()
            Global.map_view.update()
            if self.end:
                Execute.start()
                self.end = False
        pyglet.clock.schedule_once(self.loop, self.fps - self.dt)

    def on_draw(self):
        self.clear()
        Global.draw_group.draw()


if __name__ == '__main__':
    main = Execute()
    main.loop(999)
    pyglet.app.run()
