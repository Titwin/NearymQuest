import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')

from TileMap import *
from QuadTree import *

# a class to define a region of the world
# contain :
#    - position : legacy of box, the region size in pixel
#    - size : legacy of box, the region size in pixel
#    - quadtree : the spatial partitioning tree, containing all the region entities
#    - dynamicEntities : a list of all dynamic entities in the region
#    - tilemap : the tilemap representing the terrain
#    - seed : the seed to initialize the random number generator
class Region(Box):
    # constructor
    def __init__(self, position, size, seed):
        super(Region, self).__init__()
        self.position = position
        self.size = size
        self.quadtree = None
        self.tilemap = None
        self.seed = seed

    ## INITIALIZATION SPECIFIC
    # change region position and size
    # be carefull to only use this before any entities to be added into the region.
    # in effect all entities already placed in the quadtree will not be updated, breaking everything
    # parameter : position : the new node position (top left corner)
    # parameter : size : the new size of the node
    def setTransform(self, position, size):
        self.position = position
        self.size = size
        if self.quadtree:
            self.quadtree.setTransform(self.position, self.size)

    # initialize the quadtree to be a tree of specified depth
    # if the current quadtree depth is less than specify, split the tree to reach the target
    # if the current quadtree depth is more than specify, merge the tree to reach the target
    # parameter : depth : the target depth of the tree
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

    # initialize the tilemap
    # generate a random background in the tilemap and after, load the tilemap depending on file (if specified)
    # parameter : file : the file to load the tilemap from. default is None (no import)
    # parameter : imageBank : the image bank to specified to the tilemap initialization, default is 0
    # parameter : transparency : the transparency color to specified to the tilemap, default is -1 (no transparency color)
    def load(self, file = None, imageBank = 0, transparency = -1):
        random.seed(self.seed)
        w = math.floor(self.size.x/16)
        h = math.floor(self.size.y/16)
        self.tilemap = TileMap(Vector2i(w, h))
        self.tilemap.randomBackground([50,50,50,50,50,50, 20,20,20,20,20,20, 66,66, 82], None, imageBank, transparency)
        if file:
            self.tilemap.importFromFile(file, imageBank, transparency)

    # randomly generate entity to populate the region
    # parameter : factory : the entity factory for entities instanciation
    def randomPopulate(self, factory):
        if factory:
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

    ## ENTITY RELATED
    # add en entity in the region
    # be notice that if the quadtree is not yet initialize, the entity will not be added to the region
    # parameter : entity : the entity to add
    # parameter : dynamic : specify if the entity created is dynamic or not
    def addEntity(self, entity):
        if self.quadtree and self.quadtree.overlap(entity):
            self.quadtree.addEntity(entity)

    # remove an entity from the region
    # parameter : entity : the entity to remove
    def removeEntity(self, entity):
        if self.quadtree and self.quadtree.overlap(entity):
            try:
                self.quadtree.removeEntity(entity)
            except Exception as e:
                pass

    # return all entitities that potentially overlap a box
    # it just call the function of the same name on the quadtree root
    # parameter : box : the box to check the region against
    # return a list of entities that potentially overlap
    def querryEntities(self, box):
        if self.quadtree:
            return self.quadtree.querryEntities(box)
        else:
            return []


    ## TILEMAP RELATED
    # return all tiles indexes of tilemap that overlap a box
    # parameter : box : the box to check the region against
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

        # create result index list
        result = []
        for j in range(oy, fy):
            for i in range(ox, fx):
                result.append(i + j*self.tilemap.size.x)
        return result




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




