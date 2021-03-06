from Component import *
import pyxel

# virtual class inherited from component used to render the owner entity
# contain :
#    - draw() : a virtual draw function
class ComponentRenderer(Component):
    # constructor
    def __init__(self):
        super(ComponentRenderer, self).__init__()

    # virtual draw
    # parameter : entityPosFromCam : the entity position in camera space
    def draw(self, entityPosFromCam):
        pass