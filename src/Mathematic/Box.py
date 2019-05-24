from Vector2 import *

# Usefull class for a axis aligned rectangle. contain:
#   . a Vector2f position : generaly the top left corner position
#   . a Vector2f size : the size of the rectangle : (width, height)
# all of these values are in pixels
class Box:
    def __init__(self, p=Vector2f(0,0), s=Vector2f(0,0)):
        self.position = p  # top left corner position in pixel
        self.size = s      # size in pixel

    # test if an other box is overlapping the actual box
    # parameter : b : the box to check overlapping with
    # return True if the two box overlap, False otherwise
    def overlap(self, b):
        x1,y1,sx1,sy1 = self.position.x, self.position.y, self.size.x, self.size.y
        x2,y2,sx2,sy2 = b.position.x, b.position.y, b.size.x, b.size.y
        if (x1 <= x2 + sx2 and x1 + sx1 >= x2 and y1 <= y2 + sy2 and y1 + sy1 >= y2):
            return True
        return False

    def overlapPoint(self, p):
        x1,y1,sx1,sy1 = self.position.x, self.position.y, self.size.x, self.size.y
        x2,y2 = p.x, p.y
        if (x1 <= x2 and x1 + sx1 >= x2 and y1 <= y2 and y1 + sy1 >= y2):
            return True
        return False

    def inflated(self, inflationSize):
        b = Box()
        b.size = self.size + 2*inflationSize
        b.center = self.center
        return b
        
    # return the box center position, or ajust the box position for a desired box center position
    @property
    def center(self):
        return self.position + 0.5*self.size
    @center.setter
    def center(self, new_center):
        self.position = new_center - 0.5*self.size
    
    def __hash__(self):
        return id(self)
        
    #DEBUG
    def print(self):
        print('box, position : ' + str(self.position) + ', size : ' + str(self.size))

    def __str__(self):
        return 'box, position : ' + str(self.position) + ', size : ' + str(self.size)