import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Component import *
from Box import *

class Sprite(Component, Box):
    def __init__(self, imageBank = 0, position = Vector2f(0,0), size = Vector2f(16,16), offset = Vector2f(0,0), transparency = -1):
        super(Component, self).__init__()
        super(Box, self).__init__()
        self.imageBank = imageBank
        self.position = position
        self.size = size
        self.transparency = transparency
        self.offset = offset
