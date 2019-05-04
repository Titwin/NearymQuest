import pyxel
from TileMap import *
from PlayerModule import Player
from Vector2 import Vector2f

class Renderer:
    def __init__(self):
        pass

    def renderTileMap(self, camera, world):
        regionIndexList = world.querryRegions(camera)

        for regionIndex in regionIndexList:
            region = world.regions[regionIndex]
            if region.tilemap:
                tilesIndexList = region.querryTiles(camera)
                for tileIndex in tilesIndexList:
                    tile = region.tilemap.tiles[tileIndex]
                    tilePosFromCam = region.position + 16*Vector2f(tile.position.x, tile.position.y) - camera.position
                    for layer in sorted(tile.materials):
                        material = tile.materials[layer]
                        if(material.transparency != -1):
                            pyxel.blt(tilePosFromCam.x, tilePosFromCam.y,
                                      material.imageBank,
                                      16*material.indexx, 16*material.indexy,
                                      16*material.flip.x, 16*material.flip.y,
                                      material.transparency)
                        else:
                            pyxel.blt(tilePosFromCam.x, tilePosFromCam.y,
                                      material.imageBank,
                                      16*material.indexx, 16*material.indexy,
                                      16*material.flip.x, 16*material.flip.y,
                                      material.transparency)

    def renderPlayer(self, camera, player):
        a = player.animator.getSpriteAttributes()
        pPosFromCam = player.position - camera.position
        pyxel.blt(pPosFromCam.x + a[0], pPosFromCam.y + a[1], a[2], a[3], a[4], a[5], a[6], a[7])