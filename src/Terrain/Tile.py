import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Vector2 import Vector2i
from Material import *

# a class to represent a smal portion of a terrain
# contain:
#    - position : the tile vector position (relative to the region and in tile unit)
#    - materials : a dictionnary<layer, material>, a container of material, ordered by layer
class Tile:
    # constructor
    def __init__(self, position = Vector2i(0,0), materialIndex = None, material = None):
        self.position = position
        self.materials = {}
        if materialIndex != None:
            self.materials[materialIndex] = material

    # add material to tile
    # if a material already exist at this layer it's replaced by the new one
    # parameter : index : the layeer index to wher put this new material
    # parameter : m : the material to add
    def add(self, index, m):
        self.materials[index] = m

    # remove a material
    # remove the first material founded in dictionary
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



# TODO : 
# .add a removeLayer function to remove the material at the specified layer
# .add a __getitem__ to get the materail at specified layer
