import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

from Vector2 import Vector2f

class Animation:

    # string name
    # int[] frames
    # float speed
    # bool loop
    def __init__(self,name,bank,frames,interruptable = True,speed = 20,loop = False, flip = 1):
        self.__name = name
        self.__bank = bank
        self.__frames = frames
        self.__speed = speed
        self.__loop = loop
        self.__interruptable = interruptable

    @property
    def name(self):
        return self.__name
   
    @property
    def bank(self):
        return self.__bank

    #@property
    #def frames(self):
    #    return self.__frames

    @property
    def speed(self):
        return self.__speed

    @property
    def loop(self):
        return self.__loop

    @property
    def interruptable(self):
        return self.__interruptable

    @property
    def length(self):
        return len(self.__frames)

    def __getitem__(self, idx):
        #print(self.name +"["+str(idx)+"/"+str(len(self.__frames))+"]="+str(self.__frames[idx]))
        if(self.__frames[idx] != None):
            return self.bank[self.__frames[idx]]