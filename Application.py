# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import random
import pyxel
from InputManager import *
from Inputs import *

#from TilemapModule import *
from World import *
from PlayerModule import *
from Entity import *

from TileMap import *
from Renderer import *
from Camera import *


pyxel.DEFAULT_PALETTE[11] = 0x00BC2C

# application class
class App:
    application = None
    def __init__(self):
        application = self

        #global initialization
        pyxel.init(255,255, caption="Nearym Quest", scale=3)
        self.debugOverlay = False
        self.camera = Camera()
        self.streamingArea = Box()
        self.streamingArea.size = Vector2f(512, 512)
        self.renderer = Renderer()
        random.seed(0)

        # Event Manager
        self.inputManager = InputManager()
        self.inputManager.addEvent(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_F1], 'debug'))
        self.LoadMap()

        #player
        self.player = Player()
        self.player.RegisterEvents(self.inputManager)
        self.player.position.x = 0
        self.player.position.y = 0

        self.draw_count = 0

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)


    def update(self):
        self.inputManager.update()
        #self.mapRenderer.update()
        self.player.UpdateControls(self.world.position + 0.5*self.world.size, self.world.position - 0.5*self.world.size)
        self.camera.center = self.player.center
        self.streamingArea.center = self.player.center
        self.world.updateRegions(self.streamingArea)

        if self.inputManager.CheckEventTrigger('debug'):
            self.debugOverlay = not self.debugOverlay


    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.draw_count += 1

        self.player.updateAnimation()

        #debug overlay or standard rendering
        if self.debugOverlay:
            self.renderer.renderTileMap(self.camera, self.world, 16 )
            self.renderer.renderColliderOverlay(self.camera, self.world)
            self.renderer.renderFlagOverlay(self.camera, self.world)
        else:
            self.renderer.renderTileMap(self.camera, self.world)
        self.renderer.renderPlayer(self.camera, self.player)

        #creepy hud face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)

        #debug hud overlay
        if self.debugOverlay:
            pyxel.rect(32, 236, 74, 245, 6)
            pyxel.rectb(32, 236, 74, 245, 5)
            pyxel.text(35,238, 'position', 0)

            pyxel.rect(32, 246, 128, 254, 6)
            pyxel.rectb(32, 246, 128, 254, 5)
            pyxel.text(35,248, str(self.player.position), 0)

            pyxel.rect(212, 236, 254, 245, 6)
            pyxel.rectb(212, 236, 254, 245, 5)
            pyxel.text(216,238, 'region', 0)

            pyxel.rect(160, 246, 254, 254, 6)
            pyxel.rectb(160, 246, 254, 254, 5)

            region = self.world.querryRegions(Box.fromPoint(self.player.center))[0]
            regionPos = self.world.regionTwoDimensionalIndex(region)
            pyxel.text(164,248, str(region) + ' : ' + str(regionPos), 0)


    def LoadMap(self):
        # load tile palettes
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0
        pyxel.image(1).load(0, 0, 'ressources/characters.png')
        self.charactersPalette = 1
        
        # load world
        self.world = World(Vector2i(257,257))
        self.world.loadBanks("ressources/map2tileset.json", self.tilePalette, 0)

# program entry
App()