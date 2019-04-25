import pyxel
import time

class InputType:
    NONE = 0
    BUTTON = 1
    CHORD = 2
    SEQUENCE = 3

class InputNotify:
    NONE = 0
    PRESSED = 1
    RELEASED = 2
    ALL = 3



class Input:
    def __init__(self, type, notify, inputList, name):
        self.type = type
        self.notify = notify
        self.inputList = inputList
        self.name = name
        self.activated = False

    def update(self):
        haveToNotify = False
        activated = True
        for input in self.inputList:
            if(not pyxel.btn(input)):
                activated = False
                break
        if(self.notify == InputNotify.RELEASED or self.notify == InputNotify.ALL):
            if(self.activated and not activated):
                haveToNotify = True
        if(self.notify == InputNotify.PRESSED or self.notify == InputNotify.ALL):
            if(not self.activated and activated):
                haveToNotify = True

        self.activated = activated
        return haveToNotify

    def __str__(self):
        msg = self.name + ' '

        if(self.type == InputType.BUTTON):
            msg += "BUTTON "
        elif(self.type == InputType.CHORD):
            msg += "CHORD "
        elif(self.type == InputType.SEQUENCE):
            msg += "SEQUENCE "
        else:
            msg += "NONE "

        if(self.notify == InputNotify.PRESSED):
            msg += "PRESSED "
        elif(self.notify == InputNotify.RELEASED):
            msg += "RELEASED "
        elif(self.notify == InputNotify.ALL):
            msg += "ALL "
        else:
            msg += "NONE "

        msg += "["
        for input in self.inputList:
            msg += str(input) + ' '
        msg += "] "


        msg += str(self.activated)

        return msg


class Sequence(Input):
    def __init__(self, inputList, name, resetTime = 0.3):
        super().__init__(InputType.SEQUENCE, InputNotify.PRESSED, inputList, name)
        self.state = 0
        self.lastTime = time.time()
        self.resetTime = resetTime

    def update(self):
        self.activated = False
        if(time.time() - self.lastTime > self.resetTime):
            self.state = 0

        if(pyxel.btnp(self.inputList[self.state])):
            self.state += 1
            self.lastTime = time.time()
            if(self.state < len(self.inputList)):
                return False
            else:
                self.state = 0
                self.activated = True
                return True

    def __str__(self):
        msg = super().__str__()
        msg += " " + str(self.resetTime)
        return msg





