from Entity import *
from Box import *


class TreeNode(Box):
    DIVISION = 2

    def __init__ (self):
        self.child = []
        self.entities = []
        self.parent = None

    def setTransform(self, x, y, w, h):
        Box.position = Vector2f(x, y)
        Box.size = Vector2f(w, h)
        self.adjustChild()

    def isLeaf(self):
        return len(self.child) == 0

    def getLevel(self):
        if(self.parent):
            return self.parent.getLevel() + 1
        else:
            return 0

    def getDepth(self):
        if not self.isLeaf():
            return self.child[0].getDepth() + 1
        else:
            return 1

    def adjustChild(self):
        if(not self.isLeaf()):
            s = Vector2f(Box.size.x / TreeNode.DIVISION, Box.size.y / TreeNode.DIVISION)
            for i in range(0, TreeNode.DIVISION):
                for j in range(0, TreeNode.DIVISION):
                    self.child[i*TreeNode.DIVISION + j].position = Box.position - 0.5 * Box.size + 0.5 * s + Vector2f(i*s.x, j*s.y)
                    self.child[i*TreeNode.DIVISION + j].size = s
                    self.child[i*TreeNode.DIVISION + j].adjustChild()

    def split(self):
        if(self.isLeaf()):
            for i in range(0, TreeNode.DIVISION):
                for j in range(0, TreeNode.DIVISION):
                    self.child.append(TreeNode())
                    self.child[i*TreeNode.DIVISION + j].parent = self
            self.adjustChild()
        else:
            for c in self.child:
                c.split()

    def merge(self):
        if(not self.isLeaf() and self.child[0].isLeaf()):
            self.child.clear()
        elif(not self.isLeaf()):
            for c in self.child:
                c.merge()

    def overlap(self, entity):
        if (Box.position.x < entity.position.x + entity.size.x and Box.position.x + Box.size.x > entity.position.x and 
            Box.position.y < entity.position.y + entity.size.y and Box.position.y + Box.size.y > entity.size.y):
            return True
        return False

    def addEntity(self, entity):
        if self.isLeaf():
            self.entities.append(entity)
        else:
            for c in self.child:
                if c.overlap(entity):
                    c.addEntity(entity)

    def removeEntity(self, entity):
        if self.isLeaf():
            try:
                self.entities.remove(entity)
            except Exception as e:
                pass
        else:
            for c in self.child:
                if c.overlap(entity):
                    c.addEntity(entity)


    # DEBUG
    def print(self):
        print(self)
        for c in self.child:
            c.print()

    def __str__(self):
        msg = ''
        for i in range(0, self.getLevel()):
            msg += '   '
        return msg + 'p: ' + str(self.position) + ' ,s: ' + str(self.size) + ' , obj: ' + str(len(self.entities))







