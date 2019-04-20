
import numpy as np #for matrices
from numpy import genfromtxt #for csv import

class Material:
    #_palette
    #_index
    def __init__(self, index,palette = 0):
        _palette = palette
        _index = index
class Tile:
    #posX
    #posY
    #materials
    #flags
    def __init__(self, x, y, material):
        self._x = x
        self._y = y 
        self._material = material

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
    def ImportCSV(path, sizeX, sizeY):
        my_data = genfromtxt(path, delimiter=',')
        data = []
        for y in range(sizeY):
            s = ""
            for x in range(sizeX):
                data.append(Tile(x,y,int(my_data[y,x])))
                s=s+str(my_data[x,y])+" "
            print(s+"\n")
        return Tilemap(sizeX, sizeY, data)
        
