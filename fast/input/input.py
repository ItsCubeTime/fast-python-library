"""@note I was originally planning to implement this module with pynpun as backend and flesh it out quite a lot
, but Ive decided to wait for a better more robust backend solution as pynpun wont be compatible with iOS & android & as I want to try and make 'fast' support also those 
device (in some shape or form) when used together with flet.

For that reason, this module isnt functional as of yet, I recommend using mouse, keyboard and pynput until I get the desired functionality out of flet.



--I kinda stopped developing it and instead just use this module to encapsulate pip install mouse & pip install keyboard. This way it will be easier to
make my codebase run mac/linux/windows/ios/android later on when Flet has the required functionality implemented.--"""




import mouse
def onLeftClick(callback):
    mouse.on_click(callback)
def onRightClick(callback):
    mouse.on_right_click(callback)
def onMiddleClick(callback):
    mouse.on_right_click(callback)



import typing

def on_mouse_press(callback: typing.Callable):
    pass
def on_middle_mouse_press(callback: typing.Callable):
    pass
def on_right_mouse_press(callback: typing.Callable):
    pass
def on_key_press(callback: typing.Callable):
    pass
def on_key_release(callback: typing.Callable):
    pass



from enum import Enum
import typing
import types


class InputEventReturnValue:
    """This base class serves as a holder to be able to attach additional data to input events in the future without breaking code already depending
    on this library. Atm though its kind of redundant as its only holding a single value that could as well have been returned directly.
    
    inputState is expected to be set accordingly by every instance of me."""
    def __init__(self, inputState, delta) -> None:
        self.inputState: typing.Any = inputState
        self.delta: typing.Any = delta
        "Supported by all event types, for InputEventReturnValueBOOL delta is either -1,0 or 1"

class InputEventReturnValueFLOAT(InputEventReturnValue):
    inputState: float

class InputEventReturnValueBOOL(InputEventReturnValue):
    inputState: bool

class InputEventReturnValueVECTOR2D(InputEventReturnValue):
    def __init__(self, position: list[float,float], delta: list[float,float, None]) -> None:
        self.delta: list[float, float] = delta
        self.position: list[float, float] = position
        super.__init__(self, position)
    inputState: list[float, float]

class InputEventReturnTypesEnum(Enum):
    BOOL = bool
    "Do or do not, there is no try"
    FLOAT_SIGNED =       float
    "Ranges -1 to 1"
    FLOAT_SIGNED_INF =   float
    "Ranges -inf to inf"
    FLOAT_UNSIGNED =     float
    "Ranges 0 to 1"
    FLOAT_UNSIGNED_INF = float
    "Ranges 0 to inf"
    VECTOR2D: list[float] = list
    "List of 2 floats representing X & Y coordinates, also has a special attribute 'delta' (which is for what you think it is for)"

class KeyTypesEnum(Enum):
    # Keyboard
    LETTER = "LETTER"
    FKEY = "FKEY" # Any key prefixed with F, F-1 - F-12
    OTHER = "OTHER" # Hard to categorize
    
class InputControllerTypesEnum(Enum):
    KEYBOARD = KeyTypesEnum
    MOUSE = "MOUSE"
    CONTROLLER = "CONTROLLER" # @note not yet supported, though I will add support if theres need for it.

class InputType():
    def __init__(self, name, controllerType: InputControllerTypesEnum, keyType: KeyTypesEnum = KeyTypesEnum.OTHER, returnType: InputEventReturnTypesEnum = InputEventReturnTypesEnum.BOOL) -> None:
        self.name = name
        self.controllerType = controllerType.value
        self.keyType = KeyTypesEnum
        self.returnType = returnType
        self.state: returnType.value

