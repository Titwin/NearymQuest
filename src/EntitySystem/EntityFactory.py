from Component import *
from Entity import *
from Sprite import *

import random

class EntityFactory():
    def __init__(self):
        self.blueprint = {}
        self.blueprint['bigRock'] = self.__RockBig
        self.blueprint['smallRock'] = self.__RockSmall
        self.blueprint['smallTree'] = self.__TreeSmall

    def instanciate(self, instanceReference):
        callback = self.blueprint.get(instanceReference, None)
        if callback:
            return callback()
        else:
            return None

    # private field
    def __RockBig(self):
        rock = Entity()
        rock.addComponent('spriteList', [Sprite(0, Vector2f(16,80), Vector2f(16,16), Vector2f(8,14), 0)])
        rock.size = Vector2f(random.choice([16,-16]),16)
        #rock.spriteOffset = Vector2f(8,14)
        return rock

    def __RockSmall(self):
        rock = Entity()
        rock.addComponent('spriteList', [Sprite(0, Vector2f(0,80), Vector2f(16,16), Vector2f(8,12), 0)])
        rock.size = Vector2f(random.choice([16,-16]),16)
        #rock.spriteOffset = Vector2f(8,12)
        return rock

    def __TreeSmall(self):
        tree = Entity()
        tree.addComponent('spriteList', [Sprite(0, Vector2f(0,96), Vector2f(48, 32), Vector2f(24,64), 0),   #leaves
                                         Sprite(0, Vector2f(16,128), Vector2f(16, 32), Vector2f(8,32), 0)])  #bark
        tree.size = Vector2f(random.choice([48,-48]),64)
        #tree.spriteOffset = Vector2f(24,64)
        return tree