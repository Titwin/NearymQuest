import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')

from Component import *
from Vector2 import Vector2f

# Required component for dynamic objects
# contain :
#    - velocity : the entity velocity vector
class RigidBody(Component):
    # constructor
    def __init__(self):
        super(RigidBody, self).__init__()
        self._velocity = Vector2f(0,0)

    def __del__(self):
        self.owner.WORLD.removeDynamicEntity(self.owner)

    # velocity setter / getter
    @property
    def velocity(self):
        return self._velocity
    @velocity.setter
    def velocity(self, v):
        if self.owner.WORLD:
            if v.x==0 and v.y==0:
                self.owner.WORLD.removeDynamicEntity(self.owner)
            else:
                self.owner.WORLD.addDynamicEntity(self.owner)
        self._velocity = v
    
