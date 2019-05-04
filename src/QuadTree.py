from Box import *
from Entity import *



class TreeNode(Box):
    DIVISION = 2

    def __init__ (self):
        super(TreeNode, self).__init__()
        self.children = []
        self.entities = []
        self.parent = None

    def __del__(self):
        for c in self.children:
            del c
        for e in self.entities:
            del e

    def setTransform(self, position, size):
        self.position = position
        self.size = size
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
            s = self.size / TreeNode.DIVISION
            for i in range(TreeNode.DIVISION):
                for j in range(TreeNode.DIVISION):
                    self.children[i*TreeNode.DIVISION + j].position = self.position + Vector2f(i*s.x, j*s.y)
                    self.children[i*TreeNode.DIVISION + j].size = s
                    self.children[i*TreeNode.DIVISION + j].adjustChild()

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

    def merge(self):
        if(not self.isLeaf() and self.children[0].isLeaf()):
            self.children.clear()
        elif(not self.isLeaf()):
            for c in self.children:
                c.merge()

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







