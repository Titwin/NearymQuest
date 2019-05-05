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


    @property
    def center(self):
        return self.position + 0.5*self.size
    @center.setter
    def center(self, new_center):
        self.position = new_center - 0.5*self.size
    

    @staticmethod
    def fromPoint(position):
        b = Box()
        b.position = position
        b.size = Vector2f(0,0)
        return b



    #DEBUG
    def print(self):
        print('box, position : ' + str(self.position) + ', size : ' + str(self.size))

    def __str__(self):
        return 'box, position : ' + str(self.position) + ', size : ' + str(self.size)