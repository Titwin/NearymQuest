
import pyxel 
import math
from EntityComponentModule import *

class Animation:
    class Frame:
        #int idx
        #int width
        #int height
        def __init__(self, _idx,_width=1,_height=1):
            self.idx = _idx
            self.width = _width
            self.height = _height

        @staticmethod
        def CreateFrames(first,duration,width=1,height=1):
            frames = []
            for idx in range(first,first+duration):
                frames.append(Animation.Frame(idx,width,height))
            return frames

    # string name
    # Frame[] frames
    # float speed
    # bool loop
    def __init__(self,name,frames,interruptable = True,speed = 20,loop = False, flip = 1):
        self.__name = name
        self.__frames = frames
        self.__speed = speed
        self.__loop = loop
        self.__flip = flip
        self.__interruptable = interruptable

    @property
    def name(self):
        return self.__name

    @property
    def frames(self):
        return self.__frames

    @property
    def speed(self):
        return self.__speed

    @property
    def loop(self):
        return self.__loop
    @property
    def flip(self):
        return self.__flip

    @property
    def interruptable(self):
        return self.__interruptable

    @property
    def length(self):
        return len(self.__frames)

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

    def draw(self, x, y):
        offset = 0
        if(self.__flip == -1
            and self.__currentAnimation.frames[0].width == 1 
            and self.__currentAnimation.frames[self.__frame].width == 2):
            offset = -16
        pyxel.blt(x+offset, y, self.__palette, 16*self.__frame, self.__currentAnimation.frames[0].idx*16, self.__flip*16* self.__currentAnimation.frames[self.__frame].width, 16, 0)


