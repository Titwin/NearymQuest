import pyxel
import time

class EventType:
    NONE = 0
    BUTTON = 1
    CHORD = 2
    SEQUENCE = 3

class EventNotify:
    NONE = 0
    PRESSED = 1
    RELEASED = 2
    ALL = 3



class Event:
    def __init__(self, type, notify, inputList, notification):
        self.type = type
        self.notify = notify
        self.inputList = inputList
        self.notification = notification
        self.activated = False

    def update(self):
        haveToNotify = False
        activated = True
        for input in self.inputList:
            if(not pyxel.btn(input)):
                activated = False
                break
        if(self.notify == EventNotify.RELEASED or self.notify == EventNotify.ALL):
            if(self.activated and not activated):
                haveToNotify = True
        if(self.notify == EventNotify.PRESSED or self.notify == EventNotify.ALL):
            if(not self.activated and activated):
                haveToNotify = True

        self.activated = activated
        return haveToNotify

    def __str__(self):
        msg = self.notification + ' '

        if(self.type == EventType.BUTTON):
            msg += "BUTTON "
        elif(self.type == EventType.CHORD):
            msg += "CHORD "
        elif(self.type == EventType.SEQUENCE):
            msg += "SEQUENCE "
        else:
            msg += "NONE "

        if(self.notify == EventNotify.PRESSED):
            msg += "PRESSED "
        elif(self.notify == EventNotify.RELEASED):
            msg += "RELEASED "
        elif(self.notify == EventNotify.ALL):
            msg += "ALL "
        else:
            msg += "NONE "

        msg += "["
        for input in self.inputList:
            msg += str(input) + ' '
        msg += "] "


        msg += str(self.activated)

        return msg


class Sequence(Event):
    def __init__(self, inputList, notification, resetTime = 0.3):
        super().__init__(EventType.SEQUENCE, EventNotify.PRESSED, inputList, notification)
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





