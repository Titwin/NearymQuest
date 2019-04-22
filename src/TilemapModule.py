
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
            return None

    def queryTiles(self, x1, y1, x2, y2):
        overlaping = []
        tilex = math.floor(x1/16)
        tiley = math.floor(y1/16)
        for i in range(0, math.floor(x2/16)+1 - tilex):
            for j in range(0, math.floor(y2/16)+1 - tiley):
                overlaping.append((tilex + i, tiley + j))
        return overlaping

    @staticmethod
    def presentInTileList(element, array):
        for e in array:
            if e == element:
                return True
        return False


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
                for x in range(sizeX):
                    matIndex = my_data[y,x]
                    if(matIndex!=-1):
                        data[x+y*sizeX].materials.append(Material(matIndex, 0, 1,1, 0))
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

    def draw(self, tilemap, camX, camY, exception = []):
        da = camX - math.floor(camX/self.TILE_SIZE)*self.TILE_SIZE
        db = camY - math.floor(camY/self.TILE_SIZE)*self.TILE_SIZE

        for dy in range(0, 17):
            y = math.floor((camY - db)/self.TILE_SIZE) + dy
            if y < tilemap.sizeY and y >= 0:
                for dx in range(0, 17):
                    x = math.floor((camX - da)/self.TILE_SIZE) + dx
                    if x < tilemap.sizeX and x >= 0:
                        if not Tilemap.presentInTileList((x, y), exception):
                            tile = tilemap[(x, y)]
                            if(tile and len(tile.materials)>0):
                                for m in tile.materials:
                                    if m.index != Material.MATERIAL_TRANSAPARENT:
                                        pyxel.blt(
                                            dx*self.TILE_SIZE - da, 
                                            dy*self.TILE_SIZE - db, 
                                            self.palette, 
                                            (m.indexX)*self.TILE_SIZE, (m.indexY)*self.TILE_SIZE, 
                                            self.TILE_SIZE*m.flipX, self.TILE_SIZE*m.flipY,
                                            m.transparency)

    def dithering(self, tilemap, camX, camY, centerX, centerY, exception, transparentColor = 0):
        if(len(exception) <= 0):
            return 

        da = camX - math.floor(camX/self.TILE_SIZE)*self.TILE_SIZE      # camera corner position x - (camera corner tile x) *16 -> residual x
        db = camY - math.floor(camY/self.TILE_SIZE)*self.TILE_SIZE      # camera corner position x - (camera corner tile x) *16 -> residual y

        camTileX = math.floor((camX-da)/self.TILE_SIZE)
        camTileY = math.floor((camY-db)/self.TILE_SIZE)

        ox = centerX - camX             # dithering center tile x - camera corner tile x
        oy = centerY - camY             # dithering center tile y - camera corner tile y

        for t in exception:
            dx = t[0] - camTileX
            dy = t[1] - camTileY
            tile = tilemap[t]

            if(tile and len(tile.materials) > 0):
                for i in range(0, 16):
                    for j in range(0, 16):
                        x, y = self.TILE_SIZE*dx + i - da, self.TILE_SIZE*dy + j - db                   # current pixel position on screen
                        convx, convy = 4*self.TILE_SIZE + int(x - ox), 7*self.TILE_SIZE + int(y - oy)   # convolution coordinates

                        for m in tile.materials:
                            if x < ox - 16 or x > ox + 15 or y < oy - 16 or y > oy + 15: # out of dithering patern
                                pyxel.blt(self.TILE_SIZE*dx+i - da, self.TILE_SIZE*dy+j - db, 
                                          self.palette, m.indexX*self.TILE_SIZE + i, m.indexY*self.TILE_SIZE + j, 
                                          m.flipX, m.flipY, m.transparency)

                            elif pyxel.image(self.palette).get(convx, convy) != transparentColor:
                                pyxel.blt(self.TILE_SIZE*dx+i - da, self.TILE_SIZE*dy+j - db, 
                                          self.palette, m.indexX*self.TILE_SIZE + i, m.indexY*self.TILE_SIZE + j, 
                                          m.flipX, m.flipY, m.transparency)
