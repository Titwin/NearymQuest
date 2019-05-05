from Collider import *
import json


# A collider container for the tile based objects
# if the game is well organized all instances refer to a specific index into this bank, so this container contain all possible collider of the world
# contain : 
#   . map : the collider list. please don't use it to avoid unreadable code. instead use [] operator : colliderBank[colliderIndex]
# need to specified a tileset file name at construction. for now it's parsing a Tiled software file generated in json.
# see (https://www.mapeditor.org/)
class ColliderBank:
    # constructor
    def __init__(self, filename):
        # create None array
        self.map = []
        for i in range(0, 256):
            self.map.append(None)

        # open file and set bitfield
        with open(filename) as json_file:
            data = json.load(json_file)
            for t in data['tiles']:
                if 'objectgroup' in t.keys():
                    self.map[t['id']] = []
                    for b in t['objectgroup']['objects']:
                        if 'type' in b.keys():
                            collider = None
                            if b['type'] == 'trigger':
                                collider = Collider(Collider.TRIGGERBOX)
                            elif b['type'] == 'hitbox':
                                collider = Collider(Collider.HITBOX)
                            elif b['type'] == 'collider':
                                collider = Collider(Collider.BOUNDINGBOX)
                            else:
                                print("Warning : ColliderBank loading : object in tile " + str(t['id']) + " has unknown type")
                                collider = Collider(Collider.UNKNOWN)

                            collider.position.x = b['x']
                            collider.position.y = b['y']
                            collider.size.x = b['width']
                            collider.size.y = b['height']
                            self.map[t['id']].append(collider)
                        else:
                            print("Warning : ColliderBank loading : object in tile " + str(t['id']) + " has no type")

    # operator []
    # no function protection (index check, good init, ...), so use it carefully
    # parameter : index : the tile index
    # return the collider list attached to the tile
    def __getitem__(self, index):
        return self.map[i]