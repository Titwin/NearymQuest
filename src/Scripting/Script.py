import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')

from Component import *

class Script(Component):
    def __init__(self):
        super(Script, self).__init__()

    def update(self):
        pass