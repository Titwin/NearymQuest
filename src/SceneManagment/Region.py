import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')

from TileMap import *
from QuadTree import *
from Sprite import *

class Region(Box):
    def __init__(self, position, size, seed):
        super(Region, self).__init__()
        self.position = position
        self.size = size
        self.quadtree = None
        self.dynamicEntities = []
        self.tilemap = None
        self.seed = seed

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
        random.seed(self.seed)
        w = math.floor(self.size.x/16)
        h = math.floor(self.size.y/16)
        self.tilemap = TileMap(Vector2i(w, h))
        self.tilemap.randomBackground([50,50,50,50,50,50, 20,20,20,20,20,20, 66,66, 82], None, imageBank, transparency)
        if file:
            self.tilemap.importFromFile(file, imageBank, transparency)

    def randomPopulate(self, factory):
        random.seed(self.seed)
        for t in self.tilemap.tiles:
            if (t.materials[0].index in (50,20)):
                dice = random.randrange(30)
                if dice < 3:
                    tree = factory.instanciate('smallTree')
                    tree.position = self.position + 16*t.position
                    self.addEntity(tree)
                elif dice < 6:
                    rock = factory.instanciate('bigRock')
                    rock.position = self.position + 16*t.position
                    self.addEntity(rock)
                elif dice < 9:
                    rock = factory.instanciate('smallRock')
                    rock.position = self.position + 16*t.position
                    self.addEntity(rock)


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

    def querryTiles(self, box):
        # compute corners region location
        ox = math.floor((box.position.x - self.position.x) / 16)
        oy = math.floor((box.position.y - self.position.y) / 16)
        fx = math.floor((box.position.x - self.position.x + box.size.x) / 16) + 1
        fy = math.floor((box.position.y - self.position.y + box.size.y) / 16) + 1

        # clamp corners
        ox = min(max(ox, 0), self.tilemap.size.x)
        oy = min(max(oy, 0), self.tilemap.size.y)
        fx = min(max(fx, 0), self.tilemap.size.x)
        fy = min(max(fy, 0), self.tilemap.size.y)

        #print(str(ox) + ' ' + str(oy) + ' ' + str(fx) + ' ' + str(fy))

        result = []
        for j in range(oy, fy):
            for i in range(ox, fx):
                result.append(i + j*self.tilemap.size.x)
        return result


    def querryEntities(self, box):
        if self.quadtree:
            return self.quadtree.querryEntities(box)
        else:
            return []


    # DEBUG
    def print(self):
        print('region')
        print('seed : ' + str(self.seed))
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
        msg += 'seed : ' + str(self.seed) + '\n'
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




