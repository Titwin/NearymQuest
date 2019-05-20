import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Rendering')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Physics')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Scripting')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

from Component import *
from Entity import *
from Sprite import *
from SpriteRenderer import *
from Animation import *
from Animator import *
from SpriteBank import *
from PlayerModule import *
from Collider import * 

from ScriptInclude import * 

import json
import random

# Use this to create a new entity from a specified blueprint
# a blueprint is a specific callback to call. it's also a list of sprite to attach to the instanciate entity as a 'spriteList' component
# contain :
#    - blueprint : a dictionary<string, callback>. the list of callback
#    - spritelist : a dictionary<string, sprite[]>. a sprite list available to construct objects
class EntityFactory():
    # constructor
    # parameter : file : the file name to load for prefab instancing
    # the entity factory load several prefabs from a json file, and when 'instanciate' is called the related prefab is simply copied
    def __init__(self, file):
        self.file = file
        self.spriteBanks =[]
        self.templates = {}

        with open(self.file) as json_file:
            data = json.load(json_file)

            # Register the related frames
            if 'imageBanks' in data.keys():
                for b in data["imageBanks"]:

                    #create new bank
                    bank = SpriteBank(b["id"], b["file"])
                    self.spriteBanks.append(bank)
                    pyxel.image(b["id"]).load(0, 0, b["file"])

                    #add sprites
                    for s in b["sprites"]:
                        bank.addSprite( Sprite( Vector2f(s["pos_x"],s["pos_y"]), 
                                                Vector2f(s["width"],s["height"]),
                                                Vector2f(s["pivot_x"],s["pivot_y"]), 
                                                s["transparent"]),
                                        s["id"])
            else:
                print("Warning: EntityFactory: no 'imageBanks' in "+self.file)

            # create entity
            if('entities' in data.keys()):
                for name in data["entities"].keys():
                    templateData = data["entities"][name]
                    template = None
                    if(name == "player"):
                        template = Player()
                    elif(name == "wolf"):
                        template = Player()
                    else:
                        template = Entity()

                    # basic information
                    template.size.x = templateData["size_x"]
                    template.size.y = templateData["size_y"]

                    if('rigidbody' in templateData):
                        template.addComponent('RigidBody', RigidBody())

                    # rendering informations
                    if('renderer' in templateData):
                        palette = templateData["renderer"]["imageBank"]
                        bank = self.spriteBanks[palette]
                        renderer = templateData["renderer"]

                        # prefab is rendered using an Animator
                        if('animations' in renderer):
                            animations = []

                            #create the animations    
                            for a in renderer["animations"]:
                                frames = []
                                for f in a["frames"]:
                                    frame = bank.searchByName(f)
                                    if frame!=None:
                                        frames.append(frame)
                                    else:
                                        print("Warning: EntityFactory: no sprite under the name "+str(f)+", for loading "+name)    
                                animations.append(Animation(a["animationName"], bank, frames, a["interruptable"], 1.0/a["duration"], a["loop"]))

                            template.addComponent('Animator', Animator(palette, animations, renderer["defaultAnimation"]))

                        # prefab is rendered using a SpriteRenderer
                        elif('spriteList' in renderer):
                            spriteList = []
                            for s in renderer["spriteList"]:
                                sprite = bank.searchByName(s)
                                if sprite!=None:
                                    spriteList.append(sprite)
                                else:
                                    print("Warning: EntityFactory: no sprite under the name "+str(s)+", for loading "+name)   
                            template.addComponent('SpriteList', spriteList)
                            template.addComponent('ComponentRenderer', SpriteRenderer(bank))
                    else:
                        print("Warning: EntityFactory: no component renderer for entity "+name)

                    # collision informations
                    if('colliders' in templateData):
                        colliderList = []
                        for c in templateData["colliders"]:
                            collider = Collider(c["type"])
                            collider.position = Vector2f(c["pos_x"],c["pos_y"])
                            collider.size = Vector2f(c["width"],c["height"])
                            colliderList.append(collider)
                        template.addComponent('ColliderList', colliderList)
                    else:
                        print("Warning: EntityFactory: no colliders for entity "+name)

                    if('scripts' in templateData):
                        scripts = []
                        for s in templateData["scripts"]:
                            script = eval(s["name"])
                            #script.position = Vector2f(s["pos_x"],s["pos_y"])
                            #script.size = Vector2f(s["width"],s["height"])
                            scripts.append(script)
                        template.addComponent('Scripts', scripts)

                    # register template
                    self.templates[name] = template
            else:
                print("Warning: EntityFactory: no entities in "+self.file)

    # instanciate an entity from a specified prefab
    # parameter : instanceReference : a string referencing what you want
    # parameter : randomFlip : boolean indicating if you want an instance randomely flipped on X axis. default is True
    # return the instanciate entity, or None in case of failure
    def instanciate(self, instanceReference, randomFlip=True):
        if instanceReference in self.templates.keys():
            instance = self.templates[instanceReference].Copy()
            if randomFlip:
                instance.size = Vector2f(random.choice([-instance.size.x,instance.size.x]),instance.size.y)
            return instance
        else:
            return None

    # TODO
    # . add a new job to this class : an entity pool managment
    #     -> instead of allocating a new entity we re-use an available one