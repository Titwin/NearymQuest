from Box import *

class Collider(Box):
    UNKNOWN = 0
    BOUNDINGBOX = 1
    TRIGGERBOX = 2
    HITBOX = 3

    def __init__(self, type = UNKNOWN):
        self.type = type