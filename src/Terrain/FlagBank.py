import json


class FlagBank:
    solid = 0x0001
    destructible = 0x0002
    inflamable = 0x0004
    water = 0x0008

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

    def __getitem__(self, index):
        return self.map[i]

    def hasFlag(self, flag, index):
        return (self[index] & flag)