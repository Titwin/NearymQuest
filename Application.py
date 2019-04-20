# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
import InputManagerModule # as IMmodule
from Events import *
from TilemapModule import *

# application class
class App:
    def __init__(self):
        pyxel.init(255, 255)
        self.x = 0
        self.y = 0
        self.im = InputManagerModule.InputManager()

        self.im.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_W], 'forward'))
        self.im.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_S], 'backward'))
        self.im.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_A], 'left'))
        self.im.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_D], 'right'))

        self.im.addEvent(Event(EventType.CHORD, EventNotify.ALL, [pyxel.KEY_Q, pyxel.KEY_E], 'action1'))

        self.im.addEvent(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'run'))
        
        ## create the map
        self.tilePalette = pyxel.image(0).load(0, 0, 'ressources/PathAndObjects-low.png')
        self.map = Tilemap.ImportMap(
            ("ressources/map1_background.csv",
            "ressources/map1_path.csv",
            "ressources/map1_objects.csv",
            "ressources/map1_small objects.csv"
            ),
        50,50)

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        speedX = 3
        speedY = 3
        # handle character controller
        self.im.update()
        if self.im.CheckEvent('forward'):
            self.y = (self.y - 1*speedY) % pyxel.height
        elif self.im.CheckEvent('backward'):
            self.y = (self.y + 1*speedY) % pyxel.height
        if self.im.CheckEvent('left'):
            self.x = (self.x - 1*speedX) % pyxel.width    
        elif self.im.CheckEvent('right'):
            self.x = (self.x + 1*speedX) % pyxel.width

        #print(' ')

    def draw(self):
        # clear the scene
        pyxel.cls(0)

        TILE_SIZE = 16
        # draw map
        x = 0
        y = 0
        pyxel.blt(0,0,self.tilePalette,0,0,256,256)
        

# program entry
App()