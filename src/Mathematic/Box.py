from Vector2 import *

# Usefull class for a axis aligned rectangle. contain:
#   . a Vector2f position : generaly the top left corner position
#   . a Vector2f size : the size of the rectangle : (width, height)
# all of these values are in pixels
class Box:
    def __init__(self):
        self._position = Vector2f(0,0)   # top left corner position in pixel
        self.size = Vector2f(16,16)     # size in pixel

    # test if an other box is overlapping the actual box
    # parameter : b : the box to check overlapping with
    # return True if the two box overlap, False otherwise
    def overlap(self, b):
        if (self.position.x <= b.position.x + b.size.x and self.position.x + self.size.x >= b.position.x and 
            self.position.y <= b.position.y + b.size.y and self.position.y + self.size.y >= b.position.y):
            return True
        return False


    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, new_position):
        self._position = new_position

    # return the box center position, or ajust the box position for a desired box center position
    @property
    def center(self):
        return self.position + 0.5*self.size
    @center.setter
    def center(self, new_center):
        self.position = new_center - 0.5*self.size
    
    # return a box of size (0,0) at desired position (aka a simple point packed into a Box structure)
    @staticmethod
    def fromPoint(position):
        b = Box()
        b.position = position
        b.size = Vector2f(0,0)
        return b

    # return a box inflated by a vector s in any direction
    def inflate(self, s):
        b = Box()
        b.size = self.size + 2*s
        b.center = self.center
        return b


    #DEBUG
    def print(self):
        print('box, position : ' + str(self.position) + ', size : ' + str(self.size))

    def __str__(self):
        return 'box, position : ' + str(self.position) + ', size : ' + str(self.size)