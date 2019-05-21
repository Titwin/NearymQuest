from Box import *
from Vector2 import Vector2f


# A Box derivated class to represent a camera
# it's just a box with a fixed size of (256,256) for now
# to place it looking a specific location use the Box.center property
class Camera(Box):
	# constructor
    def __init__(self):
        super(Camera, self).__init__()
        self.size = Vector2f(256, 256)
        self.position = Vector2f(0, 0)




# TODO:
# add some features like :
#   . a shake effect
#   . a culling mask (only rendering some stuff)
#   . [cool and usefull stuff]