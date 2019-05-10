from Vector2 import Vector2f

class RigidBody:
    WORLD = None

    def __init__(self):
        self._velocity = Vector2f(0,0)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, v):
        if v != Vector2f.zero and RigidBody.WORLD:
            RigidBody.WORLD.addDynamicEntity(self)
    
