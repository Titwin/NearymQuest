from TileMap import *
from QuadTree import *


class Region(Box):
    def __init__(self, position, size):
        super(Region, self).__init__()
        self.position = position
        self.size = size
        self.quadtree = None
        self.dynamicEntities = []
        self.tilemap = None

    def adjustChild(self):
        if self.quadtree:
            self.quadtree.setTransform(self.position, self.size)

    def setTransform(self, position, size):
        self.position = position
        self.size = size
        self.adjustChild()

    def addEntity(self, entity, dynamic = False):
        if self.quadtree and self.quadtree.overlap(entity):
            self.quadtree.addEntity(entity)
        if dynamic:
            self.dynamicEntities.append(entity)

    def removeEntity(self, entity):
        if self.quadtree and self.quadtree.overlap(entity):
            try:
                self.quadtree.removeEntity(entity)
                self.dynamicEntities.removeEntity(entity)
            except Exception as e:
                pass

    def load(self, file, imageBank = 0, transparency = -1):
        w = math.floor(self.size.x/16)
        h = math.floor(self.size.y/16)
        self.tilemap = TileMap(Vector2i(w, h))
        self.tilemap.randomBackground([50,50,50,50,50,50, 20,20,20,20,20,20, 66,66, 82], [80,80,80,81], imageBank, transparency)
        if file:
            self.tilemap.importFromFile(file, imageBank, transparency)

    def setDepth(self, depth):
        if not self.quadtree:
            self.quadtree = TreeNode()
            self.quadtree.setTransform(self.position, self.size)
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
        if self.tilemap:
            print('tilemap s: ' + str(self.tilemap.size.x) + ' ' + str(self.tilemap.size.y))
        else:
            print('tilemap not loaded')
        if self.quadtree:
            print('quadtree : ')
            self.quadtree.print()
        else:
            print('quadtree not loaded')

    def __str__(self):
        msg = '\nregion' + '\n'
        if self.tilemap:
            msg += 'tilemap s: ' + str(self.tilemap.size.x) + ' ' + str(self.tilemap.size.y) + '\n'
        else:
            msg += 'tilemap not loaded\n'
        if self.quadtree:
            msg += 'quadtree : ' + '\n'
            msg += str(self.quadtree) + ' depth: ' + str(self.quadtree.getDepth())
        else:
            msg += 'quadtree not loaded\n'
        return msg




