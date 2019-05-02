from Vector2 import Vector2i
from Material import *


class Tile:
    def __init__(self, position = Vector2i(0,0), materialIndex = None, material = None):
        self.position = position
        self.materials = {}
        if materialIndex != None:
            self.materials[materialIndex] = material

    def add(self, index, m):
        self.materials[index] = m

    def remove(self, m):
        self.materials.pop(m, None)



    # DEBUG
    def print(self):
        print("Tile, position : " + str(self.position))
        for key, value in self.materials.items():
            print('   ' + str(key) + " : " + str(value))

    def __str__(self):
        l = sorted(self.materials.keys())
        return "position : " + str(self.position) + ", material count : " + str(len(self.materials)) + ", range : [ " + str(l[0]) + " ; " + str(l[len(l)-1]) + " ]"
