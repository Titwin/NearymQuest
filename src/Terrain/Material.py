from Vector2 import Vector2i
import math

# a class to represent a sprite blited to create the terrain
# for example a tile of the tilemap contain several materials, sorted by layers. useful to create complex terrain with transparency and layers
# contain : 
#    - imageBank : the image bank reference (to perform a blit), default is 0
#    - index : the tile index, default is 0 (so the first top left square corner of size 16x16 pixel)
#    - flip : a vector to indiquate if the image has to be flipped for the blit (-1=flip on this axis; 1=no flip), default is (1,1) > no flip at all
#    - transparency : the transparency color to consider in the tile, default is -1 (no transparency color)
class Material:
    # constructor
    def __init__(self, imageBank = 0, index = 0, flip = Vector2i(1,1), transparency = -1):
        self.imageBank = imageBank
        self.index = index
        self.flip = flip
        self.transparency = transparency

    # get the tile column index in the image
    # just transform the one dimension index into a bidimentional index (row, column), here just computing column
    @property
    def indexx(self):
        return self.index%16

    # get the tile row index in the image
    # just transform the one dimension index into a bidimentional index (row, column), here just computing row
    @property
    def indexy(self):
        return math.floor(self.index/16)

    # DEBUG
    def print(self):
        print(str(self))

    def __str__(self):
        return 'image bank : ' + str(self.imageBank) + ', index : ' + str(self.index) + ', flip : ' + str(self.flip) + ', transparency : ' + str(self.transparency)


