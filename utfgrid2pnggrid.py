#!/usr/bin/env python

import os.path
import sys

from pnggrid import PNGGrid



if __name__ == '__main__':
    for arg in sys.argv[1:]:
        with open(arg) as utfgrid_file:
            pnggrid = PNGGrid.from_utfgrid_file(utfgrid_file)
        with open(os.path.splitext(arg)[0] + '.png', 'w') as pnggrid_file:
            pnggrid.image.save(pnggrid_file)
