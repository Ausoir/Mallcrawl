from game import Global
from game.AI import Cop, Elevator, Shopper
from game.Hero import Hero
from game.Item import Item
from game.Prop import Prop


class Factory:
    data = {'Door': [Item, 'g_6x0', ['L:4']],
            'Gate': [Prop, 'g_10x0', ['ob:0']],
            'Window': [Item, 'g_8x0', ['L:1', 'ob:5']],
            'Lamp': [Item, 'g_8x1', ['L:1', 'ob:4']],
            'Bottle': [Prop, 'g_0x1', ['ob:6']],
            'Bed': [Prop, 'g_3x1', ['ob:5']],
            'Sofa': [Prop, 'g_4x1', ['ob:5']],
            'Cart': [Item, 'g_1x1', ['L:9']],
            'TV': [Item, 'g_2x2', ['L:1', 'ob:4']],
            'Chip': [Item, 'g_3x2', ['L:1', 'ob:4']],
            'Corpse': [Item, 'g_0x3', ['L:1', 'ob:3']],
            'Player': [Hero, 'g_1x3', ['L:5', 'ob:3']],
            'Elevator': [Elevator, 'g_0x3', ['L:80', 'ob:3']],
            'Shopper': [Shopper, 'g_1x3', ['L:1', 'ob:3']],
            'Cop': [Cop, 'g_1x3', ['L:4', 'ob:3']]
            }

    @staticmethod
    def make_user(pos):
        r = Factory.make('Player', pos)
        r.tags.set('spd', -1, add=True)
        Global.map_view.old_camera = r.pos
        r.center_camera()
        Global.map_view.on_sight_change()
        return r

    @staticmethod
    def make(name, pos):
        data = Factory.data[name]
        r = data[0](pos.location)
        r.set_form(data[1])
        r.tags.load(data[2])
        r.level = r.tags.get('L', 1)
        r.obstruct_type = r.tags.get('ob', 2)
        r.pos = pos
        r.add()
        return r
