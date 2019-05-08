from Tile import *

import json
import random

class TileMap:
    def __init__(self, size):
        self.size = size
        self.tiles = []
        for y in range(self.size.y):
            for x in range(self.size.x):
                self.tiles.append(Tile(Vector2i(x, y)))
        self.layersName = {}

    def __del__(self):
        self.tiles.clear()
        self.layersName.clear()

    def importFromFile(self, file, imageBank = 0, transparency = -1):
        offset = self.getLayerCount()
        with open(file) as json_file:
            data = json.load(json_file)
            for l in data['layers']:
                layerIndex = l['id'] + offset
                self.layersName[layerIndex] = l['name']
                for y in range(self.size.y):
                    for x in range(self.size.x):
                        i = l['data'][y*self.size.x + x]
                        if i!=0:
                            index = (i & 0x000001FF)                     # index range is from [1, 256], 0 is for empty
                            flipx = 1 if ((i & 0x80000000)==0) else -1   # x fliped
                            flipy = 1 if ((i & 0x40000000)==0) else -1   # y fliped
                            self.tiles[y*self.size.x + x].add(layerIndex, Material(imageBank, index-1, Vector2i(flipx,flipy), transparency))

    def randomBackground(self, choice1 = [17], choice2 = None, imageBank = 0, transparency = -1):
        self.layersName[0] = 'randomBackground0'
        self.layersName[1] = 'randomBackground1'
        for y in range(self.size.y):
            for x in range(self.size.x):
                index = random.choice(choice1)
                flip = Vector2i(random.choice([1,-1]), random.choice([1,-1]) if index==choice1[0] else 1)
                self.tiles[y*self.size.x + x].add(0, Material(imageBank, index, flip, transparency))
                if(choice2 != None and index == choice1[0] and random.randint(0, 20) == 0):
                    index = random.choice(choice2)
                    flip = Vector2i(random.choice([1,-1]), 1)
                    self.tiles[y*self.size.x + x].add(1, Material(imageBank, index, flip, transparency))

    def getLayerCount(self):
        return len(self.layersName)


    def queryTiles(self, box):
        overlaping = []
        o = box.position//16
        for i in range(0, box.size.x//16):
            for j in range(0, box.size.y//16):
                overlaping.append((o.x + i, o.y + j))
        return overlaping
    #



    # DEBUG
    def print(self):
        print('Tilemap')
        print('   size : ' + str(self.size))
        print('   layers : ' + str(self.getLayerCount()))
        for key, value in self.layersName.items():
            print('      ' + str(key) + " : " + str(value))

    def __str__(self):
        return 'Tilemap, size : ' + str(self.size) + ', layers count : ' + str(self.getLayerCount())
