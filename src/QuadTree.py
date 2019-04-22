from Entity import *


class TreeNode:
    DIVISION = 2

    def __init__ (self):
        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1
        self.child = []
        self.entities = []
        self.parent = None

    def setTransform(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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
            sx = self.w / TreeNode.DIVISION
            sy = self.h / TreeNode.DIVISION
            for i in range(0, TreeNode.DIVISION):
                for j in range(0, TreeNode.DIVISION):
                    self.child[i*TreeNode.DIVISION + j].x = self.x - self.w/2 + sx/2 + i*sx
                    self.child[i*TreeNode.DIVISION + j].y = self.y - self.h/2 + sy/2 + j*sy
                    self.child[i*TreeNode.DIVISION + j].w = sx
                    self.child[i*TreeNode.DIVISION + j].h = sy
                    self.child[i*TreeNode.DIVISION + j].adjustChild()

    def split(self):
        if(self.isLeaf()):
            sx = self.w / TreeNode.DIVISION
            sy = self.h / TreeNode.DIVISION
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
        if  self.x < entity.x + entity.w and self.x + self.w > entity.x and self.y < entity.y + entity.h and self.y + self.h > entity.h:
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
        return msg + 'p: ' + str(self.x) + ' ' + str(self.y) + ' , s: ' + str(self.w) + ' ' + str(self.h) + ' , obj: ' + str(len(self.entities))







