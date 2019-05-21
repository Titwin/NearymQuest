from Collider import *

import json


# A flag container for the tile based objects
# actually the container contain a list of unsigned int, each representing a bitfield of flags, but it's more easy to call this containner the FlagBank
# contain
#   . a shifted flag enumeration : 
#          the "flag" definition, is a bit position in the integer, but for each test you have to shift it, wich is not efficient.
#          {
#               for example to test if the bit 3 (aka INFLAMMABLE) in a bitfield is set you have to do :
#                   if (bitfield & (1 << 3)) != 0:     or      if (bitfield & (1 << INFLAMMABLE)) != 0:
#               which is more cryptic than
#                   if (bitfield & INFLAMMABLE) != 0:
#          }
#          that's why I decided to store the shifted bit result directly in the enum
# each instance contain : 
#   . flags : the tile flag list. please don't use it to avoid unreadable code. instead use getFlag method
#   . flags : the tile flag list. please don't use it to avoid unreadable code. instead use getFlag method
# need to specified a tileset file name at construction. for now it's parsing a Tiled software file generated in json.
# see (https://www.mapeditor.org/)
class TerrainBank:
    class Flags:
        none = 0x0000
        solid = 0x0001
        destructible = 0x0002
        inflamable = 0x0004
        water = 0x0008

    def __init__(self, filename=None, image=0):
        self.imageBank = image
        self.filename = filename
        self.flags = []
        self.colliders = []
        for i in range(0, 256):
            self.flags.append(TerrainBank.Flags.none)
            self.colliders.append([])
        if filename:
            self.fromFile(filename)


    def fromFile(self, filename, image=0):
        # erase current data
        self.imageBank = image
        for i in range(0, 256):
            self.flags[i] = TerrainBank.Flags.none
            self.colliders[i].clear()

        # open file and set bitfield
        with open(filename) as json_file:
            data = json.load(json_file)
            for t in data['tiles']:

                # flags
                flag = TerrainBank.Flags.none
                if 'properties' in t.keys():
                    for p in t['properties']:
                        if p['name'] == 'solid' and p['value'] == True:
                            flag |= TerrainBank.Flags.solid
                        if p['name'] == 'destructible' and p['value'] == True:
                            flag |= TerrainBank.Flags.destructible
                        if p['name'] == 'inflamable' and p['value'] == True:
                            flag |= TerrainBank.Flags.inflamable
                        if p['name'] == 'water' and p['value'] == True:
                            flag |= TerrainBank.Flags.water
                self.flags[t['id']] = flag

                # colliders
                if 'objectgroup' in t.keys():
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
                            self.colliders[t['id']].append(collider)
                        else:
                            print("Warning : ColliderBank loading : object in tile " + str(t['id']) + " has no type")

    # access to collider list of tile at index
    # parameter : index : index to get collider list
    # return a list of colliders
    def getColliders(self, index):
        try:
            return self.colliders[index]
        except IndexError:
            return []

    # access to flags of tile at index
    # parameter : index : index to get flags
    # return a bitfield of all flags
    def getFlags(self, index):
        try:
            return self.flags[index]
        except IndexError:
            return TerrainBank.Flags.none

    # test if the tile indexed by "index" has a specific flag
    # parameter : flag : the flag to test in the bitfield
    # parameter : index : the tile index
    # return True if the tile bitfield contain the flag, False otherwise
    def hasFlag(self, flag, index):
        return (self[index] & flag) != 0
