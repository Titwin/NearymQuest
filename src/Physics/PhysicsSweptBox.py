from Box import *
from Vector2 import Vector2f

# special class to represent a moving entity box
# used by the physics engine
# contain : 
#    - entity : pointer on the moving entity
#    - position : inherited from Box
#    - size : inherited from Box
#    - delta : the delta position (displacement)
#    - initial : the initial collider box
class PhysicsSweptBox(Box):
    # constructor
    def __init__(self, collider, delta, entity):
        super(PhysicsSweptBox, self).__init__()
        self.entity = entity
        self.size = Vector2f(abs(delta.x), abs(delta.y)) + collider.size
        self.center = collider.center + 0.5 * delta
        self.delta = delta
        self.initial = Box.fromBox(collider.position, collider.size)
        self.finalDelta = Vector2f(0,0)

    # DEBUG
    def __str__(self):
        return 'swept box, position : ' + str(self.position) + ', size : ' + str(self.size)