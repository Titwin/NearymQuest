from TileMap import *

class Renderer:
    def __init__(self):
        pass

    def renderTileMap(self, camera, world):
        tiles = world.queryTiles(camera)