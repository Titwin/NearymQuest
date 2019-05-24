from Script import *
from Vector2 import Vector2f

class WolfBehaviour(Script):
    def __init__(self):
        super(WolfBehaviour, self).__init__()
        self.target = None
        self.flip = 1
        self.atackTimer = 0
        self.walkingSpeed = 1
        self.runningSpeed = 3
        self.speedMag = 0
        self.defaultAnimation = "idle" # "idle", "dig", "idle2", "sleep", "howling"

    def update(self):
        rigidbody = self.owner.getComponent('RigidBody')
        if not rigidbody:
            return

        if self.target:
            d = self.target.position - self.owner.position
            s = Vector2f(0,0)
            u = self.getPrincipalDirection(d)

            # not moving
            if self.speedMag == 0:
                if d != Vector2f(0,0) and d.magnitude > 150:
                    s = self.runningSpeed * u
                    self.speedMag = self.runningSpeed
                elif d != Vector2f(0,0) and d.magnitude > 32:
                    s = self.walkingSpeed * u
                    self.speedMag = self.walkingSpeed

            # already moving to target
            else:
                if d != Vector2f(0,0) and d.magnitude > 150:
                    s = self.runningSpeed * u
                    self.speedMag = self.runningSpeed
                elif d != Vector2f(0,0) and d.magnitude > 32:
                    s = self.speedMag * u
                else:
                    self.speedMag = 0

            rigidbody.velocity =  s
        else:
            rigidbody.velocity = Vector2f(0,0)

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
        elif self.speedMag == self.walkingSpeed:
            # up
            if (rigidbody.velocity.x == 0 and rigidbody.velocity.y > 0):
                animator.play("walk_down", self.flip)
            # down
            elif(rigidbody.velocity.x == 0 and rigidbody.velocity.y < 0):
                animator.play("walk_up", self.flip)
            # horizontal
            else:
                animator.play("walk_horizontal", self.flip)
        elif self.speedMag == self.runningSpeed:
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
            animator.play(self.defaultAnimation, self.flip)

    def getPrincipalDirection(self, v):
        if v.x==0 and v.y==0:
            return Vector2f(0,0)
        u = v.normalize()
        if u.x > 0.92:
            return Vector2f(1,0)
        elif u.x < -0.92:
            return Vector2f(-1,0)
        elif u.y > 0.92:
            return Vector2f(0,1)
        elif u.y < -0.92:
            return Vector2f(0,-1)

        elif u.x > 0 and u.y > 0:
            return Vector2f(1,1)
        elif u.x > 0 and u.y < 0:
            return Vector2f(1,-1)
        elif u.x < 0 and u.y > 0:
            return Vector2f(-1,1)
        elif u.x < 0 and u.y < 0:
            return Vector2f(-1,-1)
        return Vector2f(0,0)
