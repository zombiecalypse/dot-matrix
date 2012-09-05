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

class DotMatrix(object):
    _to_preserve = "To preserve aspect ratio, only one of height and width can be given"
    def __init__(self, file, 
            size_threshold = 0.15, 
            width = None, height = None,
            size_of_pixel = 10,
            distance_between_pixels = 0):
        if width and height: raise ValueError(self._to_preserve)
        self._image = self.openToHsv(file)
        self._setSize(self._image, width, height)
        self._size_threshold = size_threshold
        self._size_of_pixel = size_of_pixel
        self._d_pixel = distance_between_pixels

    def _setSize(self, img, width, height):
        if not (width or height):
            self.width, self.height = img.shape[:2]
            self._scale_factor = 1
        else:
            original_width, original_height = img.shape[:2]
            scale_factor = self._scale_factor = width / float(original_width) if width else height / float(original_height) 
            self.width = int(original_width * scale_factor)
            self.height = int(original_height * scale_factor)

    @staticmethod
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

    @staticmethod
    def peri(lum, mean, std):
        return 1-lum

    def _pixelval(self, x, y):
        "Gets the pixel value of the (x,y) pixel in the output picture"
        assert 0 <= x <= self.width
        assert 0 <= y <= self.height
        owidth, oheight = self._image.shape[:2]
        ox, oy = int(x/self._scale_factor), int(y/self._scale_factor)
        r = int(1/self._scale_factor)/2
        k_left, k_top = max(ox-r, 0), max(oy-r,0)
        k_right, k_bot = min(ox+r, owidth), min(oy+r, oheight)
        return [self._image[k_left:k_right+1,k_top:k_bot+1,i].mean()\
                for i in range(3)]
        

    def convert(self):
        c = canvas = Drawing()
        img = self._image
        mean, std = img[:,:,1].mean(), img[:,:,1].std()
        for x,y in product(xrange(self.width), xrange(self.height)):
            hue, lum, sat = self._pixelval(x,y)
            perimeter = self.peri(lum, mean, std)
            color = Color.from_hls(hue, lum, sat)
            if perimeter > self._size_threshold:
                shape = c.circle(
                        center = (
                            (self._size_of_pixel + self._d_pixel) * x,
                            (self._size_of_pixel + self._d_pixel) * y),
                        r      = self._size_of_pixel * perimeter / 2,
                        fill = rgb(*color.rgb8))
                canvas.add(shape)
        return canvas

if __name__=='__main__':
    import sys
    img = DotMatrix(sys.argv[1], width = 50)
    svg = img.convert()
    svg.saveas('test.svg')
