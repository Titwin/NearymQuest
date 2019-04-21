
import numpy as np #for matrices
from numpy import genfromtxt #for csv import
import math
import pyxel
import random

class Material:
    MATERIAL_TRANSAPARENT = -1
    #_palette
    #_index
    def __init__(self, index,palette = 0, flipX = 1, flipY = 1, transparency = None):
        self._palette = palette
        self._index = index
        self._flipX = flipX
        self._flipY = flipY
        self._transparency = transparency

    @property
    def palette(self):
        return self._palette
    @property
    def index(self):
        return self._index
    @property
    def indexX(self):
        return self._index%16    
    @property
    def indexY(self):
        return self._index//16     
    @property
    def flipX(self):
        return self._flipX
    @property
    def flipY(self):
        return self._flipY
    @property
    def transparency(self):
        return self._transparency

class Tile:
    #posX
    #posY
    #materials
    #flags
    def __init__(self, x, y, material=None):
        self._x = x
        self._y = y
        self._materials = []
        if material!=None:
            self._materials.append(material)
    
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y

    @property
    def materials(self):
        return self._materials


class Tilemap:
    resolutionX = 32
    resolutionY = 32
    #int _sizeX
    #int _sizeY
    def __init__(self, sizeX, sizeY, data = []):
        self._sizeX = sizeX
        self._sizeY = sizeY
        
        self.map = data
        if len(data) == 0:
            for y in range(sizeY):
                for x in range(sizeX):
                    self.map.append(Tile(x,y))
    
    @property
    def sizeX(self):
        return self._sizeX
    @property
    def sizeY(self):
        return self._sizeY

    def ValidTile(self,x,y):
        return  x>=0 and x<self.sizeX and y>=0 and x<self.sizeY

    def __getitem__(self, xy):
        if self.ValidTile(xy[0],xy[1]):
            return self.map[xy[0]+xy[1]*self.sizeX]
        else:
            pass

    @staticmethod        
    def ImportMap(paths, sizeX, sizeY):
        data = []
        for y in range(sizeY):
            for x in range(sizeX):
                index = random.choice([50,50,50,50,50,50,50,50,50,50,66,66,82])
                data.append(Tile(x,y, Material(index, 0, random.choice([1,-1]), random.choice([1,-1]) if index==50 else 1)))
                if(index == 50 and random.randint(0, 20) == 0):
                    data[x+y*sizeX].materials.append(Material(51, 0, random.choice([1,-1]), 1, 0))

        for path in paths:
            my_data = genfromtxt(path, delimiter=',')
            for y in range(sizeY):
                #s = ""
                for x in range(sizeX):
                    matIndex = my_data[y,x]
                    if(matIndex!=-1):
                        data[x+y*sizeX].materials.append(Material(matIndex))
                    #s=s+str(my_data[x,y])+" "
                #print(s+"\n")
        return Tilemap(sizeX, sizeY, data)
        
class TilemapRenderer:
    def __init__(self, tilemap, palette):
        self.map = tilemap
        self.palette = palette
        self.posX = 0
        self.posY = 0
        self.TILE_SIZE = 16

    def update(self):
        pass
        #print("UpdateMap: nothing to do")

    def draw(self, a, b):
        da = a - math.floor(a/16)*16
        db = b - math.floor(b/16)*16

        #print (str(da) + ' ' + str(db) + ' ' + str(math.floor(a/16)) + ' ' + str(math.floor(b/16)))

        for dy in range(0, 17):
            y = math.floor((b-db)/16) + dy
            if y < self.map.sizeY and y >= 0:
                for dx in range(0, 17):
                    x = math.floor((a-da)/16) + dx
                    if x < self.map.sizeX and x >= 0:
                        tile = self.map[(x, y)]
                        if(len(tile.materials)>0):
                            for m in tile.materials:
                                if m.index != Material.MATERIAL_TRANSAPARENT:
                                    pyxel.blt(
                                        dx*self.TILE_SIZE - da, 
                                        dy*self.TILE_SIZE - db, 
                                        self.palette, 
                                        (m.indexX)*self.TILE_SIZE, (m.indexY)*self.TILE_SIZE, 
                                        self.TILE_SIZE*m.flipX, self.TILE_SIZE*m.flipY,
                                        m.transparency)

#    def draw(self):
#         for y in range(self.map.sizeY):
#            for x in range(self.map.sizeX):
#                tile = self.map[(x,y)]
#                if(len(tile.materials)>0):
#                    for m in tile.materials:
#                        mat = m.index
#                        if m.index != Material.MATERIAL_TRANSAPARENT:
#                            pyxel.blt(
#                                x*self.TILE_SIZE, y*self.TILE_SIZE, 
#                                self.palette, 
#                                (m.indexX)*self.TILE_SIZE, (m.indexY)*self.TILE_SIZE, 
#                                self.TILE_SIZE, self.TILE_SIZE)



