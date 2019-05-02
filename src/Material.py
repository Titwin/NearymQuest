from Vector2 import Vector2i


class Material:
    def __init__(self, imageBank = 0, index = 0, flip = Vector2i(1,1), transparency = -1):
        self.imageBank = imageBank
        self.index = index
        self.flip = flip
        self.transparency = transparency

    # DEBUG
    def print(self):
        print(str(self))

    def __str__(self):
        return 'image bank : ' + str(self.imageBank) + ', index : ' + str(self.index) + ', flip : ' + str(self.flip) + ', transparency : ' + str(self.transparency)


