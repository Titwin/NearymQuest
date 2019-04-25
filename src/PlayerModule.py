from Inputs import *
from TilemapModule import Tilemap
from AnimationModule import *
from Entity import *

class Character(Entity):
    def __init__ (self):
        Entity.__init__(self)
        self.dashTimer = 0
        self.atackTimer = 0
        self.speedMagnitude = Vector2f(1,1)
        self.speed = Vector2f(0,0)
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

        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_W], 'forward'))
        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_S], 'backward'))
        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_A], 'left'))
        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_D], 'right'))
        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack'))

        inputManager.addEvent(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        inputManager.addEvent(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        inputManager.addEvent(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        inputManager.addEvent(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        inputManager.addEvent(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

    def UpdateControls(self, maxX, maxY):
        self.speed = self.speedMagnitude

        if self.inputManager.CheckEventTrigger('attack') and self.atackTimer == 0:
            self.atackTimer = 2
        if self.atackTimer > 0:
            self.atackTimer -= 1
            self.speed = Vector2f(0,0)
        else:
            if (self.inputManager.CheckEvent('dash forward') or 
                self.inputManager.CheckEvent('dash backward') or 
                self.inputManager.CheckEvent('dash left') or 
                self.inputManager.CheckEvent('dash right')):
                self.dashTimer = 10

            if self.dashTimer > 0:
                self.speed *= 5
                self.dashTimer -= 1
            elif self.inputManager.CheckEvent('run'):
                self.speed *= 2

            direction = Vector2f(0,0)
            if self.inputManager.CheckEvent('forward'):
                direction.y = -1
            elif self.inputManager.CheckEvent('backward'):
                direction.y = 1
            if self.inputManager.CheckEvent('left'):
                direction.x = -1
            elif self.inputManager.CheckEvent('right'):
                direction.x = 1
            if direction != Vector2f(0,0):
                direction.normalized

            self.speed = Vector2f(self.speed.x * direction.x, self.speed.y * direction.y)
            self.position += self.speed
            self.position.x = max(min(self.position.x, maxX - self.size.x), 0)
            self.position.y = max(min(self.position.y, maxY - self.size.y), 0)

            if self.speed.x > 0:
                self.orientationX = 1
            elif self.speed.x < 0:
                self.orientationX = -1

            if self.speed.y > 0:
                self.orientationY = 1
            elif self.speed.y < 0:
                self.orientationY = -1


    def draw(self):
        playerX = min(self.position.x, 128)
        playerY = min(self.position.y, 128)

        flip = self.orientationX
        #### Animations
        if(self.atackTimer > 0):
            self.animator.play("attack",flip)
        # up
        elif (self.speed.x == 0 and self.speed.y > 0):
            self.animator.play("walk_down",flip)
        # down
        elif(self.speed.x == 0 and self.speed.y < 0):
            self.animator.play("walk_up",flip)
         # right
        elif(self.speed.x > 0):
            self.animator.play("walk_right",flip)
        # left
        elif(self.speed.x < 0):
            self.animator.play("walk_left",flip)
        else:
            self.animator.play("idle",flip)

        #pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)
        self.animator.draw(playerX, playerY)




