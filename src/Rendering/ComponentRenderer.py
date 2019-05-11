import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')

from Component import *
import pyxel

class ComponentRenderer(Component):
    def __init__(self):
        super(ComponentRenderer, self).__init__()

    def draw(self, camera, world):
        pass