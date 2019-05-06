from Region import *
from FlagBank import *
from ColliderBank import *
from EntityFactory import *

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

        self.flagBank = None
        self.colliderBank = None
        self.bankFileName = None
        self.terrainBank = 0
        self.terrainTransparency = -1
        self.factory = EntityFactory()

    def loadBanks(self, file, terrainImageBank = 0, terrainImageTransparency = -1):
        self.bankFileName = file
        self.terrainBank = terrainImageBank
        self.terrainTransparency = terrainImageTransparency
        self.flagBank = FlagBank(file)
        self.colliderBank = ColliderBank(file)

    # REGION RELATED
    def updateRegions(self, box):
        regionIndexList = self.querryRegions(box)
        for index in range(len(self.regions)):
            if index in regionIndexList and self.regions[index].tilemap==None:
                print('loading region ' + str(index))
                file = None
                #if self.regions[index].overlap(Box.origin()):
                #    file = 'ressources/map2.json'
                self.regions[index].load(file, self.terrainBank, self.terrainTransparency)
                self.regions[index].setDepth(3)
                self.regions[index].randomPopulate(self.factory)

            elif not(index in regionIndexList) and self.regions[index].tilemap:
                print('unload region ' + str(index))
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
    def addEntity(self, entity, dynamic = False):
        region = self.querryRegions(Box.fromPoint(entity.position))
        if(region != None):
            self.regions[region[0]].addEntity(entity, dynamic)

    def removeEntity(self, entity):
        region = self.querryRegions(Box.fromPoint(entity.position))
        if(region != None):
            self.regions[region[0]].removeEntity(entity)

    def querryEntities(self, box):
        result = []
        regionIndexList = self.querryRegions(box)
        for index in regionIndexList:
            result.extend(self.regions[index].querryEntities(box))
        return result

    def updateDynamicEntity(self, entity, newPosition):
        self.removeEntity(entity)
        entity.position = newPosition
        self.addEntity(entity)

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

