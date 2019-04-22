# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
import InputManagerModule
from Events import *

from TilemapModule import *

from PlayerModule import *

from Entity import *
from WorldModule import *

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
        self.player.x = 256
        self.player.y = 128
        self.draw_count = 0

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls(self.world.regions[0].w - 8, self.world.regions[0].w - 8)

    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.draw_count += 1

        # draw map
        camX = max(self.player.x-128, 0)
        camY = max(self.player.y-128, 0)
        self.mapRenderer.draw(self.world.regions[0].tilemapBase, camX, camY)

        # handle character
        self.drawPlayer()

        # overlay pass
        overlay = self.world.regions[0].tilemapOverlay
        exception = overlay.queryTiles(self.player.x -8, self.player.y -8, self.player.x + 24, self.player.y + 24)
        self.mapRenderer.draw(overlay, camX, camY, exception)
        self.mapRenderer.dithering(overlay, camX, camY, self.player.x+8, self.player.y+8, exception)

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


    def drawPlayer(self):
        playerX = min(self.player.x, 128)
        playerY = min(self.player.y, 128)

        flip = self.player.orientationX
        animStart = 0
        animLength = 2
        animSpeed = 20
        if (self.player.dx == 0 and self.player.dy > 0):
            animStart = 4
            animLength = 4
            animSpeed = 4
            flip = 1
        elif(self.player.dx == 0 and self.player.dy < 0):
            animStart = 3
            animLength = 4
            animSpeed = 4
            flip = 1
        elif(self.player.dx > 0):
            animStart = 2
            flip = 1
            animLength = 4
            animSpeed = 4
        elif(self.player.dx < 0):
            animStart = 2
            flip = -1
            animLength = 4
            animSpeed = 4

        pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)

# program entry
App()