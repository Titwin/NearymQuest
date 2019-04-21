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

pyxel.DEFAULT_PALETTE[11] = 0x00BC2C

# application class
class App:
    application = None
    def __init__(self):
        application = self

        #global initialization
        pyxel.init(255, 255)
        random.seed(0)

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
        #map
        self.LoadMap()

        #player
        self.player = Player()
        self.player.RegisterEvents(self.inputManager)
        self.player.x = 256
        self.player.y = 256

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls(self.map.sizeX*16, self.map.sizeY*16)

    def draw(self):
        # clear the scene
        pyxel.cls(0)

        # draw map
        camX = max(self.player.x-128, 0)
        camY = max(self.player.y-128, 0)
        self.mapRenderer.draw(self.map, camX, camY)

        # handle character
        playerX = min(self.player.x, 128)
        playerY = min(self.player.y, 128)
        pyxel.blt(playerX, playerY, self.charactersPalette, 0, 0, 16, 16, 0)
        #pyxel.rect(playerX, playerY, playerX + 8, playerY +16, 9)

        # handle multiple overlay (object height)
        playerExceptionX = math.floor(self.player.x/16)
        playerExceptionY = math.floor(self.player.y/16)

        self.mapRenderer.draw(self.overlay1, camX, camY, playerExceptionX, playerExceptionY)
        self.mapRenderer.draw(self.overlay2, camX, camY, playerExceptionX, playerExceptionY)
        self.mapRenderer.draw(self.overlay3, camX, camY, playerExceptionX, playerExceptionY)

        #creepy face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)

    def LoadMap(self):
        ## create the map
        ## load the tile palette
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0

        pyxel.image(1).load(0, 0, 'ressources/characters.png')
        self.charactersPalette = 1
        
        self.map = Tilemap.ImportMap(["ressources/map2_background.csv", "ressources/map2_objects1.csv"], 50,50)

        self.overlay1 = Tilemap.ImportLayer(["ressources/map2_overlay1.csv"], 50,50, 0)
        self.overlay2 = Tilemap.ImportLayer(["ressources/map2_overlay2.csv"], 50,50, 0)
        self.overlay3 = Tilemap.ImportLayer(["ressources/map2_overlay3.csv"], 50,50, 0)
        
         ## set the map renderer
        self.mapRenderer = TilemapRenderer(self.tilePalette)

# program entry
App()