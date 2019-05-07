import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *


# A class representing a region of an image bank with some attributes
# contain :
#    - position : legacy from Box, top left corner position in pixel in image bank
#    - size : legacy from Box, size of the rectangle in pixel
#    - transparency : the color to consider transparent in the whole rectangle
#    - pivot : the image pivot. relative to an entity, where to draw this sprite ? answer is at : entity.position - sprite.pivot
#
class Sprite(Box):
    def __init__(self, position = Vector2f(0,0), size = Vector2f(16,16), pivot = Vector2f(0,0), transparency = -1):
        super(Box, self).__init__()
        self.position = position
        self.size = size
        self.transparency = transparency
        self.pivot = pivot

    # in case the entity is flipped use this to directly have the corrected pivot
    # return the corrected pivot for a flipped entity
    @property
    def flippedPivot(self):
        return Vector2f(self.size.x - self.pivot.x, self.pivot.y)
