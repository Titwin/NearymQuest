from Box import *
from Component import *

class Entity(Box):
    def __init__(self):
        self.position = Vector2f(0,0)
        self.size = Vector2f(16,16)
        self.components = {}

    def getComponent(self, componentType):
        return self.components[componentType]

    def addComponent(self, componentType, component):
        self.components[componentType] = component

    def removeComponent(self, componentType):
        self.components.pop(component, None)



