from Script import *
from Vector2 import Vector2f
from InputManager import *
from Inputs import *

import pyxel


class PlayerController(Script):
    def __init__(self):
        super(PlayerController, self).__init__()
        self.flip = 1
        self.atackTimer = 0
        self.walkingSpeed = 1
        self.runningSpeed = 2
        self.speedMag = 0

        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_W], 'forward'))
        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_S], 'backward'))
        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_A], 'left'))
        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_D], 'right'))
        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack'))

        InputManager.singleton.addInput(Sequence([pyxel.KEY_W, pyxel.KEY_W], 'dash forward'))
        InputManager.singleton.addInput(Sequence([pyxel.KEY_S, pyxel.KEY_S], 'dash backward'))
        InputManager.singleton.addInput(Sequence([pyxel.KEY_A, pyxel.KEY_A], 'dash left'))
        InputManager.singleton.addInput(Sequence([pyxel.KEY_D, pyxel.KEY_D], 'dash right'))

        InputManager.singleton.addInput(Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_SHIFT], 'run'))

    def update(self):
        rigidbody = self.owner.getComponent('RigidBody')
        im = InputManager.singleton
        if not rigidbody or not im:
            return

        self.speedMag = 0
        if im.CheckInputTrigger('attack') and self.atackTimer == 0:
            self.atackTimer = 2
            
        if self.atackTimer > 0:
            self.atackTimer -= 1
            rigidbody.velocity = Vector2f(0,0)
        else:
            direction = Vector2f(0,0)
            if im.CheckInput('forward'):
                direction.y = -1
                self.speedMag = self.walkingSpeed
            elif im.CheckInput('backward'):
                direction.y = 1
                self.speedMag = self.walkingSpeed
            if im.CheckInput('left'):
                direction.x = -1
                self.speedMag = self.walkingSpeed
            elif im.CheckInput('right'):
                direction.x = 1
                self.speedMag = self.walkingSpeed


            if (im.CheckInput('dash forward') or im.CheckInput('dash backward') or im.CheckInput('dash left') or im.CheckInput('dash right')):
                self.dashTimer = 10

            if im.CheckInput('run'):
                self.speedMag = self.runningSpeed

            rigidbody.velocity = self.speedMag * direction


    def onPreRender(self):
        self.updateAnimation()

    def updateAnimation(self):
        animator = self.owner.getComponent('Animator')
        rigidbody = self.owner.getComponent('RigidBody')
        if not animator or not rigidbody:
            return

        # compute orientation
        if rigidbody.velocity.x > 0:
            self.flip = 1
        if rigidbody.velocity.x < 0:
            self.flip = -1

        # update right animations
        if(self.atackTimer > 0):
            animator.play("attack", self.flip)
        elif rigidbody.velocity != Vector2f(0,0) and self.speedMag == self.walkingSpeed:
            # up
            if (rigidbody.velocity.x == 0 and rigidbody.velocity.y > 0):
                animator.play("walk_down", self.flip)
            # down
            elif(rigidbody.velocity.x == 0 and rigidbody.velocity.y < 0):
                animator.play("walk_up", self.flip)
            # horizontal
            else:
                animator.play("walk_horizontal", self.flip)
        elif rigidbody.velocity != Vector2f(0,0) and self.speedMag == self.runningSpeed:
            # up
            if (rigidbody.velocity.x == 0 and rigidbody.velocity.y > 0):
                animator.play("run_down", self.flip)
            # down
            elif(rigidbody.velocity.x == 0 and rigidbody.velocity.y < 0):
                animator.play("run_up", self.flip)
            # horizontal
            else:
                animator.play("run_horizontal", self.flip)
        else:
            animator.play("idle", self.flip)




