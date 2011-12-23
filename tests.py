from cStringIO import StringIO
import unittest

import PIL.Image

from pnggrid import PNGGrid
from utfgrid import UTFGrid



class TestPNGGridDemo(unittest.TestCase):

    def setUp(self):
        self.pnggrid = PNGGrid.from_utfgrid_file(open('demo.json'))

    def test_grid(self):
        for i in xrange(0, 65502):
            self.assertEqual(self.pnggrid[i & 0xff, i >> 8], i)
        for i in xrange(65502, 65536):
            self.assertEqual(self.pnggrid[i & 0xff, i >> 8], 65501)



class TestPNGGridEurope(unittest.TestCase):

    def setUp(self):
        self.utfgrid = UTFGrid.from_file(open('europe.json'))
        self.pnggrid = PNGGrid.from_utfgrid_file(open('europe.json'))

    def test_grid(self):
        for y in xrange(0, 64):
            for x in xrange(0, 64):
                self.assertEqual(self.pnggrid[x, y], self.utfgrid[x, y])

    def test_save_load(self):
        width, height = self.pnggrid.image.size
        string_io = StringIO()
        self.pnggrid.image.save(string_io, 'PNG')
        image = PIL.Image.open(StringIO(string_io.getvalue()))
        pnggrid = PNGGrid(image)
        self.assertEqual(pnggrid.image.size, (width, height))
        for y in xrange(0, height):
            for x in xrange(0, width):
                self.assertEqual(pnggrid[x, y], self.pnggrid[x, y])
        self.assertEqual(self.pnggrid.get_data(), pnggrid.get_data())



class TestUTFGridDemo(unittest.TestCase):

    def setUp(self):
        self.utfgrid = UTFGrid.from_file(open('demo.json'))

    def test_grid(self):
        for y in xrange(0, 256):
            for x in xrange(0, 256):
                if y == 255 and x >= 222:
                    self.assertEqual(self.utfgrid[x, y], 65501)
                else:
                    self.assertEqual(self.utfgrid[x, y], 256 * y + x)



if __name__ == '__main__':
    unittest.main()
