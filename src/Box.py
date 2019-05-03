from Vector2 import *

class Box:
    def __init__(self):
        self.position = Vector2f(0,0)   # top left corner position in pixel
        self.size = Vector2f(16,16)     # size in pixel

    def overlap(self, b):
        if (self.position.x < b.position.x + b.size.x and self.position.x + self.size.x > b.position.x and 
            self.position.y < b.position.y + b.size.y and self.position.y + self.size.y > b.size.y):
            return True
        return False

    @staticmethod
    def origin():
    	b = Box()
    	b.size = Vector2f(0,0)
    	return b