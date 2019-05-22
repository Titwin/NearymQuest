from Component import *

class Script(Component):
    def __init__(self):
        super(Script, self).__init__()

    def __del__(self):
        pass
        #self.owner.WORLD.removeScriptedEntity(self.owner)

    def _type(self):
        return self.__class__.__name__

    def update(self):
        pass

    def onPreRender(self):
        pass

    #DEBUG
    def __str__(self):
        return "Script : " + self._type