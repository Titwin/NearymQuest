from Entity import *
from Box import *


class TreeNode(Box):
    DIVISION = 2

    def __init__ (self):
        self.children = []
        self.entities = []
        self.parent = None

    def setTransform(self, x, y, w, h):
        self.position = Vector2f(x, y)
        self.size = Vector2f(w, h)
        self.adjustChild()

    def isLeaf(self):
        return len(self.children) == 0

    def getLevel(self):
        if(self.parent):
            return self.parent.getLevel() + 1
        else:
            return 0

    def getDepth(self):
        if not self.isLeaf():
            return self.children[0].getDepth() + 1
        else:
            return 1

    def adjustChild(self):
        if(not self.isLeaf()):
            s = Vector2f(self.size.x / TreeNode.DIVISION, self.size.y / TreeNode.DIVISION)
            for i in range(0, TreeNode.DIVISION):
                for j in range(0, TreeNode.DIVISION):
                    self.children[i*TreeNode.DIVISION + j].position = self.position - 0.5 * self.size + 0.5 * s + Vector2f(i*s.x, j*s.y)
                    self.children[i*TreeNode.DIVISION + j].size = s
                    self.children[i*TreeNode.DIVISION + j].adjustChild()

    def split(self):
        if(self.isLeaf()):
            for i in range(0, TreeNode.DIVISION):
                for j in range(0, TreeNode.DIVISION):
                    self.children.append(TreeNode())
                    self.children[i*TreeNode.DIVISION + j].parent = self
            self.adjustChild()
        else:
            for c in self.children:
                c.split()

    def merge(self):
        if(not self.isLeaf() and self.children[0].isLeaf()):
            self.children.clear()
        elif(not self.isLeaf()):
            for c in self.children:
                c.merge()

    def overlap(self, entity):
        if (self.position.x < entity.position.x + entity.size.x and self.position.x + self.size.x > entity.position.x and 
            self.position.y < entity.position.y + entity.size.y and self.position.y + self.size.y > entity.size.y):
            return True
        return False

    def addEntity(self, entity):
        if self.isLeaf():
            self.entities.append(entity)
        else:
            for c in self.children:
                if c.overlap(entity):
                    c.addEntity(entity)

    def removeEntity(self, entity):
        if self.isLeaf():
            try:
                self.entities.remove(entity)
            except Exception as e:
                pass
        else:
            for c in self.children:
                if c.overlap(entity):
                    c.addEntity(entity)


    # DEBUG
    def print(self):
        print(self)
        for c in self.children:
            c.print()

    def __str__(self):
        msg = ''
        for i in range(0, self.getLevel()):
            msg += '   '
        return msg + 'p: ' + str(self.position) + ' ,s: ' + str(self.size) + ' , obj: ' + str(len(self.entities))







