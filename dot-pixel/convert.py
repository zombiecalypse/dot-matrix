from palette import Color
import Image
import numpy
from svgwrite import Drawing, rgb
from itertools import product

import sys

def each_pixel(img):
    try:
        return product(*[xrange(z) for z in img.size])
    except:
        return product(*[xrange(z) for z in img.shape[:2]])

def openToHsv(file):
    img = Image.open(file)
    arr = numpy.zeros(img.size+(3,), dtype=float)
    for v in each_pixel(img):
        try:
            color = Color(rgb8=img.getpixel(v))
            arr[v] = tuple(color.hls)
        except ValueError as e:
            print v,":",img.getpixel(v)
            raise e
    return arr

E = 1e-10
from math import exp

def peri(lum, mean, std):
    return 1-lum
    #return 1

def convertToDotMatrix(img):
    c = canvas = Drawing()
    mean, std = img[:,:,1].mean(), img[:,:,1].std()
    for x,y in each_pixel(img):
        hue, lum, sat = img[x,y]
        perimeter = peri(lum, mean, std)
        color = Color.from_hls(hue, lum, sat)
        if perimeter > 0.15:
            canvas.add(c.circle(center=(10*x,10*y), r = 10*perimeter/2, fill = rgb(*color.rgb8)))
    return canvas

if __name__=='__main__':
    import sys
    img = openToHsv(sys.argv[1])
    svg = convertToDotMatrix(img)
    svg.saveas('test.svg')
