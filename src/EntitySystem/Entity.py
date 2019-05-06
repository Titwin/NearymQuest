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
        self.pivot = Vector2f(8,16)
        self.components = {}

    def getComponent(self, componentType):
        if componentType in self.components.keys():
            return self.components[componentType]
        else:
            return None

    def addComponent(self, componentType, component):
        component.owner = self
        self.components[componentType] = component

    def removeComponent(self, componentType):
        self.components.pop(component, None)



