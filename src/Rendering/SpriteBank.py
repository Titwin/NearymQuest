from Sprite import *

# A sprite container.
# if the game is well organized all instances refer to a specific index into this bank, so this container contain all possible collider of the world
# so the "big" structure of a sprite is a shared resource
# contain :
#    - data : the list of all registred sprite
#    - dataName : the name of registred sprite at the same index
#    - imageBank : the image bank this bank refer too
class SpriteBank():
    # constructor
    # parameter : bank : the image bank this bank refer too
    def __init__(self, bank):
        self.data = []
        self.dataName = []
        self.imageBank = bank

    # register a new sprite into the bank
    # parameter : sprite : a sprite object to add into the bank
    # parameter : name : a name to associate to this sprite. default is 'unknown'
    # return the index of the new registred sprite
    def addSprite(self, sprite, name = 'unknown'):
        self.data.append(sprite)
        self.dataName.append(name)
        return len(self.data)-1

    # operator []
    # no function protection (index check, good init, ...), so use it carefully
    # parameter : index : the sprite index
    # return the sprite attached to this index
    def __getitem__(self, index):
        return self.data[index]

    # search an index from a registred name
    # parameter : name : the sprite name to search
    # return the first sprite registred under this name
    def searchByName(self, name):
        for i in range(0,len(self.dataName)-1):
            if self.dataName[i] == name:
                return i
        return None

    # get the name of the sprite at a specified index, same as operator [] but for name list
    # parameter : index : the sprite index
    # return the sprite name attached to this index
    def getName(self, index):
        return self.dataName[index]

