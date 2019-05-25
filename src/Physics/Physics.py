from Color import *
from Box import *
from Vector2 import Vector2f
from PhysicsSweptBox import *
from Collider import *
from QuadTree import *
from collections import defaultdict

class Physics:
    def __init__(self, renderer = None):
        self.renderer = renderer
        self.inflationFactor = Vector2f(5,5)
        self.avgClusterSolver = 0
        self.avgBroadPhase = 0
        self.avgIterations = 0

        self.specialEntity = None
        self.specialSwept = None

    def update(self, world, speed=1):
        self.avgClusterSolver = 0
        self.avgBroadPhase = 0
        self.avgIterations = 0

        sweptlist = self._createSweptBoxList(world, speed)
        pairs = self._detectCollidingPairs(world, sweptlist)
        nodes = self._detectNodesFromPairs(pairs)
        graph = Physics.ColliderGraph(nodes)
        for p in pairs:
            graph.addLink(p[0], p[1])
            graph.addLink(p[1], p[0])
        clusters = graph.getClusters()

        for cluster in clusters:
            self._clusterSolver(cluster)

        if len(clusters):
            self.avgClusterSolver /= len(clusters)
            self.avgIterations /= len(clusters)

        for swept in sweptlist:
            world.addEntity(swept.entity)
        for n in TreeNode.physicsContainer:
            n.physicsEntities.clear()
            if n.parent:
                n.parent.checkMergeNeeded()
        TreeNode.physicsContainer.clear()

        #print("Physics stat :")
        #print("   broad-phase : " + str(self.avgBroadPhase))
        #print("   cluster size : " + str(self.avgClusterSolver))
        #print("   iterations : " + str(self.avgIterations))


    def _createSweptBoxList(self, world, speed):
        sweptList = []
        self.specialSwept = None
        for entity in world.dynamicEntities:
            rb = entity.getComponent('RigidBody')
            colliders = entity.getComponent('ColliderList')
            if rb and colliders:
                c = colliders[0]
                collider = Box(entity.position - c.position, Vector2f(abs(c.size.x), abs(c.size.y)))
                swept = PhysicsSweptBox(collider, speed * rb.velocity, entity)
                sweptList.append(swept)
                world.addPhysicsEntity(swept)
                world.removeEntity(entity)
                if entity == self.specialEntity:
                    self.specialSwept = swept
        return sweptList

    def _detectCollidingPairs(self, world, sweptList):
        pairs = []
        self.avgBroadPhase = 0
        for swept in sweptList:
            neighbours = world.querryPhysicsEntities(swept.inflated(self.inflationFactor))
            self.avgBroadPhase += len(neighbours)

            collided = False
            for neigh in neighbours:
                if id(swept)!=id(neigh) and id(swept.entity)!=id(neigh):
                    if isinstance(neigh, PhysicsSweptBox):
                        if swept.overlap(neigh):
                            collided = True
                            pairs.append((swept, neigh))
                    else:
                        for c in neigh.getComponent('ColliderList', []):
                            collider = Collider.fromBox(neigh.position - c.position, Vector2f(abs(c.size.x), abs(c.size.y)), c.type)
                            if swept.overlap(collider):
                                collided = True
                                pairs.append((swept, collider))

            if not collided:
                swept.entity.position += swept.delta
        if len(sweptList) != 0:
            self.avgBroadPhase /= len(sweptList)
        return pairs

    def _detectNodesFromPairs(self, pairs):
        return set([i[0] for i in pairs]) | set([i[1] for i in pairs])

    def _clusterSolver(self, cluster):
        moving = []
        maxdelta = Vector2f(0,0)
        for box in cluster:
            if isinstance(box, PhysicsSweptBox):
                moving.append(box)
                if box.delta.magnitudeSqr > maxdelta.magnitudeSqr:
                    maxdelta = box.delta
        iterations = math.floor(maxdelta.magnitude)

        self.avgIterations += iterations
        self.avgClusterSolver += len(cluster)

        for x in range(iterations):
            for swept in moving:
                if swept.delta.x == 0 and swept.delta.y == 0:
                    continue

                u = swept.delta.x / iterations
                swept.initial.position.x += u
                swept.finalDelta.x += u
                for box in cluster:
                    if swept != box:
                        if (isinstance(box, PhysicsSweptBox) and swept.initial.overlap(box.initial)) or swept.initial.overlap(box):
                            self.collision(swept, box, Vector2f(u,0))
                            break

                u = swept.delta.y / iterations
                swept.initial.position.y += u
                swept.finalDelta.y += u
                for box in cluster:
                    if swept != box:
                        if (isinstance(box, PhysicsSweptBox) and swept.initial.overlap(box.initial)) or swept.initial.overlap(box):
                            self.collision(swept, box, Vector2f(0,u))
                            break

        for swept in moving:
            swept.entity.position += swept.finalDelta

    def collision(self, swept, box2, dp):
        if isinstance(box2, PhysicsSweptBox) or box2.type == Collider.BOUNDINGBOX:
            swept.initial.position -= dp
            swept.finalDelta -= dp
            if swept.entity:
                if not isinstance(box2, PhysicsSweptBox) and box2.type == Collider.BOUNDINGBOX:
                    rb = swept.entity.getComponent('RigidBody')
                    if dp.x != 0:
                        swept.delta.x = 0
                        rb.velocity.x = 0
                    else:
                        swept.delta.y = 0
                        rb.velocity.y = 0
            else:
                print("Error : Physics : collision : no entity assigned to sweptbox")
        else:
            pass
            #if dp.x != 0:
            #    print("enter TRIGGER by x")
            #else:
            #    print("enter TRIGGER by y")





    class ColliderGraph():
        def __init__(self, nodes):
            self.nodes = nodes
            self.graph = dict.fromkeys(nodes)
            self.visited = dict.fromkeys(nodes, False)
            for n in self.graph.keys():
               self.graph[n] = set()

        def addLink(self, n1, n2):
            if n1 != n2:
                self.graph[n1].add(n2)

        def getClusters(self):
            clusters = []
            for n in self.graph.keys():
                if not self.visited[n]:
                    c = []
                    self._getNeighbours(n, c)
                    clusters.append(c)
            return clusters

        def _getNeighbours(self, node, neigh):
            if not self.visited[node]:
                self.visited[node] = True
                neigh.append(node)
                for n in self.graph[node]:
                    self._getNeighbours(n, neigh)

        def print(self):
            for n in self.graph.keys():
                print(id(n))
                for n2 in self.graph[n]:
                    print("   " + str(id(n2)))