import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *
from Vector2 import *

class Camera(Box):
    def __init__(self):
        super(Camera, self).__init__()
        self.size = Vector2f(256, 256)
        self.position = Vector2f(0, 0)