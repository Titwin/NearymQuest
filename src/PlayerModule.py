import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/EntitySystem')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/InputSystem')

from Inputs import *
from AnimationModule import *
from Entity import *
from RigidBody import *

class Character(Entity):
    def __init__ (self):
        super(Character, self).__init__()
        self.dashTimer = 0
        self.atackTimer = 0
        self.walkingSpeed = Vector2f(1,1)
        self.speed = Vector2f(0,0)
        self.orientationX = 1
        self.orientationY = 1
        self.addComponent('RigidBody', RigidBody())


class Player(Character):
    def __init__ (self, palette):
        super(Player, self).__init__()
        self.CreateAnimator(palette)

    def CreateAnimator(self, palette):
        self.charactersPalette = palette
        self.addComponent('animator', Animator(
                                    self.charactersPalette,
                                    (Animation("idle",Animation.Frame.CreateFrames(0,2),True,20,True,1),
                                    Animation("walk_left",Animation.Frame.CreateFrames(2,4),True,4,True,-1),
                                    Animation("walk_right",Animation.Frame.CreateFrames(2,4),True,4,True,1),
                                    Animation("walk_up",Animation.Frame.CreateFrames(3,4),True,4,True,1),
                                    Animation("walk_down",Animation.Frame.CreateFrames(4,4),True,4,True,1),
                                    Animation("attack",(Animation.Frame(1,1,1), Animation.Frame(2,1,1),Animation.Frame(3,2,1,Vector2f(8,16))),False,2,False,1)), # speed 2
                                    "idle"))

    def RegisterEvents(self, inputManager):

        self.inputManager = inputManager #perhaps use static propery

        inputManager.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_W], 'forward'))
        inputManager.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_S], 'backward'))
        inputManager.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_A], 'left'))
        inputManager.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_D], 'right'))
        inputManager.addInput(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack'))

        inputManager.addInput(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        inputManager.addInput(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        inputManager.addInput(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        inputManager.addInput(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        inputManager.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

    def UpdateControls(self, maxBound, minBound):
        p = self.position
        if self.inputManager.CheckInputTrigger('attack') and self.atackTimer == 0:
            self.atackTimer = 2
            
        if self.atackTimer > 0:
            self.atackTimer -= 1
            self.speed = Vector2f(0,0)
        else:
            self.speed = self.walkingSpeed

            if (self.inputManager.CheckInput('dash forward') or 
                self.inputManager.CheckInput('dash backward') or 
                self.inputManager.CheckInput('dash left') or 
                self.inputManager.CheckInput('dash right')):
                self.dashTimer = 10

            if self.dashTimer > 0:
                self.speed *= 5
                self.dashTimer -= 1
            elif self.inputManager.CheckInput('run'):
                self.speed *= 2

            direction = Vector2f(0,0)
            if self.inputManager.CheckInput('forward'):
                direction.y = -1
            elif self.inputManager.CheckInput('backward'):
                direction.y = 1
            if self.inputManager.CheckInput('left'):
                direction.x = -1
            elif self.inputManager.CheckInput('right'):
                direction.x = 1
            #if direction != Vector2f(0,0):
            #    direction.normalized

            self.speed = Vector2f(self.speed.x * direction.x, self.speed.y * direction.y)
            p = self.position + self.speed
            p.x = max(min(p.x, maxBound.x - self.size.x), minBound.x)
            p.y = max(min(p.y, maxBound.y - self.size.y), minBound.y)

            if self.speed.x > 0:
                self.orientationX = 1
            elif self.speed.x < 0:
                self.orientationX = -1

            if self.speed.y > 0:
                self.orientationY = 1
            elif self.speed.y < 0:
                self.orientationY = -1

        return p


    def updateAnimation(self):
        animator = self.getComponent('animator')
        if not animator:
            return


        flip = self.orientationX
        #### Animations
        if(self.atackTimer > 0):
            animator.play("attack",flip)
        # up
        elif (self.speed.x == 0 and self.speed.y > 0):
            animator.play("walk_down",flip)
        # down
        elif(self.speed.x == 0 and self.speed.y < 0):
            animator.play("walk_up",flip)
         # right
        elif(self.speed.x > 0):
            animator.play("walk_right",flip)
        # left
        elif(self.speed.x < 0):
            animator.play("walk_left",flip)
        else:
            animator.play("idle",flip)

        #pyxel.blt(playerX, playerY, self.charactersPalette, 16*(math.floor(self.draw_count/animSpeed)%animLength), animStart*16, flip*16, 16, 0)
        #self.animator.draw(playerX, playerY)


    def __str__(self):
        msg = 'player, position : ' + str(self.position) + ', size : ' + str(self.size) + '\n'
        for c in self.components.keys():
            msg += '   ' + str(c) + '\n'
        return msg
        

