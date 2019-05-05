import pyxel


# The input updater, container and checker. 
# Instanced as a singleton, to access this class from an entity (for example), use : InputManager.inputManager
# contain :
#   . the game input list
#   . all raised notifications during the frame
class InputManager:
    # The singleton instance
    singleton = None
    
    # Constructor
    def __init__(self):
        singleton = self
        self.InputList = []
        self.frameInputs = []

    # Add an input to handle
    # simply add it (don't check if the input or a similar one already exist)
    # parameter : input : the input to add
    def addInput(self, input):
        self.InputList.append(input)

    # Remove an input
    # remove the first one from the input list on success. do nothing otherwise
    # parameter : input : the input to remove
    def removeInput(self, input):
        try:
            self.InputList.remove(input)
        except Exception as e:
            print("InputManager : fail removing input")

    # Remove first input based from name
    # remove the first one from the input list on success. do nothing otherwise
    # parameter : inputName : the input name to search for remove
    def removeInputFromName(self, inputName):
        try:
            for e in self.InputList:
                if(e.name == inputName):
                    self.InputList.remove(e)
        except Exception as e:
            print("InputManager : fail removing input")

    # Update internal state
    # has to be called each frame from the application
    # iterate on all registred inputs and call their virtual function "update".
    # if an input ask to rise a notification, this last one is created using the input name and state.
    # a notification is actually a tupple : (input name, internal boolean state [activated or not])
    def update(self):
        self.frameInputs = []
        for e in self.InputList:
            if(e.update()):
                self.frameInputs.append((e.name, e.activated))

    # Check if an input raised a notification this frame
    # parameter : inputName : the input name to check
    # if the input raised a notification this frame, the actual input state is returned (activated or not),
    # return False otherwise
    def CheckInputTrigger(self, inputName):
        for e in self.frameInputs:
            if(e[0] == inputName):
                return e[1]
        return False

    # Check if an input raised a notification this frame
    # parameter : inputName : the input name to check
    # return True if the inputName is found in the list of all the frame notifications
    # if you need the actual input steta after this give you true, use CheckInputTrigger function after a call of this one
    def CheckNotification(self, inputName):
        for e in self.frameInputs:
            if(e[0] == inputName):
                return True
        return False

    # Check if an input is currentlly active
    # parameter : inputName : the input name to check
    # return True if the first input referred as inputName is currentlly active, False otherwise
    # return False if no input with this name was found
    def CheckInput(self, inputName):
        for e in self.InputList:
            if(e.name == inputName):
                return e.activated
        return False





#   EXAMPLES OF USES CASES
    #   SINGLETON CREATION
        # the creation is better in your Application class
        #   self.inputManager = InputManager()

    #   TO CREATE NEW INPUTS FOR YOUR GAME FROM YOUR APPLICATION CLASS:
        # for a move command for a character : a simple BUTTON is enough
        #   inputManager.addInput( Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_W], 'forward') )
        #   inputManager.addInput( Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_S], 'backward') )
        #   inputManager.addInput( Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_A], 'left') )
        #   inputManager.addInput( Input(InputType.BUTTON, InputNotify.NONE, [pyxel.KEY_D], 'right') )

        # for an attack command you just want to know if the button was pressed during the frame so you create a BUTTON that notify on PRESSED
        #   inputManager.addInput( Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack') )

        # for moving alteration like running or sneaky walk
        #   inputManager.addInput( Input(InputType.CHORD, InputNotify.NONE, [pyxel.KEY_W, pyxel.KEY_SHIFT], 'run') )

        # for a special combo or sheat code :
        # inputManager.addInput( Sequence([pyxel.KEY_W, pyxel.KEY_W, 
        #                                  pyxel.KEY_S, pyxel.KEY_S,
        #                                  pyxel.KEY_A, pyxel.KEY_D,
        #                                  pyxel.KEY_A, pyxel.KEY_D,
        #                                  pyxel.KEY_Q, pyxel.KEY_E], 'god mode', 0.3) )


    #   TO CREATE NEW INPUTS FOR YOUR GAME FROM ANYWHERE:
        # do the same but call the singleton reference store in the InputManager class, for example :
        #   InputManager.singleton.addInput( Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack') )

        # this  is usefull if you want to create new inputs during runtime, for example: 
        #   if (replace weapon by shovel):
        #       InputManager.singleton.removeInputFromName( 'attack' )
        #       InputManager.singleton.addInput( Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'dig') )
        #   if (replace shovel by weapon):
        #       InputManager.singleton.removeInputFromName( 'dig' )
        #       InputManager.singleton.addInput( Input(InputType.BUTTON, InputNotify.PRESSED, [pyxel.KEY_SPACE], 'attack') )

