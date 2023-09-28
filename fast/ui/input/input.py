import nicegui
from ... import asyncronous
def getMousePos(windowRelative=True, client=None):
    if client==None:
        client = nicegui.globals.get_client()
    print(asyncronous.runSync(client.run_javascript('[cursorX, cursorY]')))

from ... import classes

classes.enums.Key


def getKeyState(key: classes.enums.Key):
    "Also used for mouse buttons - and would also be used for other kinds of input devices in the future, like game controllers if we ever add support."
    