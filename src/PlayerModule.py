from Events import *
from TilemapModule import Tilemap
from AnimationModule import *
class Character:
    def __init__ (self):
        self._x = 0
        self._y = 0
        self._w = 8
        self._h = 16
        self.dashTimer = 0
        self.speedX = 1
        self.speedY = 1
        self.dx = 0
        self.dy = 0
        self.orientationX = 1
        self.orientationY = 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = float(new_x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = float(new_y)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, new_w):
        self._w = float(new_w)

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, new_h):
        self._h = float(new_h)


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
            Animation("attack",Animation.Frame.CreateFrames(1,3),False,4,False,1)),
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

        if self.inputManager.CheckEvent('attack'):
            print("attack!!")
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


        #### Animations
        # up
        if (self.dx == 0 and self.dy > 0):
            #animStart = 4
            #animLength = 4
            #animSpeed = 4
            flip = 1
            self.animator.Play("walk_down",flip)
        # down
        elif(self.dx == 0 and self.dy < 0):
            #animStart = 3
            #animLength = 4
            #animSpeed = 4
            flip = 1
            self.animator.Play("walk_up",flip)
         # right
        elif(self.dx > 0):
            #animStart = 2
            flip = 1
            #animLength = 4
            #animSpeed = 4
            self.animator.Play("walk_right",flip)
        # left
        elif(self.dx < 0):
            #animStart = 2
            flip = -1
            #animLength = 4
            #animSpeed = 4
            self.animator.Play("walk_left",flip)
        else:
            #idle
            #animStart = 0
            #animLength = 2
            #animSpeed = 20
            flip = self.orientationX
            self.animator.Play("idle",flip)

        #pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)
        self.animator.Draw(playerX, playerY)




