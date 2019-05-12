from ComponentRenderer import *

# render of entity containing sprites
# render entity depending on sprites in 'SpriteList' component
# for now renderer is asking for spriteList component each frame
class SpriteRenderer(ComponentRenderer):
    # constructor
    def __init__(self):
        super(SpriteRenderer, self).__init__()

    # draw overload
    # just iterate over sprites attached to owner entity and draw them
    def draw(self, camera, world):
        spriteBank = world.spriteBank
        sprites = self.owner.getComponent('SpriteList')
        entityPosFromCam = self.owner.position - camera.position

        if sprites:
            for spriteIndex in sprites:
                sprite = spriteBank[spriteIndex]
                if self.owner.size.x > 0:
                    pyxel.blt(entityPosFromCam.x - sprite.pivot.x, entityPosFromCam.y - sprite.pivot.y,
                              spriteBank.imageBank,
                              sprite.position.x, sprite.position.y,
                              sprite.size.x,     sprite.size.y,
                              sprite.transparency)
                else:
                    pyxel.blt(entityPosFromCam.x - sprite.flippedPivot.x, entityPosFromCam.y - sprite.flippedPivot.y,
                              spriteBank.imageBank,
                              sprite.position.x, sprite.position.y,
                              -sprite.size.x,     sprite.size.y,
                              sprite.transparency)





