import pyxel

class InputManager:
    def __init__(self):
        self.instantEventList = []

    def addEvent(self, event):
        self.instantEventList.append(event)

    def removeEvent(self, event):
        try:
            self.instantEventList.remove(event)
        except Exception as e:
            print("InputManager : fail removing event")

    def update(self):
        frameEvent = []
        for e in self.instantEventList:
            if(e.update()):
                frameEvent.append((e.notification, e.activated))
        