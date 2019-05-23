from Region import *
from EntityFactory import *
from SpriteBank import *
from TerrainBank import *

import math

class World(Box):
    def __init__(self, regionsArray):
        super(World, self).__init__()
        self.regionsArray = regionsArray
        self.position = Vector2f(0,0)
        self.size = 16 * 50 * Vector2f(regionsArray.x, regionsArray.y)
        self.regionSize = 16 * Vector2f(50, 50)
        self.regions = []

        o = Vector2f(-self.size.x / 2, -self.size.y / 2)
        for i in range(self.regionsArray.x):
            for j in range(self.regionsArray.y):
                self.regions.append(Region(o + Vector2f(i*self.regionSize.x, j*self.regionSize.y), self.regionSize, random.randint(0,2147483647)))

        self.terrainBank = None
        self.terrainTransparency = -1
        self.factory = None
        self.dynamicEntities = set()
        self.scriptedEntities = set()

    def loadBanks(self, terrainFile, entityFile,terrainImageBank = 0, terrainImageTransparency = -1):
        self.terrainBank = TerrainBank(terrainFile, terrainImageBank)
        self.terrainTransparency = terrainImageTransparency
        self.factory = EntityFactory(entityFile)

    # REGION RELATED
    def updateRegions(self, loadBox, unloadBox):
        unloadIndexList = self.querryRegions(unloadBox)
        loadIndexList = self.querryRegions(loadBox)
        for index in unloadIndexList:
            if index in loadIndexList and self.regions[index].tilemap==None:
                print('load reg ' + str(index))
                self.regions[index].load(None, self.terrainBank.imageBank, self.terrainTransparency)
                self.regions[index].quadtree = TreeNode()
                self.regions[index].quadtree.setTransform(self.regions[index].position, self.regions[index].size)
                #self.regions[index].setDepth(4)
                #self.regions[index].randomPopulate(self.factory)

            elif not(index in loadIndexList) and self.regions[index].tilemap:
                print('unload reg ' + str(index))
                #self.regions[index].setDepth(0)
                del self.regions[index].tilemap
                del self.regions[index].quadtree
                self.regions[index].tilemap = None
                self.regions[index].quadtree = None

    def querryRegions(self, box):
        # compute corners region location
        ox = math.floor((box.position.x + 0.5*self.size.x) / (16*50))
        oy = math.floor((box.position.y + 0.5*self.size.y) / (16*50))
        fx = math.floor((box.position.x + box.size.x + 0.5*self.size.x) / (16*50)) + 1
        fy = math.floor((box.position.y + box.size.y + 0.5*self.size.y) / (16*50)) + 1

        # clamp corners
        ox = min(max(ox, 0), self.regionsArray.x)
        oy = min(max(oy, 0), self.regionsArray.y)
        fx = min(max(fx, 0), self.regionsArray.x)
        fy = min(max(fy, 0), self.regionsArray.y)

        #print(str(ox) + ' ' + str(oy) + ' ' + str(fx) + ' ' + str(fy))

        # result compute
        regionIndexList = []
        for i in range(ox, fx):
            for j in range(oy, fy):
                index = i*self.regionsArray.y + j
                if index < len(self.regions):
                    regionIndexList.append(index)
        return regionIndexList

    def regionTwoDimensionalIndex(self, index):
        return Vector2i(math.floor(index/self.regionsArray.y), index%int(self.regionsArray.y))


    # ENTITY RELATED
    def addEntity(self, entity):
        region = self.querryRegions(Box(entity.position))
        if(region != None):
            self.regions[region[0]].addEntity(entity)
        else:
            print("ERROR : World.addEntity : entity outside world bounds")

    def removeEntity(self, entity):
        region = self.querryRegions(Box(entity.position))
        if(region != None):
            self.regions[region[0]].removeEntity(entity)

    def isValidEntity(self, entity):
        region = self.querryRegions(Box(entity.position))
        if region != None and self.regions[region[0]].quadtree:
            return True
        return False

    def querryEntities(self, box):
        result = set()
        regionIndexList = self.querryRegions(box)
        for index in regionIndexList:
            result = result | self.regions[index].querryEntities(box)
        return result

    def addDynamicEntity(self, entity):
        self.dynamicEntities.add(entity)

    def removeDynamicEntity(self, entity):
        try:
            self.dynamicEntities.remove(entity)
        except:
            pass

    def addScriptedEntity(self, entity):
        self.scriptedEntities.add(entity)

    def removeScriptedEntity(self, entity):
        try:
            self.scriptedEntities.remove(entity)
        except:
            pass

    ## PHYSICS RELATED
    # remove all fake entities placed during physics update
    def clearPhysicsEntities(self, box):
        regionIndexList = self.querryRegions(box)
        for index in range(len(self.regions)):
            self.regions[index].clearPhysicsEntities()

    # add a physics entity to the node
    def addPhysicsEntity(self, entity):
        region = self.querryRegions(Box(entity.position))
        if(region != None):
            tree = self.regions[region[0]].quadtree
            if tree:
                return tree.addPhysicsEntity(entity)
            else:
                entity.entity = None
        return None

    # same as 'querryEntities', but return in addition all physicsEntities
    def querryPhysicsEntities(self, box):
        result = set()
        regionIndexList = self.querryRegions(box)
        for index in regionIndexList:
            result = result | self.regions[index].querryPhysicsEntities(box)
        return result


    #DEBUG
    def print(self):
        print('---WORLD---')
        for r in self.regions:
            print(str(r))

    def __str__(self):
        msg = '---WORLD---\n'
        for r in self.regions:
            msg += str(r) + '\n'
        return msg

