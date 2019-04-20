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

        self.im.addEvent(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        self.im.addEvent(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        self.im.addEvent(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        self.im.addEvent(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        self.im.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

        self.dashTimer = 0
        
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
        self.im.update()

        speedX = 3
        speedY = 3
        if self.im.CheckEvent('dash forward') or self.im.CheckEvent('dash backward') or self.im.CheckEvent('dash left') or self.im.CheckEvent('dash right'):
            self.dashTimer = 10
        if self.dashTimer > 0:
            speedX *= 5
            speedY *= 5
            self.dashTimer -= 1
        elif self.im.CheckEvent('run'):
            speedX *= 2
            speedY *= 2

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
        
        #pyxel.blt(TILE_SIZE,TILE_SIZE,self.tilePalette,TILE_SIZE*6,0,TILE_SIZE*3,TILE_SIZE*3)
        
        for y in range(self.map.sizeY):
            for x in range(self.map.sizeX):
                tile = self.map[(x,y)]
                if(len(tile.materials)>0):
                    for m in tile.materials:
                        mat = m.index
                        indexX = mat %16
                        indexY = mat//16
                        if mat != -1:
                            pyxel.blt(
                                x*TILE_SIZE, y*TILE_SIZE, 
                                self.tilePalette, 
                                (indexX)*TILE_SIZE, (indexY)*TILE_SIZE, 
                                TILE_SIZE, TILE_SIZE)

        # handle character            
        pyxel.rect(self.x, self.y, self.x + 8, self.y +16, 9)

# program entry
App()