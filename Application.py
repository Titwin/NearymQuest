# permit application to import module from 'src' folder
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/InputSystem')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Physics')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Rendering')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/SceneManagment')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Terrain')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Scripting')

# import modules
import random
import pyxel

from InputManager import *
from Inputs import *

#from TilemapModule import *
from World import *
from Entity import *
from Renderer import *
from Camera import *
from Color import *
from Physics import *

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
        self.streamingArea.center = Vector2f(0,0)
        self.renderer = Renderer()
        self.physics = Physics()
        random.seed(0)

        # Event Manager
        self.inputManager = InputManager()
        self.inputManager.addInput(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_F1], 'debug'))

        # world and player
        self.LoadMap()

        self.draw_count = 0


        reg = self.world.querryRegions(Box(self.player.position))
        for r in reg:
            self.world.regions[r].print()


        # has to be completely at the end of init
        #pyxel.run(self.update, self.draw)
        pyxel.run_with_profiler(self.update, self.draw)


    def update(self):
        self.inputManager.update()
        self.camera.center = self.player.center
        self.streamingArea.center = self.player.center
        self.world.updateRegions(self.streamingArea, self.streamingArea.inflated(Vector2f(100,100)))

        if self.inputManager.CheckInputTrigger('debug'):
            self.debugOverlay = not self.debugOverlay

        deadEntities = []
        for entity in self.world.scriptedEntities:
            if not self.world.isValidEntity(entity):
                deadEntities.append(entity)
                continue

            scripts = entity.getComponent('Scripts')
            if scripts:
                for s in scripts:
                    s.update()
        for e in deadEntities:
            self.world.removeEntity(e)
            self.world.removeDynamicEntity(e)
            self.world.removeScriptedEntity(e)

        # physics
        if self.debugOverlay:
            self.physics.renderer = self.renderer
        else:
            self.physics.renderer = None
        self.physics.update(self.world)



    def draw(self):
        # clear the scene
        pyxel.cls(Color.Black)
        self.renderer.resetStat()

        #debug overlay or standard rendering
        if self.debugOverlay:
            self.renderer.renderTileMap(self.camera, self.world, 16)
            self.renderer.renderColliderOverlay(self.camera, self.world)
            self.renderer.renderFlagOverlay(self.camera, self.world)
        else:
            self.renderer.renderTileMap(self.camera, self.world)

        # same for entities
        self.renderer.renderEntities(self.camera, self.world)
        self.renderer.drawGizmos(self.camera)
        if self.debugOverlay:
            self.renderer.renderEntitiesPivot(self.camera, self.world)

        #debug hud overlay
        if self.debugOverlay:
            self.drawDebugHUD()
        self.renderer.gizmos.clear()

        reg = self.world.querryRegions(Box(self.player.position))
        for r in reg:
            self.world.regions[r].quadtree.draw(self.camera, Color.Red)


    def LoadMap(self):
        # load world
        self.world = World(Vector2i(257,257))
        Entity.WORLD = self.world
        self.world.loadBanks("ressources/map3tileset.json", 'ressources/animationBank.json', 0, 0)
        self.world.updateRegions(self.streamingArea, self.streamingArea)

        self.player = self.world.factory.instanciate("player")
        #self.player.addComponent('Scripts', [PlayerController()])
        self.player.position = self.streamingArea.center
        self.world.addEntity(self.player)

        for i in range(-5,6):
            for j in range(-5,6):
                if i==0 and j==0:
                    continue
                dog = self.world.factory.instanciate("wolf")
                dog.position = self.player.position + Vector2f(64*i, 64*j)
                dog.getComponent('Scripts')[0].target = self.player


    def drawDebugHUD(self):
        # player position
        pyxel.rect(32, 236, 74, 245, 6)
        pyxel.rectb(32, 236, 74, 245, 5)
        pyxel.text(35,238, 'position', 0)

        pyxel.rect(32, 246, 128, 254, 6)
        pyxel.rectb(32, 246, 128, 254, 5)
        pyxel.text(35,248, str(Vector2f(math.floor(10*self.player.position.x)/10.0, math.floor(10*self.player.position.y)/10.0)), 0)

        # player actual region
        pyxel.rect(212, 236, 254, 245, 6)
        pyxel.rectb(212, 236, 254, 245, 5)
        pyxel.text(216,238, 'region', 0)

        pyxel.rect(160, 246, 254, 254, 6)
        pyxel.rectb(160, 246, 254, 254, 5)

        region = self.world.querryRegions(Box.fromPoint(self.player.center))[0]
        regionPos = self.world.regionTwoDimensionalIndex(region)
        pyxel.text(164,248, str(region) + ' : ' + str(regionPos), 0)

        # rendering statistics
        pyxel.rect(212, 0, 254, 8, 6)
        pyxel.rectb(212, 0, 254, 8, 5)
        pyxel.text(216,2, 'rendering', 0)

        pyxel.rect(196, 9, 254, 17, 6)
        pyxel.rectb(196, 9, 254, 17, 5)
        pyxel.text(200,11, 'tiles ' + str(self.renderer.tileDrawn), 0)

        pyxel.rect(196, 18, 254, 26, 6)
        pyxel.rectb(196, 18, 254, 26, 5)
        pyxel.text(200,20, 'sptites ' + str(self.renderer.entitiesDrawn), 0)

        pyxel.rect(196, 27, 254, 35, 6)
        pyxel.rectb(196, 27, 254, 35, 5)
        pyxel.text(200,29, 'total ' + str(self.renderer.primitiveDrawn), 0)


# program entry
App()