from Collider import *
import json

class ColliderBank:
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

    def __getitem__(self, index):
        return self.map[i]