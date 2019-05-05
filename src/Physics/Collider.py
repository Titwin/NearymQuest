import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *

class Collider(Box):
    UNKNOWN = 0
    BOUNDINGBOX = 1
    TRIGGERBOX = 2
    HITBOX = 3

    def __init__(self, type = UNKNOWN):
        super(Collider, self).__init__()
        self.type = type
