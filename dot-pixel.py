#!/usr/bin/env python
import argparse
from dotpixel import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-W', '--width', type=int)
    group.add_argument('-H', '--height', type=int)
    parser.add_argument('-S', '--size-threshold', type = float, default =0.15)
    parser.add_argument('-s', '--pixel-size', type = float, default =10)
    parser.add_argument('-d', '--pixel-distance', type = float, default = 0)
    parser.add_argument('inputfile', nargs=1)
    parser.add_argument('outputfile', nargs=1)
    args = parser.parse_args()
    arg = lambda x: getattr(args, x)
    with open(arg('inputfile')[0]) as f:
        matrix = DotMatrix(f, 
                arg('size_threshold'), 
                arg('width'), arg('height'),
                arg('pixel_size'),
                arg('pixel_distance'))
        svg = matrix.convert()
        svg.saveas(arg('outputfile')[0])
