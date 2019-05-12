import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *


class PhysicsSweptBox(Box):
    def __init__(self, entity, delta):
        super(PhysicsSweptBox, self).__init__()
        self.entity = entity
        self.size = Vector2f(abs(delta.x), abs(delta.y)) + entity.size
        self.center = entity.center + 0.5 * delta

    def __str__(self):
        return 'swept box, position : ' + str(self.position) + ', size : ' + str(self.size)