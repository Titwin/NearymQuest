import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *
from Component import *

class Entity(Box):
    def __init__(self):
        super(Entity, self).__init__()
        self.position = Vector2f(0,0)
        self.size = Vector2f(16,16)
        self.components = {}

    def getComponent(self, componentType):
        return self.components[componentType]

    def addComponent(self, componentType, component):
        self.components[componentType] = component

    def removeComponent(self, componentType):
        self.components.pop(component, None)



