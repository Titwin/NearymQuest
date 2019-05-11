import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Rendering')

from Component import *
from Entity import *
from Sprite import *
from SpriteRenderer import *

import random

# Use this to create a new entity from a specified blueprint
# a blueprint is a specific callback to call. it's also a list of sprite to attach to the instanciate entity as a 'spriteList' component
# contain :
#    - blueprint : a dictionary<string, callback>. the list of callback
#    - spritelist : a dictionary<string, sprite[]>. a sprite list available to construct objects
class EntityFactory():
    # constructor
    # parameter : spriteBank : the sprite bank to use to construct the spriteList
    #
    # actually it was simpler to initialize the sprite bank here, by creating new sprite and registring them to the bank from here.
    # the reason is simpler : all the magic numbers comes from here : we create all the sprite definition from here and we define entity constant from here.
    # one full dirty code in one place to rule them all !!
    # joking..., if we want to do it properly we have to move these magic stuff in a configuration file (for example in json) and load this file by both :
    # the entity factory and the sprite bank. the first one read all entity parameters and the second just all the sprites parameters.
    def __init__(self, spriteBank):
        self.blueprint = {}
        self.blueprint['bigRock'] = self.__RockBig
        self.blueprint['smallRock'] = self.__RockSmall
        self.blueprint['smallTree'] = self.__TreeSmall

        self.spritelist = {}
        self.spritelist['bigRock'] = [spriteBank.addSprite(Sprite(Vector2f(16,80), Vector2f(16,16), Vector2f(8,14), 0), 'bigRock')]
        self.spritelist['smallRock'] = [spriteBank.addSprite(Sprite(Vector2f(0,80), Vector2f(16,16), Vector2f(8,12), 0), 'smallRock')]
        self.spritelist['smallTree'] = [spriteBank.addSprite(Sprite(Vector2f(0,96), Vector2f(48, 32), Vector2f(24,64), 0), 'smallTreeLeaves'),
                                        spriteBank.addSprite(Sprite(Vector2f(16,128), Vector2f(16, 32), Vector2f(8,32), 0), 'smallTreeBark')]

    # instanciate an entity from a specified blueprint
    # parameter : instanceReference : a string referencing what you want
    # return the instanciate entity, or None in case of failure
    def instanciate(self, instanceReference):
        callback = self.blueprint.get(instanceReference, None)
        if callback:
            return callback()
        else:
            return None





    # private field : all the callbacks
    def __RockBig(self):
        rock = Entity()
        rock.addComponent('SpriteList', self.spritelist['bigRock'])
        rock.size = Vector2f(random.choice([16,-16]),16)
        rock.addComponent('ComponentRenderer', SpriteRenderer())
        return rock

    def __RockSmall(self):
        rock = Entity()
        rock.addComponent('SpriteList', self.spritelist['smallRock'])
        rock.size = Vector2f(random.choice([16,-16]),16)
        rock.addComponent('ComponentRenderer', SpriteRenderer())
        return rock

    def __TreeSmall(self):
        tree = Entity()
        tree.addComponent('SpriteList', self.spritelist['smallTree'])
        tree.size = Vector2f(random.choice([48,-48]),64)
        tree.addComponent('ComponentRenderer', SpriteRenderer())
        return tree









# TODO
# . add a new job to this class : an entity pool managment
#     -> instead of allocating a new entity we re-use an available one