# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
import InputManagerModule
from Inputs import *

from TilemapModule import *
from PlayerModule import *

from Entity import *
from World import *

pyxel.DEFAULT_PALETTE[11] = 0x00BC2C

# application class
class App:
    application = None
    def __init__(self):
        application = self

        #global initialization
        pyxel.init(255,255, caption="Nearym Quest", scale=3)
        random.seed(0)

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
        #map
        self.LoadMap()

        # QuadTree structure init
        self.world = World()
        self.world.regions[0] = Region(0, 0, 50*16, 50*16)
        self.world.regions[0].load([ "ressources/map2tileset.json",
                          ["ressources/map2_background.csv", "ressources/map2_objects1.csv"], 
                          ["ressources/map2_overlay1.csv", "ressources/map2_overlay2.csv", "ressources/map2_overlay3.csv"]],
                          0)
        self.world.regions[0].setDepth(3)

        #player
        self.player = Player()
        self.player.RegisterEvents(self.inputManager)
        self.player.position.x = 256
        self.player.position.y = 128
        self.draw_count = 0

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls(self.world.regions[0].size.x - 8, self.world.regions[0].size.y - 8)

    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.draw_count += 1

        # draw map
        camX = max(self.player.position.x-128, 0)
        camY = max(self.player.position.y-128, 0)
        self.mapRenderer.draw(self.world.regions[0].tilemapBase, camX, camY)

        # handle character
        self.player.draw()

        # overlay pass
        overlay = self.world.regions[0].tilemapOverlay
        exception = overlay.queryTiles(self.player.position.x -8, self.player.position.y -8, self.player.position.x + 24, self.player.position.y + 24)
        self.mapRenderer.draw(overlay, camX, camY, exception)
        self.mapRenderer.dithering(overlay, camX, camY, self.player.position.x+8, self.player.position.y+8, exception)

        #creepy face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)

    def LoadMap(self):
        ## create the map
        self.world = World(1, 1)
        self.world.regions[0] = Region(0, 0, 50*16, 50*16)
        self.world.regions[0].load([ "ressources/map2tileset.json",
                          ["ressources/map2_background.csv", "ressources/map2_objects1.csv"], 
                          ["ressources/map2_overlay1.csv", "ressources/map2_overlay2.csv", "ressources/map2_overlay3.csv"]],
                          0)
        self.world.regions[0].setDepth(3)

        ## load the tile palette
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0

        pyxel.image(1).load(0, 0, 'ressources/characters.png')
        self.charactersPalette = 1
        
        ## set the map renderer
        self.mapRenderer = TilemapRenderer(self.tilePalette)

# program entry
App()