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
#   . map : the collider list. please don't use it to avoid unreadable code. instead use [] operator : colliderBank[colliderIndex]
# need to specified a tileset file name at construction. for now it's parsing a Tiled software file generated in json.
# see (https://www.mapeditor.org/)
class FlagBank:
    solid = 0x0001
    destructible = 0x0002
    inflamable = 0x0004
    water = 0x0008

    # constructor
    def __init__(self, filename):
        # create empty flag array
        self.map = []
        for i in range(0, 256):
            self.map.append(0x0000)

        # open file and set bitfield
        with open(filename) as json_file:
            data = json.load(json_file)
            for t in data['tiles']:
                flag = 0x0000
                if 'properties' in t.keys():
                    for p in t['properties']:
                        if p['name'] == 'solid' and p['value'] == True:
                            flag |= FlagBank.solid
                        if p['name'] == 'destructible' and p['value'] == True:
                            flag |= FlagBank.destructible
                        if p['name'] == 'inflamable' and p['value'] == True:
                            flag |= FlagBank.inflamable
                        if p['name'] == 'water' and p['value'] == True:
                            flag |= FlagBank.water
                self.map[t['id']] = flag

    # operator []
    # parameter : index : the tile index
    # return the tile bitfield
    def __getitem__(self, index):
        return self.map[i]

    # test if the tile indexed by "index" has a specific flag
    # parameter : flag : the flag to test in the bitfield
    # parameter : index : the tile index
    # return True if the tile bitfield contain the flag, False otherwise
    def hasFlag(self, flag, index):
        return (self[index] & flag) != 0