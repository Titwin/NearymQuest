import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Rendering')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

from Component import *
from Entity import *
from Sprite import *
from SpriteRenderer import *
from Animation import *
from Animator import *
from SpriteBank import *
from PlayerModule import *
import json

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
    def __init__(self, file, spriteBank):
        self.__file = file
        self.spriteBanks =[]
        self.templates = {}
        with open(file) as json_file:
            data = json.load(json_file)

            # Register the related frames
            if(not ('imageBanks' in data.keys())):
                print("warning: no imageBanks in "+self.__file)
            else:
                for b in data["imageBanks"]:
                    #create new bank
                    bank = SpriteBank(b["id"],b["file"])
                    self.spriteBanks.append(bank)
                    pyxel.image(b["id"]).load(0, 0, b["file"])
                    #add sprites
                    for s in b["sprites"]:
                        print("sprite to load:"+str(s))
                        bank.addSprite(
                            Sprite(
                                Vector2f(s["pos_x"],s["pos_y"]), 
                                Vector2f(s["width"],s["height"]),
                                Vector2f(s["pivot_x"],s["pivot_y"]), 
                            s["transparent"]), s["id"])

            # create entity
            if(not('entities' in data.keys())):
                print("warning: no entities in "+self.__file)
            else:
                for name in data["entities"].keys():
                    templateData = data["entities"][name]
                    template = None
                    if(name == "player"):
                        template = Player()
                        # rigidbody
                        template.addComponent('RigidBody', RigidBody())

                    else:
                        template = Entity()

                    # basic information
                    template.size.x = templateData["size_x"]
                    template.size.y = templateData["size_y"]

                    # rendering information
                    if(not('renderer' in templateData)):
                        print("warning: no entities."+name+".renderer in "+self.__file)
                    else:

                        palette = templateData["renderer"]["imageBank"]
                        bank = self.spriteBanks[palette]
                        renderer = templateData["renderer"]
                        if('animations' in renderer):
                            animations = []
                            #create the animations    
                            for a in renderer["animations"]:
                                print(a["animationName"])
                                frames = []
                                for f in a["frames"]:
                                    frame = bank.searchByName(f)
                                    if(frame != None):
                                        frames.append(frame)
                                        print(str(f)+"::"+str(bank.searchByName(f)))
                                    else:
                                        print("no sprite under the name "+str(f))    
                                animation = Animation(a["animationName"], bank, frames,a["interruptable"],1.0/a["duration"],a["loop"],1)
                                animations.append(animation)

                            animator = Animator(palette,animations, "idle")

                            template.addComponent('animator', animator)
                        elif('spriteList' in renderer):
                            spriteList = []
                            for s in renderer["spriteList"]:
                                sprite = bank.searchByName(s)
                                if(sprite != None):
                                    spriteList.append(sprite)
                                    print(str(s)+"::"+str(bank.searchByName(s)))
                                else:
                                    print("no sprite under the name "+str(s))   
                            print(name +" has sprites: "+str(len(spriteList)))
                            template.addComponent('SpriteList', spriteList)
                            template.addComponent('ComponentRenderer',SpriteRenderer(bank))
                            pass
                            #player.addComponent('animator', animator)

                    # collision information
                    if(not('collider' in templateData)):
                        print("warning: no entities."+name+".collider in "+self.__file)
                    else:
                        #import colliders and other related stuff
                        pass

                    # register template
                    self.templates[name] = template

    # instanciate an entity from a specified blueprint
    # parameter : instanceReference : a string referencing what you want
    # return the instanciate entity, or None in case of failure
    def instanciate(self, instanceReference):
        if instanceReference in self.templates.keys():
            instance = self.templates[instanceReference].Copy()
            instance.size = Vector2f(random.choice([-instance.size.x,instance.size.x]),instance.size.y)
            if instance.getComponent("RigidBody"):
                 Entity.WORLD.addDynamicEntity(instance)
            return instance
        else:
            return None

    # TODO
    # . add a new job to this class : an entity pool managment
    #     -> instead of allocating a new entity we re-use an available one