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
        self.loadingSteps = 0

    def __del__(self):
        del self.quadtree

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

    def generateTilemap(self):
        w = math.floor(self.size.x/16)
        h = math.floor(self.size.y/16)
        self.tilemap = TileMap(Vector2i(w, h))

    def generateTilemapBackground(self, imageBank = 0, transparency = -1):
        random.seed(self.seed)
        self.tilemap.randomBackground([50,50,50,50,50,50, 20,20,20,20,20,20, 66,66, 82], None, imageBank, transparency)

    def generateTilemapFromFile(self, file = None, imageBank = 0, transparency = -1):
        if file:
            self.tilemap.importFromFile(file, imageBank, transparency)

    # randomly generate entity to populate the region
    # parameter : factory : the entity factory for entities instanciation
    def randomPopulate(self, factory):
        random.seed(self.seed)
        if factory and self.quadtree:
            random.seed(self.seed)
            for t in self.tilemap.tiles:
                if (t.materials[0].index in (50,20)):
                    dice = random.randrange(30)
                    if dice < 3:
                        tree = factory.instanciate('smallTree')
                        tree.position = self.position + 16*t.position
                        self.quadtree.addEntity(tree)
                    elif dice < 6:
                        rock = factory.instanciate('bigRock')
                        rock.position = self.position + 16*t.position
                        self.quadtree.addEntity(rock)
                    elif dice < 9:
                        rock = factory.instanciate('smallRock')
                        rock.position = self.position + 16*t.position
                        self.quadtree.addEntity(rock)

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




