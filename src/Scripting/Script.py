import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Component import *

class Script(Component):
    def __init__(self):
        super(Script, self).__init__()

    def update(self):
        pass

    def onPreRender(self):
        pass

    #DEBUG
    def __str__(self):
        return "Script : " + self.__class__.__name__