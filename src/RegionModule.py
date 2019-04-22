from TilemapModule import *
from QuadTree import *


class Region():
    def __init__(self, x = 0, y = 0, w = 1, h = 1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.quadtree = None
        self.flagmap = None
        self.tilemapBase = None
        self.tilemapOverlay = None

    def adjustChild(self):
        if self.quadtree:
            self.quadtree.setTransform(self.x, self.y, self.w, self.h)

    def setTransform(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.adjustChild()

    def addEntity(self, entity):
        if self.quadtree and self.quadtree.overlap(entity):
            self.quadtree.addEntity(entity)

    def removeEntity(self, entity):
        if self.quadtree and self.quadtree.overlap(entity):
            self.quadtree.removeEntity(entity)

    def load(self, files, transparency = 0):
        w = self.w//16
        h = self.h//16
        self.flagmap = FlagMap(files[0])
        self.tilemapBase = Tilemap.ImportMap(files[1], w, h, self.flagmap)
        self.tilemapOverlay = Tilemap.ImportLayer(files[2], w, h, self.flagmap, transparency)

    def setDepth(self, depth):
        if not self.quadtree:
            self.quadtree = TreeNode()
            self.quadtree.setTransform(self.x, self.y, self.w, self.h)
            for i in range(1, depth):
                self.quadtree.split()
            return
        d = self.quadtree.getDepth()
        if d < depth:
            for i in range(1, depth - d):
                self.quadtree.split()
        elif d > depth:
            for i in range(1, d - depth):
                self.quadtree.merge()


    # DEBUG
    def print(self):
        print('region')
        print('tilemap s: ' + str(self.tilemapBase.sizeX) + ' ' + str(self.tilemapBase.sizeY))
        print('overlay s: ' + str(self.tilemapOverlay.sizeX) + ' ' + str(self.tilemapOverlay.sizeY))
        print('quadtree : ')
        self.quadtree.print()

    def __str__(self):
        msg = '\nregion' + '\n'
        msg += 'tilemap s: ' + str(self.tilemapBase.sizeX) + ' ' + str(self.tilemapBase.sizeY) + '\n'
        msg += 'overlay s: ' + str(self.tilemapOverlay.sizeX) + ' ' + str(self.tilemapOverlay.sizeY) + '\n'
        msg += 'quadtree : ' + '\n'
        msg += str(self.quadtree) + ' depth: ' + str(self.quadtree.getDepth())
        return msg




