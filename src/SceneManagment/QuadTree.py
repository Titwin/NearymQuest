from Box import *
from Entity import *


# Base class for constructing a Tree (quad, oct, ...)
# contain :
#     - children : a list of node considered as child (could be empty is node is a leaf)
#     - entities : a list of entities attached to the node. these entities origins are inside the node boundaries
#     - parent : a reference on the parent node. if None, this node is the tree root
#     - physicsEntities : a list of fake entities attached to the node. Only used in physics process. please don't touch it
class TreeNode(Box):
    DIVISION = 2    # number of division in one axis, defined on 2 for quadtree (2 child on x, 2 child on y)

    # constructor
    def __init__ (self):
        super(TreeNode, self).__init__()
        self.children = []
        self.entities = set()
        self.physicsEntities = set()
        self.parent = None

    # destructor
    def __del__(self):
        for c in self.children:
            del c
        #for e in self.entities:
        #    del e

    ## TREE RELATED
    # change node position and size (and adjust children if needed)
    # parameter : position : the new node position (top left corner)
    # parameter : size : the new size of the node
    def setTransform(self, position, size):
        self.position = position
        self.size = size
        self.adjustChild()

    # check if the node is a leaf
    # return True is node is actually a leaf, Fals otherwise
    def isLeaf(self):
        return len(self.children) == 0

    # get the node level in tree
    # return the node level, 0 if node is the tree root
    def getLevel(self):
        if(self.parent):
            return self.parent.getLevel() + 1
        else:
            return 0

    # get the local tree depth (number of level until leaves) relatively to node.
    # ex : if node is leaf, return 1 (for the actual node level), if node is root return the entire tree depth
    # return local depth
    def getDepth(self):
        if not self.isLeaf():
            return self.children[0].getDepth() + 1
        else:
            return 1

    # adjust automatically all the children size and position based on the node current position and size
    # please don't use it, prefer setTransform, split, merge or other
    def adjustChild(self):
        if(not self.isLeaf()):
            s = self.size / TreeNode.DIVISION
            for i in range(TreeNode.DIVISION):
                for j in range(TreeNode.DIVISION):
                    self.children[i*TreeNode.DIVISION + j].position = self.position + Vector2f(i*s.x, j*s.y)
                    self.children[i*TreeNode.DIVISION + j].size = s
                    self.children[i*TreeNode.DIVISION + j].adjustChild()

    # increase local depth by one
    # if the node is a leaf, it instanciate children based on TreeNode.DIVISION, and adjust them after
    # if the node is not a leaf it call the same function on each child
    def split(self):
        if(self.isLeaf()):
            for i in range(TreeNode.DIVISION):
                for j in range(TreeNode.DIVISION):
                    self.children.append(TreeNode())
                    self.children[i*TreeNode.DIVISION + j].parent = self
            self.adjustChild()
        else:
            for c in self.children:
                c.split()

    # decrease local depth by one
    # if the node contain children which are leaves it delete them,
    # if its children are not leaves it call the same function for each
    # if node is currentlly leaf, nothing happen
    def merge(self):
        if(not self.isLeaf() and self.children[0].isLeaf()):
            self.children.clear()
        elif(not self.isLeaf()):
            for c in self.children:
                c.merge()



    ## ENTITY RELATED
    # add an entity in the local tree
    # search the first child that overlap the entity and call this function on it
    # if node is a leaf it add this entity to its entity list
    def addEntity(self, entity):
        if self.isLeaf():
            self.entities.add(entity)
        else:
            for c in self.children:
                if c.overlap(entity):
                    c.addEntity(entity)
                    return

    # remove an entity to the local tree
    # search the first child that overlap the entity and call this function on it
    # if node is a leaf it try to remove this entity from its entity list
    def removeEntity(self, entity):
        if self.isLeaf():
            try:
                self.entities.remove(entity)
            except Exception as e:
                pass
        else:
            for c in self.children:
                if c.overlap(entity):
                    c.removeEntity(entity)

    # return all entitities that potentially overlap a box
    # if node is a leaf it return its entity list
    # otherwise for each child that overlap the box it call this function on it
    # parameter : box : the box to check the local tree against
    # return a list of entities that potentially overlap
    def querryEntities(self, box):
        if self.isLeaf():
            return self.entities.copy()
        else:
            result = set()
            for c in self.children:
                if c.overlap(box):
                    r = c.querryEntities(box)
                    if r:
                        result = result | r
            return result


    ## PHYSICS RELATED
    # remove all fake entities placed during physics update
    def clearPhysicsEntities(self):
        self.physicsEntities.clear()
        for c in self.children:
            c.clearPhysicsEntities()

    # add a physics entity to the node
    # parameter : entity ; the physics entity to add
    # return the node possesing the entity added
    def addPhysicsEntity(self, entity):
        if self.isLeaf():
            self.physicsEntities.add(entity)
            return self
        else:
            for c in self.children:
                if c.overlap(entity):
                    return c.addPhysicsEntity(entity)

    # same as 'querryEntities', but return in addition all physicsEntities
    def querryPhysicsEntities(self, box):
        if self.isLeaf():
            return (self.entities.copy() | self.physicsEntities.copy())
        else:
            result = set()
            for c in self.children:
                if c.overlap(box):
                    r = c.querryPhysicsEntities(box)
                    if r:
                        result = result | r
            return result

    ## DEBUG
    def print(self):
        print(self)
        for c in self.children:
            c.print()

    def __str__(self):
        msg = ''
        for i in range(0, self.getLevel()):
            msg += '   '
        return msg + 'p: ' + str(self.position) + ' ,s: ' + str(self.size) + ' , obj: ' + str(len(self.entities))







