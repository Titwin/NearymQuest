from ComponentRenderer import *

# render of entity containing sprites
# render entity depending on sprites in 'SpriteList' component
# for now renderer is asking for spriteList component each frame
# contain :
#    - bank : the spritebank used for render this entity
class SpriteRenderer(ComponentRenderer):
    # constructor
    def __init__(self, bank):
        super(SpriteRenderer, self).__init__()
        self.__bank = bank

    # draw overload
    # just iterate over sprites attached to owner entity and draw them
    def draw(self, entityPosFromCam):
        sprites = self.owner.getComponent('SpriteList')

        if sprites:
            for spriteIndex in sprites:
                sprite = self.__bank[spriteIndex]
                if self.owner.size.x > 0:
                    pyxel.blt(entityPosFromCam.x - sprite.pivot.x, entityPosFromCam.y - sprite.pivot.y,
                              self.__bank.imageBank,
                              sprite.position.x, sprite.position.y,
                              sprite.size.x,     sprite.size.y,
                              sprite.transparency)
                else:
                    pyxel.blt(entityPosFromCam.x - sprite.flippedPivot.x, entityPosFromCam.y - sprite.flippedPivot.y,
                              self.__bank.imageBank,
                              sprite.position.x, sprite.position.y,
                              -sprite.size.x,     sprite.size.y,
                              sprite.transparency)





