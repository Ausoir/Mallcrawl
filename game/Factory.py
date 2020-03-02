from game import Global
from game.AI import Cop, Elevator, Shopper, Scanner
from game.Hero import Hero, Van
from game.Item import Item
from game.Prop import Prop


class Factory:
    data = {'Door': [Item, 'g_6x0', ['L:7']],
            'Gate': [Prop, 'g_10x0', ['ob:0']],
            'Window': [Item, 'g_8x0', ['L:4', 'ob:5']],
            'Grave': [Item, 'g_11x1', ['L:2', 'ob:5']],
            'Crate': [Prop, 'g_9x0', []],
            'Lamp': [Item, 'g_8x1', ['L:1', 'ob:4']],
            'Bed': [Prop, 'g_3x1', ['ob:5']],
            'Sofa': [Prop, 'g_4x1', ['ob:5']],
            'Register': [Item, 'g_5x1', ['L:8', 'loot:Money', 'ob:5']],
            'Workshop': [Prop, 'g_6x1', ['ob:5']],
            'Kitchen': [Prop, 'g_7x1', ['ob:5']],
            'Toilet': [Prop, 'g_9x1', ['ob:5']],
            'Sink': [Prop, 'g_10x1', ['ob:5']],
            'Cart': [Item, 'g_1x1', ['L:1', 'ob:4']],
            'TV': [Item, 'g_2x1', ['L:3', 'ob:4']],
            'Food': [Prop, 'g_0x2', ['ob:0']],
            'Drink': [Prop, 'g_1x2', ['ob:0']],
            'Clothing': [Prop, 'g_5x2', ['ob:6']],
            'Bag': [Item, 'g_6x2', ['L:1', 'ob:4']],
            'Pickaxe': [Item, 'g_7x2', ['L:3', 'ob:4']],
            'Nightstick': [Item, 'g_8x2', ['L:1', 'ob:4']],
            'Shovel': [Item, 'g_9x2', ['L:2', 'ob:4']],
            'Airhorn': [Item, 'g_10x2', ['L:2', 'ob:5']],
            'Ducttape': [Prop, 'g_11x2', ['ob:0']],
            'Chair': [Item, 'g_4x2', ['L:2', 'ob:4']],
            'Bat': [Item, 'g_3x2', ['L:5', 'ob:4']],
            'Money': [Item, 'g_2x2', ['L:9', 'ob:4']],
            'Corpse': [Item, 'g_0x3', ['L:1', 'ob:3']],
            'Player': [Hero, 'g_1x3', ['L:1', 'ob:3', 'R:1']],
            'Van': [Van, 'g_2x3', ['s:0', 'req:3', 'ob:0']],
            'Elevator': [Elevator, 'g_3x3', ['L:8', 'ob:2']],
            'Shopper': [Shopper, 'g_5x3', ['L:1', 'ob:3', 'loot:Bag']],
            'Shoppest': [Shopper, 'g_9x3', ['L:13', 'spd:-4', 'ob:3', 'loot:Money']],
            'Hobo': [Shopper, 'g_6x3', ['L:8', 'spd:2', 'ob:3']],
            'Dog': [Cop, 'g_7x3', ['L:2', 'spd:-2', 'ob:3']],
            'Agent': [Cop, 'g_8x3', ['L:33', 'spd:2', 'ob:3', 'loot:Elevator']],
            'Cop': [Cop, 'g_4x3', ['L:3', 'ob:3', 'loot:Nightstick']],
            'Scanner': [Scanner, 'g_11x3', ['v:1', 'ob:0']],
            'K9Alpha': [Cop, 'g_10x3', ['L:7', 'spd:-7', 'ob:3', 'loot:Dog']]
            }

    @staticmethod
    def make_user(pos):
        r = Factory.make('Player', pos)
        Global.map_view.old_camera = r.pos
        r.center_camera()
        Global.map_view.on_sight_change()
        return r

    @staticmethod
    def make(name, pos):
        data = Factory.data[name]
        r = data[0](pos.location)
        r.name = name
        r.set_form(data[1])
        r.tags.load(data[2])
        r.level = r.tags.get('L', 1)
        r.obstruct_type = r.tags.get('ob', 2)
        r.pos = pos
        r.add()
        return r
