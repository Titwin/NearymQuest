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

from QuadTree import *
from Entity import *

pyxel.DEFAULT_PALETTE[11] = 0x00BC2C

# application class
class App:
    application = None
    def __init__(self):
        application = self

        #global initialization
        pyxel.init(255,255, caption="Nearym Quest", scale=3)
        random.seed(0)
        self.draw_count = 0

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
        #map
        self.LoadMap()

        # QuadTree structure init
        self.quadtree = TreeNode()
        self.quadtree.split()
        self.quadtree.split()
        self.quadtree.setTransform(0,0, 50*16, 50*16)

        #player
        self.InitPlayer()
        self.charactersPalette = 1

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls(self.map.sizeX*16 - 8, self.map.sizeY*16 - 8)

    def draw(self):
        # clear the scene
        pyxel.cls(0)
        
        # draw map
        camX = max(self.player.x-128, 0)
        camY = max(self.player.y-128, 0)
        self.mapRenderer.draw(self.map, camX, camY)

        # handle character
        self.player.draw()

        # overlay pass
        exception = self.overlay.queryTiles(self.player.x -8, self.player.y -8, self.player.x + 24, self.player.y + 24)
        self.mapRenderer.draw(self.overlay, camX, camY, exception)
        self.mapRenderer.dithering(self.overlay, camX, camY, self.player.x+8, self.player.y+8, exception)

        #creepy face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)

        self.draw_count += 1

    def LoadMap(self):
        ## create the map
        ## load the tile palette
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0

        self.map = Tilemap.ImportMap(["ressources/map2_background.csv", "ressources/map2_objects1.csv"], 50,50)
        self.overlay = Tilemap.ImportLayer(["ressources/map2_overlay1.csv", "ressources/map2_overlay2.csv", "ressources/map2_overlay3.csv"], 50,50, 0)
        
        ## set the map renderer
        self.mapRenderer = TilemapRenderer(self.tilePalette)

    def InitPlayer(self):
        pyxel.image(1).load(0, 0, 'ressources/characters.png')

        self.player = Player()
        self.player.RegisterEvents(self.inputManager)

        self.player.x = 256
        self.player.y = 128

# program entry
App()