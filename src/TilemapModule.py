
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
                index = random.choice([50,50,50,50,50,50, 20,20,20,20,20,20, 66,66, 82])
                data.append(Tile(x,y, Material(index, 0, random.choice([1,-1]), random.choice([1,-1]) if index==50 else 1)))
                if(index == 50 and random.randint(0, 20) == 0):
                    data[x+y*sizeX].materials.append(Material(random.choice([80,80,80,81]), 0, random.choice([1,-1]), 1, 0))

        for path in paths:
            my_data = genfromtxt(path, delimiter=',')
            for y in range(sizeY):
                #s = ""
                for x in range(sizeX):
                    matIndex = my_data[y,x]
                    if(matIndex!=-1):
                        data[x+y*sizeX].materials.append(Material(matIndex, 0, 1,1, 0))
                    #s=s+str(my_data[x,y])+" "
                #print(s+"\n")
        return Tilemap(sizeX, sizeY, data)

    @staticmethod        
    def ImportLayer(paths, sizeX, sizeY, transparency):
        data = []
        for y in range(sizeY):
            for x in range(sizeX):
                data.append(Tile(x,y))

        for path in paths:
            my_data = genfromtxt(path, delimiter=',')
            for y in range(sizeY):
                for x in range(sizeX):
                    matIndex = my_data[y,x]
                    if(matIndex!=-1):
                        data[x+y*sizeX].materials.append(Material(matIndex, 0, 1, 1, transparency))
        return Tilemap(sizeX, sizeY, data)

        
class TilemapRenderer:
    def __init__(self, palette):
        self.palette = palette
        self.TILE_SIZE = 16

    def update(self):
        pass

    def draw(self, tilemap, a, b, exceptx = -10, excepty = -10, exceptw = 1, excepth = 1):
        da = a - math.floor(a/16)*16
        db = b - math.floor(b/16)*16

        for dy in range(0, 17):
            y = math.floor((b-db)/16) + dy
            if y < tilemap.sizeY and y >= 0:
                for dx in range(0, 17):
                    x = math.floor((a-da)/16) + dx
                    if x < tilemap.sizeX and x >= 0:

                        if x<exceptx or x>exceptx+exceptw or y<excepty or y>excepty+excepth:
                            tile = tilemap[(x, y)]
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
                        else:
                            self.dithering(tilemap[(x, y)], dx*self.TILE_SIZE - da,dy*self.TILE_SIZE - db)



    def dithering(self, tile, x, y):
        patern = [(0,0), (4,0), (8,0), (12,0),
                  (2,1), (6,1), (10,1), (14,1), 
                  (0,2), (4,2), (8,2), (12,2),
                  (2,3), (6,3), (10,3), (14,3),

                  (0,4), (4,4), (8,4), (12,4),
                  (2,5), (6,5), (10,5), (14,5), 
                  (0,6), (4,6), (8,6), (12,6),
                  (2,7), (6,7), (10,7), (14,7),

                  (0,8), (4,8), (8,8), (12,8),
                  (2,9), (6,9), (10,9), (14,9), 
                  (0,10), (4,10), (8,10), (12,10),
                  (2,11), (6,11), (10,11), (14,11),

                  (0,12), (4,12), (8,12), (12,12),
                  (2,13), (6,13), (10,13), (14,13), 
                  (0,14), (4,14), (8,14), (12,14),
                  (2,15), (6,15), (10,15), (14,15)]


        for m in tile.materials:
            if m.index != Material.MATERIAL_TRANSAPARENT:
                for c in patern:
                    pyxel.blt(x + c[0], y + c[1], self.palette, (m.indexX)*self.TILE_SIZE + c[0], (m.indexY)*self.TILE_SIZE + c[1], 1,1, m.transparency)
                    #pyxel.pix(x + c[0], y + c[1], self.palette.get(16*tile.x + coor.x, 16*tile.y + coor.y))