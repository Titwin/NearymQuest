
import pyxel 
import math

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
            print("creating set of frames:("+str(first)+","+str(duration)+")=")
            for idx in range(first,first+duration):
                print(idx)
                frames.append(Animation.Frame(idx,width,height))
            print("created set of frames:("+str(first)+","+str(duration)+")="+str(len(frames)))
            return frames

    # string name
    # Frame[] frames
    # float speed
    # bool loop
    def __init__(self,name,frames,speed = 20,loop = False, flip = 1):
        self.__name = name
        self.__frames = frames
        self.__speed = speed
        self.__loop = loop
        self.__flip = flip

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
    def length(self):
        return len(self.__frames)

class Animator:

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
            print(animation.name +"::"+ str(animation.length))
        self.__defaultAnimation = default_animation
        self.__currentAnimation = self.__animations[default_animation]
        self.__currentFrame = 0
        self.__time = 0
        self.__flip = 1

    def Play(self, animation, flip, restart = False):
        if(restart or animation != self.__currentAnimation or self.__flip != flip ):
            self.__currentFrame = -1
            self.__currentAnimation = self.__animations[animation]
            self.__flip = flip
        self.Tick()

    def Tick(self):
        self.__time += 1

    def Draw(self, x, y):
        frame = 16*(math.floor(self.__time/self.__currentAnimation.speed)%self.__currentAnimation.length)
        print(self.__currentAnimation.name+" "+str(frame)+" "+ str(self.__currentAnimation.length))
        #pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)
        pyxel.blt(x, y, self.__palette, frame, self.__currentAnimation.frames[0].idx*16, self.__flip*16, 16, 0)


