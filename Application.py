# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
import InputManagerModule # as IMmodule

# application class
class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.x = 0
        self.im = InputManagerModule.InputManager()
        
        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width
        self.im.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, self.x + 7, 7, 9)

# program entry
App()