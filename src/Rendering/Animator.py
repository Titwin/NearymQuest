import pyxel
import math
from Vector2 import Vector2f
from ComponentRenderer import *

# Animator class handling all about animations of an entity
# the animation machine state is handled by the controller script. here we just increment, reset and loop animations states
# the 'master script' wich handle the character machine state just call the 'play' function once in a frame depending to the wanted animation
# contain :
#    - palette : int, the pyxel palette used for drawing
#    - animations : Dictionary(string,Animation), a container of all known animation
#    - defaultAnimation : string, the default animation, used when a non looping animation finished
#    - currentAnimation : string, the current animation name
#    - time : int, the current animation time used to correctlly change frame, etc...
#    - currentFrame : int, the current frame in current animation
#    - flip : int [1,-1], indicate if the entity is currently flipped (== -1)
#    - frame : current animation frame internal use
class Animator (ComponentRenderer):
    # Constructor
    def __init__(self, palette, animations, default_animation):
        super(Animator,self).__init__()
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
        self.__frame = 0

    # play a specific animation
    # just call this several time with the same parameters to see your entity be animated
    # parameter : animation : the animation to play
    # parameter : flip : indicate if animation has to be flipped (-1), or not (1), default is 1
    # parameter : restart : indicate if the animation state has to be reset, default is False
    def play(self, animation, flip=1, restart=False):
        if(restart or self.__currentAnimation.interruptable and (self.__animations[animation] != self.__currentAnimation or self.__flip != flip) ):
            self.__currentFrame = -1
            self.__currentAnimation = self.__animations[animation]
            self.__flip = flip
            self.__frame = 0
            self.__time = 0
        self.tick()

    # increment animation state
    def tick(self):
        self.__time += 1
        self.__frame = math.floor(self.__time/self.__currentAnimation.speed)
        if self.__frame>= self.__currentAnimation.length:
            if self.__currentAnimation.loop:
                self.__frame = 0
                self.__time = 0
            else:
                self.play(self.__defaultAnimation,self.__flip, True)

    # draw overload
    # draw the current animation frame with all goods parameters
    def draw(self, entityPosFromCam):
        animation = self.__currentAnimation
        frame = animation[self.__frame]
        firstFrame = animation[0]
        offset = 0
        if(self.__flip == -1 and firstFrame.size.x != frame.size.x):
            offset = firstFrame.size.x-frame.size.x

        pyxel.blt(entityPosFromCam.x + offset - frame.pivot.x, 
                     entityPosFromCam.y - frame.pivot.y,
                     self.__palette,
                     frame.position.x, frame.position.y,
                     self.__flip * frame.size.x, frame.size.y,
                     0)
     
    