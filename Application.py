# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
import InputManagerModule # as IMmodule
from Events import *
from TilemapModule import *
from PlayerModule import *

# application class
class App:
    application = None
    def __init__(self):

        application = self

        #global initialization
        pyxel.init(255, 255)

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
        #map
        self.LoadMap()

        #player
        self.player = Player()
        self.player.RegisterEvents(self.inputManager)

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls()

    def draw(self):
        # clear the scene
        pyxel.cls(0)

        # draw map      
        #pyxel.blt(TILE_SIZE,TILE_SIZE,self.tilePalette,TILE_SIZE*6,0,TILE_SIZE*3,TILE_SIZE*3)
        self.mapRenderer.draw()

        # handle character            
        pyxel.rect(self.player.x, self.player.y, self.player.x + 8, self.player.y +16, 9)


    def LoadMap(self):
        ## create the map
        ## load the tile palette
        self.tilePalette = pyxel.image(0).load(0, 0, 'ressources/PathAndObjects-low.png')
        ## load the map layers, in order
        self.map = Tilemap.ImportMap(
            ("ressources/map1_background.csv",
            "ressources/map1_path.csv",
            "ressources/map1_objects.csv",
            "ressources/map1_small objects.csv"
            ),
        50,50)
         ## set the map renderer
        self.mapRenderer = TilemapRenderer(self.map,self.tilePalette)

# program entry
App()