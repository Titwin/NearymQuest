import pyxel

class InputManager:
    def __init__(self):
        self.EventList = []

    def addEvent(self, event):
        self.EventList.append(event)

    def removeEvent(self, event):
        try:
            self.EventList.remove(event)
        except Exception as e:
            print("InputManager : fail removing event")

    def update(self):
        self.frameEvent = []
        for e in self.EventList:
            if(e.update()):
                self.frameEvent.append((e.notification, e.activated))

    def CheckEventTriggerDown(self, eventName):
        for e in self.frameEvent:
            if(e[0].notification == eventName):
                return e[1]
        return False

    def CheckEventTriggerUp(self, eventName):
        for e in self.frameEvent:
            if(e[0].notification == eventName):
                return not e[1]
        return False  

    def CheckEvent(self, eventName):
        for e in self.EventList:
            if(e.notification == eventName):
                return e.activated
        return False


        