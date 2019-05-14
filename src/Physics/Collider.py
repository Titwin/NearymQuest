import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *


# A Box derivated class to represent a box collider.
# contain
#   . a collider type enum
# each instance contain
#   . the collider type
class Collider(Box):
    UNKNOWN = 0			# not specified
    BOUNDINGBOX = 1     # a bounding box affected by physics
    TRIGGERBOX = 2      # a trigger box, if something go inside rise a trigger
    HITBOX = 3          # like a triggerbox but to represent sensible area or dammage area

    # constructor, default type is UNKNOWN
    def __init__(self, type = UNKNOWN):
        super(Collider, self).__init__()
        self.type = type


    @staticmethod
    def fromBox(position, size, type):
        c = Collider(type)
        c.position = position
        c.size = size
        return c
