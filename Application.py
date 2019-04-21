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

        # Event Manager
        self.inputManager = InputManagerModule.InputManager()
        #map
        self.LoadMap()

        # QuadTree structure init
        self.quadtree = TreeNode()
        self.quadtree.split()
        self.quadtree.split()
        self.quadtree.setTransform(0,0, 50*16, 50*16)

        e = Entity()
        e.x, e.y = 5, 5
        self.quadtree.addEntity(e)

        self.quadtree.print()


        #player
        self.player = Player()
        self.player.RegisterEvents(self.inputManager)
        self.player.x = 256
        self.player.y = 256
        self.draw_count = 0

        # has to be completely at the end of init
        pyxel.run(self.update, self.draw)

    def update(self):
        self.inputManager.update()
        self.mapRenderer.update()
        self.player.UpdateControls(self.map.sizeX*16, self.map.sizeY*16)

    def draw(self):
        # clear the scene
        pyxel.cls(0)
        self.draw_count += 1

        # draw map
        camX = max(self.player.x-128, 0)
        camY = max(self.player.y-128, 0)
        self.mapRenderer.draw(self.map, camX, camY)

        # handle character
        self.drawPlayer()



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