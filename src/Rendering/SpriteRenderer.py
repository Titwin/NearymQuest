from ComponentRenderer import *

class SpriteRenderer(ComponentRenderer):
    def __init__(self):
        super(SpriteRenderer, self).__init__()

    def draw(self, camera, world):
        spriteBank = world.spriteBank
        sprites = self.owner.getComponent('SpriteList')
        entityPosFromCam = self.owner.position - camera.position

        for spriteIndex in sprites:
            sprite = spriteBank[spriteIndex]
            pyxel.blt(entityPosFromCam.x - sprite.pivot.x, entityPosFromCam.y - sprite.pivot.y,
                      spriteBank.imageBank,
                      sprite.position.x, sprite.position.y,
                      sprite.size.x,     sprite.size.y,
                      sprite.transparency)





