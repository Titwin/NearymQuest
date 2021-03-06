from Box import *
from Component import *


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
        self.size = Vector2f(16,16)
        self.components = {}

    def __del__(self):
        rb = self.getComponent('RigidBody')
        if rb:
            Entity.WORLD.removeDynamicEntity(self)
        scripts = self.getComponent('Scripts')
        if scripts:
            Entity.WORLD.removeScriptedEntity(self)

    ## COMPONENT RELATED
    # get the component defined by componentType
    # return the component asked, None otherwise
    def getComponent(self, componentType, error=None):
        if componentType in self.components.keys():
            return self.components[componentType]
        else:
            return error

    # add a component to the component list
    # parameter : componentType : the component type or name
    # parameter : component : the real object to attach as component
    def addComponent(self, componentType, component):
        try:
            for c in component:
                if isinstance(c, Component):
                    c.owner = self
        except TypeError as te:
             component.owner = self
        self.components[componentType] = component

    # remove the first component of type componentType from the entity
    # parameter : componentType : the component to remove
    def removeComponent(self, componentType):
        self.components.pop(component, None)

    ## OVERLOAD OF BOX ATTRIBUTES
    #@property
    #def position(self):
    #    return self._position
    #@position.setter
    #def position(self, new_position):
    #    if Entity.WORLD:
    #        Entity.WORLD.removeEntity(self)
    #    self._position = new_position
    #    if Entity.WORLD:
    #        Entity.WORLD.addEntity(self)

    ## PREFAB INSTANCING
    # create a copy of entity
    # instanciate a new entity and populate with shared component
    # return a copy
    def Copy(self):
        other = Entity()
        other.size = self.size
        other.position = self.position
        #for name in self.components.keys():
        #    other.addComponent(name, copy.deepcopy(self.components[name]))
        return other

    #DEBUG
    def print(self):
        print(str(self))

    def __str__(self):
        msg = 'entity, position : ' + str(self.position) + ', size : ' + str(self.size)
        for c in self.components.keys():
            msg += '\n   ' + str(c) + ' ' + str(self.components[c])
        return msg

