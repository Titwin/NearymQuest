import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Vector2 import Vector2i
import math

class Material:
    def __init__(self, imageBank = 0, index = 0, flip = Vector2i(1,1), transparency = -1):
        self.imageBank = imageBank
        self.index = index
        self.flip = flip
        self.transparency = transparency

    @property
    def indexx(self):
        return self.index%16

    @property
    def indexy(self):
        return math.floor(self.index/16)

    # DEBUG
    def print(self):
        print(str(self))

    def __str__(self):
        return 'image bank : ' + str(self.imageBank) + ', index : ' + str(self.index) + ', flip : ' + str(self.flip) + ', transparency : ' + str(self.transparency)


