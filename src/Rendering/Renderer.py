import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

import pyxel
from TileMap import *
from Vector2 import Vector2f

class Renderer:
    def renderTileMap(self, camera, world, tileRenderSize = 16):
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
                        pyxel.blt(tilePosFromCam.x, tilePosFromCam.y,
                                  material.imageBank,
                                  16*material.indexx, 16*material.indexy,
                                  tileRenderSize*material.flip.x, tileRenderSize*material.flip.y,
                                  material.transparency)


    def renderColliderOverlay(self, camera, world):
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
                        colliderList = world.colliderBank.map[material.index]
                        if colliderList:
                            for c in colliderList:
                                p1 = tilePosFromCam + c.position
                                p2 = tilePosFromCam + c.position + c.size

                                if material.flip.x == -1:
                                    p1.x = tilePosFromCam.x + 16 - c.position.x
                                    p2.x = tilePosFromCam.x + 16 - c.position.x - c.size.x
                                if material.flip.x == -1:
                                    p1.y = tilePosFromCam.y + 16 - c.position.y
                                    p2.y = tilePosFromCam.y + 16 - c.position.y - c.size.y

                                pyxel.rectb(p1.x, p1.y, p2.x, p2.y, c.type)


    def renderFlagOverlay(self, camera, world):
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
                        flag = world.flagBank.map[material.index]
                        if flag != 0:
                            pyxel.text(tilePosFromCam.x + 4, tilePosFromCam.y + 4, str(flag), 0)




    def renderPlayer(self, camera, player):
        a = player.animator.getSpriteAttributes()
        pPosFromCam = player.position - camera.position
        pyxel.blt(pPosFromCam.x + a[0], pPosFromCam.y + a[1], a[2], a[3], a[4], a[5], a[6], a[7])












## OLD function

#    def dithering(self, tilemap, camX, camY, centerX, centerY, exception, transparentColor = 0):
#        if(len(exception) <= 0):
#            return 
#        s = self.TILE_SIZE
#        da = camX - math.floor(camX/s)*s      # camera corner position x - (camera corner tile x) *16 -> residual x
#        db = camY - math.floor(camY/s)*s      # camera corner position x - (camera corner tile x) *16 -> residual y
#        camTileX = math.floor((camX-da)/s)
#        camTileY = math.floor((camY-db)/s)
#        ox = centerX - camX             # dithering center tile x - camera corner tile x
#        oy = centerY - camY             # dithering center tile y - camera corner tile y
#        for t in exception:
#            dx = t[0] - camTileX
#            dy = t[1] - camTileY
#            tile = tilemap[t]
#            if(tile and len(tile.materials) > 0):
#                for i in range(0, s):
#                    for j in range(0, s):
#                        x, y = s*dx + i - da, s*dy + j - db                   # current pixel position on screen
#                        convx, convy = 1*s + int(x - ox), 15*s + int(y - oy)   # convolution coordinates
#                        for m in tile.materials:
#                            if x < ox - s or x > ox + s-1 or y < oy - s or y > oy + s-1: # out of dithering patern
#                                pyxel.blt(s*dx+i - da, s*dy+j - db, 
#                                          self.palette, m.indexX*s + i, m.indexY*s + j, 
#                                          m.flipX, m.flipY, m.transparency)
#                            elif pyxel.image(self.palette).get(convx, convy) != transparentColor:
#                                pyxel.blt(s*dx+i - da, s*dy+j - db, 
#                                          self.palette, m.indexX*s + i, m.indexY*s + j, 
#                                          m.flipX, m.flipY, m.transparency)