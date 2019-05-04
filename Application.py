# permit application to import module from 'src' folder
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import random
import pyxel
import InputManagerModule
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
        self.camera = Camera()
        self.renderer = Renderer()
        #self.camera.position = Vector2f(-128,-128)
        random.seed(0)

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
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
        self.world.updateRegions(self.camera)


    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.draw_count += 1

        self.player.updateAnimation()
        self.renderer.renderTileMap(self.camera, self.world)
        self.renderer.renderPlayer(self.camera, self.player)


        #creepy face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)


    def LoadMap(self):
        # load tile palettes
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0

        pyxel.image(1).load(0, 0, 'ressources/characters.png')
        self.charactersPalette = 1
        
        # load world
        self.world = World(Vector2i(3,3))
        self.world.loadBanks("ressources/map2tileset.json", self.tilePalette, 0)
        self.world.updateRegions(self.camera)

# program entry
App()