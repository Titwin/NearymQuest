import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Box import *
from Component import *
import copy

# All object in the world are entities, or heritate from it (so they are in a way)
# each instance contains :
#    - position : legacy from Box, the position of the entity in the world in pixel
#    - size : legacy from Box, the size of the entity in pixel
#    - components : a dictionary<string, var>
#            - the key is the component type (sprite, animator, controller, ...)
#            - the value is the "component", it could be something herited by Component, a list, ..., anything actually
class Entity(Box):
    WORLD = None    # current world containing the entity

    # constructor
    def __init__(self):
        super(Entity, self).__init__()
        #self.position = Vector2f(0,0)
        self.size = Vector2f(16,16)
        self.components = {}

    ## COMPONENT RELATED
    # get the component defined by componentType
    # return the component asked, None otherwise
    def getComponent(self, componentType):
        if componentType in self.components.keys():
            return self.components[componentType]
        else:
            return None

    # add a component to the component list
    def addComponent(self, componentType, component):
        try:
            for c in component:
                if isinstance(c, Component):
                    c.owner = self
        except TypeError as te:
             component.owner = self
        self.components[componentType] = component

    # remove the first component of type componentType from the entity
    def removeComponent(self, componentType):
        self.components.pop(component, None)

    ## CONTAINER RELATED
    # necessary to have Entity set
    def __hash__(self):
        return id(self)

    ## OVERLOAD OF BOX ATTRIBUTES
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, new_position):
        if Entity.WORLD:
            Entity.WORLD.removeEntity(self)
        self._position = new_position
        if Entity.WORLD:
            Entity.WORLD.addEntity(self)


    def Copy(self):
        other = Entity()
        for name in self.components.keys():
            other.addComponent(name, copy.copy(self.components[name]))
        return other

    #DEBUG
    def print(self):
        print(str(self))

    def __str__(self):
        msg = 'entity, position : ' + str(self.position) + ', size : ' + str(self.size)
        for c in self.components.keys():
            msg += '\n   ' + str(c)
        return msg

