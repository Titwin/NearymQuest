import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Mathematic')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src/Rendering')

from Color import *
from PhysicsSweptBox import *
from Collider import *

class Physics:
    def __init__(self, renderer = None):
        self.renderer = renderer
        self.sweptBoxList = []
        self.quadtreeNode = []
        self.islandList = []
        self.inflationFactor = Vector2f(16,16)
        self.broadPhase = 0
        self.islandSolveur = 0
        self.avgIterations = 0

    def update(self, world, speed = 1):
        # reset temp variables
        self.sweptBoxList.clear()
        self.quadtreeNode.clear()
        self.islandList.clear()
        self.avgBroadPhase = 0
        self.avgIslandSolveur = 0
        self.avgIterations = 0

        # predict transforms and creating bounding swept volume
        for entity in world.dynamicEntities:
            rb = entity.getComponent('RigidBody')
            if rb:
                c = entity.getComponent('ColliderList')[0]
                collider = Box.fromBox(entity.position - c.position, Vector2f(abs(c.size.x), abs(c.size.y)))
                swept = PhysicsSweptBox(collider, speed * rb.velocity, entity)
                self.sweptBoxList.append(swept)
                world.removeEntity(entity)
                self.quadtreeNode.append(world.addPhysicsEntity(swept))

        # detect islands
        for swept in self.sweptBoxList:
            if self.renderer:
                self.renderer.gizmos.append((swept.inflated(self.inflationFactor), Color.LightGrey))
                self.renderer.gizmos.append((swept, Color.Red))
            neighbours = world.querryPhysicsEntities(swept.inflated(self.inflationFactor))
            self.avgBroadPhase += len(neighbours)

            collided = False
            for neigh in neighbours:
                if id(swept)!=id(neigh) and id(swept.entity)!=id(neigh):
                    colliders = []
                    if isinstance(neigh, PhysicsSweptBox):
                        colliders = neigh.entity.getComponent('ColliderList')
                    else:
                        colliders = neigh.getComponent('ColliderList')

                    for c in colliders:
                        collider = None
                        if isinstance(neigh, PhysicsSweptBox):
                            collider = Collider.fromBox(neigh.entity.position - c.position, Vector2f(abs(c.size.x), abs(c.size.y)), c.type)
                        else:
                            collider = Collider.fromBox(neigh.position - c.position, Vector2f(abs(c.size.x), abs(c.size.y)), c.type)

                        if self.renderer:
                            self.renderer.gizmos.append((collider, Color.Red))
                        if swept.overlap(collider):
                            if self.renderer:
                                self.renderer.gizmos.append((collider, Color.Black))
                            if not collided:
                                self.islandList.append(set())
                                self.islandList[-1].add(swept)
                            collided = True
                            self.islandList[-1].add(collider)

            # integrate simple case
            if(not collided):
                swept.entity.position += swept.delta

        if len(self.sweptBoxList):
            self.avgBroadPhase /= len(self.sweptBoxList)

        # simplify islands (merge all non disjoint)
        if len(self.islandList):
            temp = []
            while len(self.islandList):
                current = self.islandList.pop(0)
                for island in self.islandList:
                    if not island.isdisjoint(current):
                        current = current | island
                temp.append(current)
            self.islandList , temp = temp , self.islandList

        # per island continuous collision detection and intergration
        for island in self.islandList:

            # preparing island
            moving = []
            maxdelta = Vector2f(0,0)
            for box in island:
                if isinstance(box, PhysicsSweptBox):
                    moving.append(box)
                    if box.delta.magnitudeSqr > maxdelta.magnitudeSqr:
                        maxdelta = box.delta
            iterations = math.floor(maxdelta.magnitude)+1
            self.avgIterations += iterations
            if self.renderer:
                for swept in moving:
                    self.renderer.gizmos.append((swept.initial, Color.White))
            self.avgIslandSolveur += len(island)

            # move every moving boxes, up to 1 pixel at same time
            for x in range(iterations):
                for swept in moving:
                    if swept.delta == Vector2f(0,0):
                        continue

                    u = swept.delta.x / iterations
                    swept.initial.position.x += u
                    swept.finalDelta.x += u
                    for box in island:
                        if swept != box:
                            if (isinstance(box, PhysicsSweptBox) and swept.initial.overlap(box.initial)) or swept.initial.overlap(box):
                                self.collision(swept, box, Vector2f(u,0))
                                break

                    u = swept.delta.y / iterations
                    swept.initial.position.y += u
                    swept.finalDelta.y += u
                    for box in island:
                        if swept != box:
                            if (isinstance(box, PhysicsSweptBox) and swept.initial.overlap(box.initial)) or swept.initial.overlap(box):
                                self.collision(swept, box, Vector2f(0,u))
                                break

            for swept in moving:
                swept.entity.position += swept.finalDelta

        if len(self.islandList):
            self.avgIslandSolveur /= len(self.islandList)
            self.avgIterations /= len(self.islandList)

        # clear world of temp data
        for n in self.quadtreeNode:
            if n:
                n.clearPhysicsEntities()
        for swept in self.sweptBoxList:
            world.addEntity(swept.entity)


    def collision(self, swept, box2, dp):
        if isinstance(box2, PhysicsSweptBox) or box2.type == Collider.BOUNDINGBOX:
            swept.initial.position -= dp
            swept.finalDelta -= dp
            rb = swept.entity.getComponent('RigidBody')
            if dp.x != 0:
                swept.delta.x = 0
                rb.velocity.x = 0
            else:
                swept.delta.y = 0
                rb.velocity.y = 0
        else:
            if dp.x != 0:
                print("enter TRIGGER by x")
            else:
                print("enter TRIGGER by y")