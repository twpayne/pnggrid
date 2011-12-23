import json



class UTFGrid(object):

    def __init__(self, grid, keys, data=None):
        self.grid = grid
        self.keys = keys
        self.data = data

    def __getitem__(self, xy):
        x, y = xy
        index = ord(self.grid[y][x])
        if index >= 93:
            index -=1
        if index >= 35:
            index -= 1
        index -= 32
        return self.keys[index]

    def __setitem__(self, xy, key):
        x, y = xy
        if key is None:
            key = ''
        if key not in self.keys:
            self.keys[key] = len(self.keys)
        index = self.keys[key] + 32
        if index >= 34:
            index += 1
        if index >= 92:
            index += 1
        self.grid[y][x] = chr(index)

    @classmethod
    def from_dict(cls, utfgrid):
        keys = [int(k) if k != '' else None for k in utfgrid['keys']]
        return cls(utfgrid['grid'], keys, utfgrid.get('data', None))

    @classmethod
    def from_file(cls, file):
        return cls.from_dict(json.load(file))

    @classmethod
    def from_string(cls, string):
        return cls.from_dict(json.loads(string))

