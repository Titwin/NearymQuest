from RegionModule import *


class World():
    def __init__(self, w = 1, h = 1):
        self.regions = []
        self.w = w
        self.h = h
        self.rw = 50
        self.rh = 50

        ox = -self.rw * w / 2
        oy = -self.rh * h / 2
        for i in range(w):
            for j in range(w):
                self.regions.append(Region(ox + i*self.rw, oy + j*self.rh, self.rw, self.rh))

    def print(self):
        for r in regions:
            print(r)

    def __str__(self):
        msg = '---WORLD---\n'
        for r in regions:
            msg += str(r) + '\n'
        return msg

