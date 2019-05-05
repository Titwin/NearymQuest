import pyxel
import time


# Enumerations for Inputs, permit to classify them and to configure them for notification
class InputType:
    NONE = 0       # ...(futur uses ?)...
    BUTTON = 1     # default, one button is pressed
    CHORD = 2      # multiple key pressed at same time
    SEQUENCE = 3   # multiple key pressed in specific order

class InputNotify:
    NONE = 0       # default, no notification
    PRESSED = 1    # notify when changing from released to pressed
    RELEASED = 2   # notify when changing from pressed to released
    ALL = 3        # notify when change state like (PRESSED or RELEASED)


# base class for all inputs, it contain :
#   . the update() function needed by the InputManager.
#   . a type and a notification enum
#   . a list of listening keys
#   . a name set by user (doesn't have to be unique for notification, but better to discriminate by passive check [check without notification])
#   . a boolean state (currently active or not)
class Input:
    def __init__(self, type, notify, inputList, name):
        self.type = type
        self.notify = notify
        self.inputList = inputList
        self.name = name
        self.activated = False

    # called each frame from InputManager.
    # return true if a notification has to be raised by the InputManager
    def update(self):
        # local initialization
        haveToNotify = False
        activated = True

        # if at least one key is not active then the event is not active too (work for buttons and chords)
        for input in self.inputList:
            if(not pyxel.btn(input)):
                activated = False
                break

        # check if input has to rise a notification
        if(self.notify == InputNotify.RELEASED or self.notify == InputNotify.ALL):
            if(self.activated and not activated):
                haveToNotify = True
        if(self.notify == InputNotify.PRESSED or self.notify == InputNotify.ALL):
            if(not self.activated and activated):
                haveToNotify = True

        # set internal stete and end
        self.activated = activated
        return haveToNotify


    # DEBUG
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

# derivate class from Input
# represent a key sequence (ordered number of key to be activated in a short period of time)
# useful for combos or double click on keys
# contain :
#   . the actual state (the next key state to check during the next update)
#   . the last valid key check time
#   . the maximum time acceptable for changing stete between too check. if two check occure
class Sequence(Input):
    def __init__(self, inputList, name, resetTime = 0.3):
        super().__init__(InputType.SEQUENCE, InputNotify.PRESSED, inputList, name)
        self.state = 0
        self.lastTime = time.time()
        self.resetTime = resetTime

    # inherited function from Input class
    def update(self):
        # a sequence is only active the frame the sequence is achived (so unactivated by default)
        self.activated = False

        # timeout so we have to reset the Input state
        if(time.time() - self.lastTime > self.resetTime):
            self.state = 0

        # check if the current state key is active, if yes increment increment state to check the next one in next update
        if(pyxel.btnp(self.inputList[self.state])):
            self.state += 1
            self.lastTime = time.time()
            if(self.state < len(self.inputList)):
                return False
            else:
                # input is active for this frame, reset internal state and ask manager for rise a notification
                self.state = 0
                self.activated = True
                return True

    # DEBUG
    def __str__(self):
        msg = super().__str__()
        msg += " " + str(self.resetTime)
        return msg





