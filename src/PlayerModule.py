from Events import *
from TilemapModule import Tilemap
from AnimationModule import *
from EntityComponentModule import *

class Character(Entity):
    def __init__ (self):
        Entity.__init__(self)
        self.dashTimer = 0
        self.speedX = 1
        self.speedY = 1
        self.dx = 0
        self.dy = 0
        self.orientationX = 1
        self.orientationY = 1


class Player(Character):
    def __init__ (self):
        Character.__init__(self)
        self.CreateAnimator()

    def CreateAnimator(self):
        self.charactersPalette = 1
        self.animator = Animator(
            self.charactersPalette,
            (Animation("idle",Animation.Frame.CreateFrames(0,2),True,20,True,1),
            Animation("walk_left",Animation.Frame.CreateFrames(2,4),True,4,True,-1),
            Animation("walk_right",Animation.Frame.CreateFrames(2,4),True,4,True,1),
            Animation("walk_up",Animation.Frame.CreateFrames(3,4),True,4,True,1),
            Animation("walk_down",Animation.Frame.CreateFrames(4,4),True,4,True,1),
            Animation("attack",(Animation.Frame(1,1,1), Animation.Frame(2,1,1),Animation.Frame(3,2,1)),False,2,False,1)),
            "idle")

    def RegisterEvents(self, inputManager):

        self.inputManager = inputManager #perhaps use static propery

        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_W], 'forward'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_S], 'backward'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_A], 'left'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_D], 'right'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_SPACE], 'attack'))

        inputManager.addEvent(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        inputManager.addEvent(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        inputManager.addEvent(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        inputManager.addEvent(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

    def UpdateControls(self, maxX, maxY):
        speedX = self.speedX
        speedY = self.speedY
        self.dx = 0
        self.dy = 0

        self.__attackTrigger = False
        if self.inputManager.CheckEvent('attack'):
            self.__attackTrigger = True
        else:
            if self.inputManager.CheckEvent('dash forward') or self.inputManager.CheckEvent('dash backward') or self.inputManager.CheckEvent('dash left') or self.inputManager.CheckEvent('dash right'):
                self.dashTimer = 10
            if self.dashTimer > 0:
                speedX *= 5
                speedY *= 5
                self.dashTimer -= 1
            elif self.inputManager.CheckEvent('run'):
                speedX *= 2
                speedY *= 2

            if self.inputManager.CheckEvent('forward'):
                self.y = (self.y - 1*speedY)
                self.dy =  -1*speedY
            elif self.inputManager.CheckEvent('backward'):
                self.y = (self.y + 1*speedY)
                self.dy =  1*speedY
            if self.inputManager.CheckEvent('left'):
                self.x = (self.x - 1*speedX)
                self.dx =  -1*speedX
            elif self.inputManager.CheckEvent('right'):
                self.x = (self.x + 1*speedX)
                self.dx =  1*speedX

            self.x = max(min(self.x, maxX - self.w), 0)
            self.y = max(min(self.y, maxY - self.h), 0)

            if self.dx > 0:
                self.orientationX = 1
            elif self.dx < 0:
                self.orientationX = -1

            if self.dy > 0:
                self.orientationY = 1
            elif self.dy < 0:
                self.orientationY = -1


    def draw(self):
        playerX = min(self.x, 128)
        playerY = min(self.y, 128)

        flip = self.orientationX
        #### Animations
        if(self.__attackTrigger==True):
            self.animator.play("attack",flip)
        # up
        elif (self.dx == 0 and self.dy > 0):
            self.animator.play("walk_down",flip)
        # down
        elif(self.dx == 0 and self.dy < 0):
            self.animator.play("walk_up",flip)
         # right
        elif(self.dx > 0):
            self.animator.play("walk_right",flip)
        # left
        elif(self.dx < 0):
            self.animator.play("walk_left",flip)
        else:
            self.animator.play("idle",flip)

        #pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)
        self.animator.draw(playerX, playerY)




