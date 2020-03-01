import os

import pyglet
from game.Picture import Picture
from pyglet.image import Texture, Animation
from pyglet.image.atlas import TextureAtlas


class Data:
    cache = {}
    atlas = None

    @staticmethod
    def init():
        Data.atlas = TextureAtlas()
        Data.set_cache('none', Texture.create(1, 1))
        Data.initialize_image('g', [12, 4])

    @staticmethod
    def direct(fdir, path='game/'):
        return os.path.join(path + fdir)

    @staticmethod
    def read(fdir):
        with open(Data.direct(fdir), "U", newline='\n') as f:
            data = f.readlines()
            return '\n'.join([x.strip().split(' //')[0] for x in data])

    @staticmethod
    def write(fdir, data):
        with open(Data.direct(fdir), "w", newline='\n') as f:
            f.seek(0)
            f.write(data)
            f.truncate()

    @staticmethod
    def get_files(fdir, fn):
        return [m for m in os.listdir(Data.direct(fdir)) if fn(m)]

    @staticmethod
    def is_file(fdir):
        return os.path.exists(Data.direct(fdir))

    @staticmethod
    def get_cache(fdir):
        if fdir not in Data.cache:
            return None
        return Data.cache[fdir]

    @staticmethod
    def set_cache(fdir, arg):
        if fdir not in Data.cache:
            Data.cache[fdir] = arg

    @staticmethod
    def get_track(fdir):
        directory = fdir
        cache = Data.get_cache(directory)
        if not cache:
            cache = pyglet.media.StaticSource(pyglet.media.load(Data.direct(directory + '.wav')))
            Data.set_cache(directory, cache)
        return cache

    @staticmethod
    def get_image(fdir, cache):
        img = Data.atlas.add(pyglet.image.load(Data.direct(fdir + '.png')))
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        if cache:
            Data.cache[fdir] = img
        return img

    @staticmethod
    def get_form(fdir, form=None, **kwargs):
        cache = Data.get_cache(fdir)
        if not cache:
            cache = Data.get_image(fdir, False)
        if not form:
            if cache:
                if isinstance(cache, Texture) or isinstance(cache, Animation):
                    return Picture(cache, **kwargs)
                else:
                    return cache

    @staticmethod
    def initialize_image(name, subset_size):
        image = pyglet.image.load(Data.direct(name + '.png'))
        image_grid = pyglet.image.ImageGrid(image, subset_size[1], subset_size[0])
        seq = pyglet.image.TextureGrid(image_grid)
        i = 0
        for y in range(subset_size[1]):
            for x in range(subset_size[0]):
                seq[i].anchor_x = int(seq[i].width / 2)
                seq[i].anchor_y = int(seq[i].height / 2)
                Data.cache[name + '_' + str(x) + 'x' + str(subset_size[1] - y - 1)] = seq[i]
                i += 1

    @staticmethod
    def process_raw(data):
        lines = data.split('\n')
        if len(lines) > 1:
            return Data.parse(",".join('['+x+']' for x in data.split('\n')))
        return Data.parse(data)

    @staticmethod
    def parse(data):
        r = []
        raw = ''
        special = False
        while data:
            code = data[0]
            data = data[1:]
            if code == '\'':
                special = not special
            elif special:
                raw += code
            elif code == '[':
                data, result = Data.parse(data)
                r.append(result)
            elif code == ']':
                if raw:
                    if raw.isdigit() or raw[0] == '-':
                        raw = int(raw)
                    r.append(raw)
                return data, r
            elif code == ',':
                if raw:
                    if raw.isdigit() or raw[0] == '-':
                        raw = int(raw)
                    r.append(raw)
                    raw = ''
            else:
                raw += code
        if raw:
            if raw.isdigit() or raw[0] == '-':
                raw = int(raw)
            r.append(raw)
        return r
