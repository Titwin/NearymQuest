import pyxel
from TileMap import *
from Vector2 import Vector2f
from Color import *
from Collider import *

class Renderer:
    def __init__(self):
        self.entitiesDrawn = 0
        self.tileDrawn = 0
        self.primitiveDrawn = 0
        self.gizmos = []

    def resetStat(self):
        self.entitiesDrawn = 0
        self.tileDrawn = 0
        self.primitiveDrawn = 0


    # STANDARD DRAW PASS
    def renderTileMap(self, camera, world, tileRenderSize = 16):
        regionIndexList = world.querryRegions(camera)

        for regionIndex in regionIndexList:
            region = world.regions[regionIndex]
            if region.tilemap:
                tilesIndexList = region.querryTiles(camera)
                for tileIndex in tilesIndexList:
                    tile = region.tilemap.tiles[tileIndex]
                    tilePosFromCam = region.position + 16*tile.position - camera.position
                    for layer in sorted(tile.materials):
                        material = tile.materials[layer]
                        pyxel.blt(tilePosFromCam.x, tilePosFromCam.y,
                                  material.imageBank,
                                  16*material.indexx, 16*material.indexy,
                                  tileRenderSize*material.flip.x, tileRenderSize*material.flip.y,
                                  material.transparency)
                    self.tileDrawn += len(tile.materials)
        self.primitiveDrawn += self.tileDrawn

    def renderEntities(self, camera, world):
        entities = list(world.querryEntities(camera.inflated(Vector2f(48,64))))
        if entities != None:
            entities.sort(key=Renderer.entityKey)
            for entity in entities:
                scripts = entity.getComponent('Scripts')
                if scripts:
                    for s in scripts:
                        s.onPreRender()

                renderer = entity.getComponent('ComponentRenderer')
                if renderer:
                    self.draw(camera, entity, renderer)
                    self.entitiesDrawn += 1

                elif entity.getComponent('Animator'):
                    self.draw(camera, entity, entity.getComponent('Animator'))
                    self.entitiesDrawn += 1

        self.primitiveDrawn += 1

    
    # compute position of the entity in relationship to the camera, then ask its delegator to render
    def draw(self, camera, entity, renderDelegate):
         #blt(x, y, img, u, v, w, h, [colkey])
         entityPosFromCam = entity.position - camera.position
         renderDelegate.draw(entityPosFromCam)

    # Wrapper for the pyxel blt function
    # probably unnecessary
    def blt(x, y, img, u, v, w, h, colkey = -1):
        pyxel.blt(x, y, img, u, v, w, h, colkey)

    def drawGizmos(self, camera):
        for b in self.gizmos:
            entityPosFromCam = b[0].position - camera.position
            pyxel.rectb(entityPosFromCam.x, entityPosFromCam.y, entityPosFromCam.x + b[0].size.x, entityPosFromCam.y + b[0].size.y, b[1])
        self.gizmos.clear()


    # DEBUG
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
                        colliderList = world.terrainBank.getColliders(material.index)
                        if colliderList:
                            for c in colliderList:
                                p1 = tilePosFromCam + c.position
                                p2 = tilePosFromCam + c.position + c.size

                                if material.flip.x == -1:
                                    p1.x = tilePosFromCam.x + 15 - c.position.x
                                    p2.x = tilePosFromCam.x + 15 - c.position.x - c.size.x
                                if material.flip.y == -1:
                                    p1.y = tilePosFromCam.y + 16 - c.position.y
                                    p2.y = tilePosFromCam.y + 16 - c.position.y - c.size.y

                                pyxel.rectb(p1.x, p1.y, p2.x, p2.y, 0)
                            self.primitiveDrawn += len(colliderList)


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
                        flag = world.terrainBank.getFlags(material.index)
                        if flag != 0:
                            pyxel.text(tilePosFromCam.x + 4, tilePosFromCam.y + 4, str(flag), 0)
                            self.primitiveDrawn += 1


    def renderEntitiesPivot(self, camera, world):
        if (math.floor(pyxel.frame_count / 5)%2) == 0:
            entities = list(world.querryEntities(camera.inflated(Vector2f(48,64))))
            if entities != None:
                entities.sort(key=Renderer.entityKey)
                for entity in entities:
                    entityPosFromCam = entity.position - camera.position
                    pyxel.pix(entityPosFromCam.x, entityPosFromCam.y, 0)
                self.primitiveDrawn += len(entities)


    def renderEntitiesColliders(self, camera, world):
        entities = list(world.querryEntities(camera.inflated(Vector2f(48,64))))
        if entities != None:
            entities.sort(key=Renderer.entityKey)
            for entity in entities:
                entityPosFromCam = entity.position - camera.position
                colliders = entity.getComponent('ColliderList')
                if colliders:
                    for c in colliders:
                        if c.type == Collider.BOUNDINGBOX:
                            pyxel.rectb(entityPosFromCam.x - c.position.x, entityPosFromCam.y - c.position.y, 
                                        entityPosFromCam.x - c.position.x + c.size.x, entityPosFromCam.y - c.position.y + c.size.y, 
                                        Color.Black)
                        elif c.type == Collider.TRIGGERBOX:
                            pyxel.rectb(entityPosFromCam.x - c.position.x, entityPosFromCam.y - c.position.y, 
                                        entityPosFromCam.x - c.position.x + c.size.x, entityPosFromCam.y - c.position.y + c.size.y, 
                                        Color.Yellow)
                    self.primitiveDrawn += len(colliders)


    #USEFULL
    @staticmethod
    def entityCmp(a,b):
        if a.position.y == b.position.y:
            return a.position.x < b.position.x
        else:
            return a.position.y < b.position.y
    @staticmethod
    def entityKey(a):
        return (a.position.y)*16 + a.position.x













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