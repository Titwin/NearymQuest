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

# import modules
import random
import pyxel
from InputManager import *
from Inputs import *

#from TilemapModule import *
from World import *
from PlayerModule import *
from Entity import *

from Sprite import *
from PhysicsSweptBox import *

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
        pyxel.init(255,255, caption="Nearym Quest", scale=3, fps=30)
        self.debugOverlay = False
        self.camera = Camera()
        self.streamingArea = Box()
        self.streamingArea.size = Vector2f(512, 512)
        self.streamingArea.center = Vector2f(0,0)
        self.renderer = Renderer()
        random.seed(0)

        # Event Manager
        self.inputManager = InputManager()
        self.inputManager.addInput(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_F1], 'debug'))
        

        # world and player
        self.LoadMap()
        self.characterBank = SpriteBank(self.charactersPalette)
        self.player = Player(self.characterBank)
        self.player.RegisterEvents(self.inputManager)
        self.player.center = self.streamingArea.center
        self.player.addComponent('RigidBody', RigidBody())
        self.world.addDynamicEntity(self.player)

        # debug
        r = self.world.querryRegions(self.player)
        self.world.regions[r[0]].print()

        self.draw_count = 0

        # has to be completely at the end of init
        #pyxel.run(self.update, self.draw)
        pyxel.run_with_profiler(self.update, self.draw)


    def update(self):
        self.inputManager.update()
        self.player.position = self.player.UpdateControls(self.world.position + 0.5*self.world.size, self.world.position - 0.5*self.world.size)
        self.camera.center = self.player.center
        self.streamingArea.center = self.player.center
        self.world.updateRegions(self.streamingArea, self.streamingArea.inflated(Vector2f(100,100)))

        if self.inputManager.CheckInputTrigger('debug'):
            self.debugOverlay = not self.debugOverlay

        self.updatePhysics()


    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.renderer.resetStat()
        self.draw_count += 1

        self.player.updateAnimation()

        #debug overlay or standard rendering
        if self.debugOverlay:
            self.renderer.renderTileMap(self.camera, self.world, 16 )
            self.renderer.renderColliderOverlay(self.camera, self.world)
            self.renderer.renderFlagOverlay(self.camera, self.world)
        else:
            self.renderer.renderTileMap(self.camera, self.world)

        # same for entities
        self.renderer.renderEntities(self.camera, self.world)
        if self.debugOverlay:
            self.renderer.renderEntitiesColliders(self.camera, self.world)
            self.renderer.renderEntitiesPivot(self.camera, self.world)


        #creepy hud face
        pyxel.blt(0,14*16, self.charactersPalette, 4*16, 1*16, 32,32, 11)

        #debug hud overlay
        if self.debugOverlay:
            self.drawDebugHUD()


    def LoadMap(self):
        # load tile palettes
        pyxel.image(0).load(0, 0, 'ressources/map3tileset.png')
        self.tilePalette = 0
        pyxel.image(1).load(0, 0, 'ressources/characters.png')
        self.charactersPalette = 1
        
        # load world
        self.world = World(Vector2i(257,257))
        self.world.loadBanks("ressources/map3tileset.json", self.tilePalette, 0)
        self.world.updateRegions(self.streamingArea, self.streamingArea)
        Entity.WORLD = self.world



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

    def updatePhysics(self):
        # predict transforms and creating bounding swept volume
        fakeBoxList = []
        quadtreeNode = []
        for entity in self.world.dynamicEntities:
            rb = entity.getComponent('RigidBody')
            if rb:
                fakeBox = PhysicsSweptBox(entity, rb.velocity)
                fakeBoxList.append(fakeBox)
                #self.world.removeEntity(entity)
                quadtreeNode.append(self.world.addPhysicsEntity(fakeBox))

        # detect pairs
        for fb in fakeBoxList:
            neighbours = self.world.querryPhysicsEntities(fb)
            for e in neighbours:
                if id(fb)!=id(e) and id(fb.entity)!=id(e) and fb.overlap(e):
                    print("collision : " + str(e))
        print("\n")


        # compute contacts

        # solve constraint

        # integrate position

        # clear
        for n in quadtreeNode:
            if n:
                n.clearPhysicsEntities()
        #for fb in fakeBoxList:
        #    self.world.addEntity(fb.entity)

# program entry
App()