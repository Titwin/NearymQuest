from Events import *
from TilemapModule import Tilemap

class Character:
    def __init__ (self):
        self._x = 0
        self._y = 0
        self._w = 8
        self._h = 16
        self.dashTimer = 0
        self.speedX = 3
        self.speedY = 3

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

    def RegisterEvents(self, inputManager):

        self.inputManager = inputManager #perhaps use static propery

        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_W], 'forward'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_S], 'backward'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_A], 'left'))
        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_D], 'right'))

        inputManager.addEvent(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        inputManager.addEvent(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        inputManager.addEvent(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        inputManager.addEvent(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        inputManager.addEvent(Event(EventType.BUTTON, EventNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

    def UpdateControls(self, maxX, maxY):
        speedX = self.speedX
        speedY = self.speedY

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
        elif self.inputManager.CheckEvent('backward'):
            self.y = (self.y + 1*speedY)
        if self.inputManager.CheckEvent('left'):
            self.x = (self.x - 1*speedX)
        elif self.inputManager.CheckEvent('right'):
            self.x = (self.x + 1*speedX)

        self.x = max(min(self.x, maxX - self.w), 0)
        self.y = max(min(self.y, maxY - self.h), 0)
