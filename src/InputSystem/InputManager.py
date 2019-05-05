import pyxel

class InputManager:
    inputManager = None
    
    def __init__(self):
        inputManager = self
        self.InputList = []
        self.frameInputs = []

    def addEvent(self, event):
        self.InputList.append(event)

    def removeEvent(self, event):
        try:
            self.InputList.remove(event)
        except Exception as e:
            print("InputManager : fail removing event")

    def update(self):
        self.frameInputs = []
        for e in self.InputList:
            if(e.update()):
                self.frameInputs.append((e.name, e.activated))

    def CheckEventTrigger(self, eventName):
        for e in self.frameInputs:
            if(e[0] == eventName):
                return e[1]
        return False

    def CheckEvent(self, eventName):
        for e in self.InputList:
            if(e.name == eventName):
                return e.activated
        return False


        