class InputTypesEnum(Enum):
    "Every enum value in here is required to have a unique name fed as first param, as other data is discarded when doing value comparisons on objects of type InputType."
    MOUSEMOVE   = InputType("MOUSEMOVE"      , InputControllerTypesEnum.MOUSE, returnType=InputEventReturnTypesEnum.VECTOR2D)
    MOUSESCROLL = InputType("MOUSESCROLL"    , InputControllerTypesEnum.MOUSE, returnType=InputEventReturnTypesEnum.FLOAT_SIGNED)
    LMB   = InputType("LMB"  , InputControllerTypesEnum.MOUSE   )
    RMB   = InputType("RMB"  , InputControllerTypesEnum.MOUSE   )
    MMB   = InputType("MMB"  , InputControllerTypesEnum.MOUSE   , returnType=InputEventReturnTypesEnum.FLOAT_SIGNED)
    A     = InputType("A"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    B     = InputType("B"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    C     = InputType("C"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    D     = InputType("D"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    E     = InputType("E"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    F     = InputType("F"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    G     = InputType("G"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    H     = InputType("H"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    I     = InputType("I"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    J     = InputType("J"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    K     = InputType("K"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    L     = InputType("L"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    M     = InputType("M"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    N     = InputType("N"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    O     = InputType("O"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    P     = InputType("P"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    Q     = InputType("Q"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    R     = InputType("R"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    S     = InputType("S"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    T     = InputType("T"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    U     = InputType("U"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    V     = InputType("V"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    W     = InputType("W"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    X     = InputType("X"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    Y     = InputType("Y"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    Z     = InputType("Z"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)
    Å     = InputType("Å"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)# These are special Swedish letters, why not I guess
    Ä     = InputType("Ä"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)#
    Ö     = InputType("Ö"    , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.LETTER)# Heh, would be fun to add the entire Chinese, Japanese & Korean alphabet
    F1    = InputType("F1"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F2    = InputType("F2"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F3    = InputType("F3"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F4    = InputType("F4"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F5    = InputType("F5"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F6    = InputType("F6"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F7    = InputType("F7"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F8    = InputType("F8"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F9    = InputType("F9"   , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F10   = InputType("F10"  , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F11   = InputType("F11"  , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    F12   = InputType("F12"  , InputControllerTypesEnum.KEYBOARD, KeyTypesEnum.FKEY)
    ENTER = InputType("ENTER", InputControllerTypesEnum.KEYBOARD)
# InputTypesEnum.A.value.state
import pynput
import keyboard

# keyboard.on_p
#class InputEventCondition():
#    def __init__(self, inputType, inputState = None) -> None:
#        self.inputType: InputType = inputType
#        self.inputState: typing.Any  = inputState
#        """Should NOT be of type {InputEventReturnValue}, but just a simple value like True, 1.0, False, 0.0. We can add 
#        support for InputEventReutrnValue & custom function/lambda based conditions in the future if proven useful (custom lambdas
#        could for instance be used to make conditions like checking if a float is greater than a required value).
#        
#        Value of "None" means that no state condition needs to be fullfilled."""
#
#    def __eq__(self, other: object) -> bool:
#        if isinstance(other, InputEventCondition):
#            if self.inputType == other.inputType:
#                if self.inputState == None or other.inputState == None: # @note Were treating an inputState of value None as if theres no state condition desired.
#                    return True
#                elif self.inputState.name == other.inputState.name:
#                    return True
#        return False
#    
#class EventHandler():
#    "Input event handler, can be used to register callbacks on key/mouse press/release/ticks. Instanciate before use"
#    _tickrate = 30
#    _callbacks: list[typing.Callable] = []
#    _inputEventConditionsWeAreLookingFor: list[InputEventCondition] = []
#
#    _pynputMouseListener: pynput.mouse.Listener = None
#    "May be replaced in the future if we move away from pynput."
#    _pynputKeyboardListener: pynput.keyboard.Listener = None
#    "May be replaced in the future if we move away from pynput."
#
#    def __init__(self):
#        pass
#
#    def _executeCallbacks(self, inputEventReturnValue: InputEventReturnValueBOOL):
#        for callback in self._callbacks:
#            if isinstance(callback, typing.Callable):
#                numberOfParameters = callback.__code__.co_argcount
#                if numberOfParameters > 0:
#                    callback(inputEventReturnValue)
#                else:
#                    callback()
#
#    def _refreshListeners(self):
#        def mouseClick(xPos, yPos, button: pynput.mouse.Button, isButtonDown):
#            shouldExecuteCallbacks = False
#            inputEventCondition: InputEventCondition = eval(f"{InputEventCondition.__name__}({InputTypesEnum.LMB if button == button.left else InputTypesEnum.RMB if button == button.right else button.middle}, {isButtonDown})")
#            for inputEventConditionIter in self._inputEventConditionsWeAreLookingFor:
#                if inputEventCondition == inputEventConditionIter:
#                    shouldExecuteCallbacks = True
#            
#            if shouldExecuteCallbacks:
#                self._executeCallbacks(InputEventReturnValueBOOL(isButtonDown))
#
#            # print(f"""mouse click 
#            # xPos {xPos} type: {type(xPos)}
#            # yPos {yPos} type: {type(yPos)}
#            # button {button} type: {type(button)}
#            # isButtonDown {isButtonDown} type: {type(isButtonDown)}
#            # """)
#        def mouseMove(xPos: float, yPos: float):
#            shouldExecuteCallbacks = False
#            for inputEventConditionIter in self._inputEventConditionsWeAreLookingFor:
#                if InputEventCondition(InputTypesEnum.MOUSEMOVE, None) == inputEventConditionIter:
#                    shouldExecuteCallbacks = True
#
#            if shouldExecuteCallbacks:
#                xyPos = [xPos, yPos]
#                if hasattr(self, "_mouseMoveMousePosPreviousEventCall"):
#                    delta = self._mouseMoveMousePosPreviousEventCall - xyPos
#                else:
#                    delta = [0,0]
#                self._executeCallbacks(InputEventReturnValueVECTOR2D(xyPos,delta))
#                self._mouseMoveMousePosPreviousEventCall = xyPos
#            # print(f"""mouse move 
#            # xPos {xPos} type: {type(xPos)}
#            # yPos {yPos} type: {type(yPos)}
#            # """)
#        def mouseScroll(xPos, yPos, unkonwnData = None, velocity: float = None):
#            shouldExecuteCallbacks = False
#            for inputEventConditionIter in self._inputEventConditionsWeAreLookingFor:
#                if InputEventCondition(InputTypesEnum.MOUSESCROLL, None) == inputEventConditionIter:
#                    shouldExecuteCallbacks = True
#
#            if shouldExecuteCallbacks:
#                self._executeCallbacks(InputEventReturnValueFLOAT())
#            
#            pass
#            # print(f"""mouse scroll 
#            # xPos {xPos} type: {type(xPos)}
#            # yPos {yPos} type: {type(yPos)}
#            # unkonwnData {unkonwnData} type: {type(unkonwnData)}
#            # velocity {velocity} type: {type(velocity)}
#            # """)
#        try:
#            self._pynputMouseListener.stop()
#        except:
#            pass
#        self._pynputMouseListener = pynput.mouse.Listener(on_click=mouseClick, on_move=mouseMove, on_scroll=mouseScroll)
#        self._pynputMouseListener.start()
#
#    def registerInputTrigger(self, inputType: InputType, valueRequiredToTriggerEventOptional: typing.Union[None, float, bool, list] = None):
#        "Append another input & value condition to the event listener(s)"
#        pass
#    
#    def registerCallback(self, callback: typing.Callable):
#        "Append another callback to get executed when any of the inputs are triggered with a conditionally satesfying return value"
#
#    def __exit__(self):
#        self.kill()
#
#    def kill(self):
#        "Murder me"



if False:
    import asyncio
    import time
    from pynput import keyboard
    from pynput import mouse


    # KEYBOARD
    def on_activate(data = None):
        print(f'on_activate datatype: {type(data)} data: {data}')
    def on_activate2(data = None):
        print(f'on_activate2 datatype: {type(data)} data: {data}')
    def on_activate3(data):
        print(f'on_activate3 datatype: {type(data)} data: {data}')
    e = keyboard.Listener(on_press=on_activate3)
    e.start()
    e = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+h': on_activate,
            '<ctrl>+<alt>+i': on_activate2})
    asyncio.new_event_loop().run_in_executor(None, e.start(), [])
    # KEYBOARD END

    # MOUSE
    mouseController = mouse.Controller()
    print(f"mousePos: {mouseController.position}")
    def mouse_click(data, data2, data3 = None, data4 = None):
        print(f"""mouse click 
        data {data} type: {type(data)}
        data2 {data2} type: {type(data2)}
        data {data3} type: {type(data3)}
        data2 {data4} type: {type(data4)}
        """)
    def mouse_move(data, data2, data3 = None, data4 = None):
        print(f"""mouse move 
        data {data} type: {type(data)}
        data2 {data2} type: {type(data2)}
        data {data3} type: {type(data3)}
        data2 {data4} type: {type(data4)}
        """)
    def mouse_scroll(data, data2, data3 = None, data4 = None):
        print(f"""mouse scroll 
        data {data} type: {type(data)}
        data2 {data2} type: {type(data2)}
        data {data3} type: {type(data3)}
        data2 {data4} type: {type(data4)}
        """)
    e = mouse.Listener(on_click=mouse_click, on_move=mouse_move, on_scroll=mouse_scroll)
    e.start()
    # MOUSE END

    time.sleep(100)
