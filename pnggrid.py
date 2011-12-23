from itertools import chain, imap, izip_longest
import json

import PIL.Image

from utfgrid import UTFGrid



# http://docs.python.org/library/itertools.html
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)



class PNGGrid(object):

    def __init__(self, image, data=None):
        self.image = image
        self.pixels = self.image.load()
        if data is not None:
            self.set_data(data)

    def __getitem__(self, xy):
        return self.unpack_pixel(self.pixels[xy])

    def __setitem__(self, xy, key):
        self.pixels[xy] = self.pack_key(key)

    def get_data(self):
        width, height = self.image.size
        if width == height:
            return None
        json_data = ''.join(imap(chr, chain.from_iterable(self.pixels[x, y] for y in xrange(width, height) for x in xrange(0, width))))
        index = json_data.find('\0')
        if index != -1:
            json_data = json_data[:index]
        return json.loads(json_data)

    def set_data(self, data):
        width, height = self.image.size
        if data is None:
            if height != width:
                self.image = self.image.crop((0, 0, width, width))
                self.pixels = self.image.load()
        else:
            s = json.dumps(data, separators=(',', ':'))
            if len(s) % width != 0:
                s += '\0' * (width - len(s) % width)
            data_rows = len(s) // width
            if height != width + data_rows:
                self.image = self.image.crop((0, 0, width, width + data_rows))
                self.pixels = self.image.load()
            for i, pixel in enumerate(grouper(4, s)):
                self.pixels[i % width, width + i // width] = tuple(ord(x) for x in pixel)

    def pack_key(self, key):
        if key is None:
            return (255, 255, 255, 0)
        else:
            assert 0 <= key < 2 << 24
            r, g, b, a = key & 0xff, (key >> 8) & 0xff, (key >> 16) & 0xff, 255
            return (r, g, b, a)

    def unpack_pixel(self, pixel):
        r, g, b, a = pixel
        if a == 0:
            return None
        else:
            return r + (g << 8) + (b << 16)

    @classmethod
    def from_utfgrid(cls, utfgrid):
        height = len(utfgrid.grid)
        width = height
        assert 0 < height <= 256
        assert height & (height - 1) == 0
        if utfgrid.data is None:
            data = None
        else:
            data = utfgrid.data
            height += (len(json.dumps(data, separators=(',', ':'))) + width - 1) // width
        pnggrid = cls(PIL.Image.new('RGBA', (width, height)), data)
        for y, row in enumerate(utfgrid.grid):
            assert len(row) == width
            for x in xrange(0, width):
                pnggrid[x, y] = utfgrid[x, y]
        return pnggrid

    @classmethod
    def from_utfgrid_file(cls, file):
        return cls.from_utfgrid(UTFGrid.from_file(file))

    @classmethod
    def from_utfgrid_string(cls, string):
        return cls.from_utfgrid(UTFGrid.from_string(string))
