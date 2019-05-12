import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')

import pyxel 
import math
from Component import *
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

    def __get__(self, idx):
        self.bank[frames[idx]]

class Animator (Component):
    # Dictionary(string,Animation) animations
    # string currentAnimation
    # int time
    # int currentFrame
    # bool flip
    def __init__(self, palette, animations, default_animation):
        self.__palette = palette
        #indexes the animations by name
        self.__animations = {}
        for animation in animations:
            self.__animations[animation.name] = animation
           
        self.__defaultAnimation = default_animation
        self.__currentAnimation = self.__animations[default_animation]
        self.__currentFrame = 0
        self.__time = 0
        self.__flip = 1

    def play(self, animation, flip, restart = False):
        if(restart or self.__currentAnimation.interruptable and (self.__animations[animation] != self.__currentAnimation or self.__flip != flip) ):
            self.__currentFrame = -1
            self.__currentAnimation = self.__animations[animation]
            self.__flip = flip
            self.__frame = 0
            self.__time = 0
        self.tick()

    def tick(self):
        self.__time += 1
        self.__frame = math.floor(self.__time/self.__currentAnimation.speed)
        if self.__frame>= self.__currentAnimation.length:
            if self.__currentAnimation.loop:
                self.__frame = 0
                self.__time = 0
            else:
                self.play(self.__defaultAnimation,self.__flip, True)

    def getSpriteAttributes(self):
        animation = self.__currentAnimation
        frame = animation[self.__frame]
        
        offset = 0
        if(self.__flip == -1
            and animation.frames[0].width == 1 
            and animation.frames[self.__frame].width == 2):
            offset = -16
        return (offset - self.__currentAnimation.frames[self.__frame].offset.x, 0 - self.__currentAnimation.frames[self.__frame].offset.y,
                self.__palette,
                16*self.__frame, self.__currentAnimation.frames[0].idx*16,
                self.__flip*16* self.__currentAnimation.frames[self.__frame].width, 16,
                0)

    def draw(self, x, y):

        offset = 0
        if(self.__flip == -1
            and self.__currentAnimation.frames[0].width == 1 
            and self.__currentAnimation.frames[self.__frame].width == 2):
            offset = -16
        pyxel.blt(x+offset, y, self.__palette, 16*self.__frame, self.__currentAnimation.frames[0].idx*16, self.__flip*16* self.__currentAnimation.frames[self.__frame].width, 16, 0)


