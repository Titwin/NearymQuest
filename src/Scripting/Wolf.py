from Script import *

class Wolf(Script):
    def __init__(self):
        super(Wolf, self).__init__()
        self.target = None
        self.flip = 1
        self.atackTimer = 0
        self.walkingSpeed = 1
        self.runningSpeed = 10

    def update(self):
        rigidbody = self.owner.getComponent('RigidBody')
        if not rigidbody:
            return

        if self.target:
            d = self.target.position - self.owner.position
            s = Vector2f(0,0)
            if d != Vector2f(0,0) and d.magnitude > 64:
                s = self.runningSpeed * d.normalize()
            elif d != Vector2f(0,0) and d.magnitude > 48:
                s = self.walkingSpeed * d.normalize()
            rigidbody.velocity =  s
        else:
            pass

    def onPreRender(self):
        animator = self.owner.getComponent('Animator')
        rigidbody = self.owner.getComponent('RigidBody')
        if not animator or not rigidbody:
            return

        # compute entity orientation
        if rigidbody.velocity.x > 0:
            self.flip = 1
        if rigidbody.velocity.x < 0:
            self.flip = -1

        # update right animations
        if(self.atackTimer > 0):
            animator.play("attack", self.flip)
        # up
        elif (rigidbody.velocity.x == 0 and rigidbody.velocity.y > 0):
            animator.play("walk_down", self.flip)
        # down
        elif(rigidbody.velocity.x == 0 and rigidbody.velocity.y < 0):
            animator.play("walk_up", self.flip)
         # right
        elif(rigidbody.velocity.x > 0):
            animator.play("walk_horizontal", self.flip)
        # left
        elif(rigidbody.velocity.x < 0):
            animator.play("walk_horizontal", self.flip)
        else:
            animator.play("idle", self.flip)
