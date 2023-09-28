from __future__ import annotations


# from enum import Enum as _Enum
# import enum
# import aenum
# from aenum import StrEnum
# from aenum import Enum as _Enum
# import aenum as _aenum

# def extendEnum(inherited_enum):
#     def wrapper(added_enum):
#         joined = {}
#         for item in inherited_enum:
#             joined[item.name] = item.value
#         for item in added_enum:
#             joined[item.name] = item.value
#         return _Enum(added_enum.__name__, joined)
#     return wrapper
class Key():
    "Also used for mouse buttons - and would also be used for other kinds of input devices in the future, like game controllers if we ever add support."
    #    LMB RMB MMB A B C D E F G H I J K L M N O P Q R S T U V W X Y Z N1=1 N2=2 N3=3 N4=4 N5=5 N6=6 N7=7 N8=8 N9=9 N0=0 SPACE=' ' TAB MINUS=- PLUS=+ DOT=. COMMA=, UP DOWN LEFT RIGHT SHIFT CTRL CMD ALT ENTER BACKSPACE
    LMB       = 'LMB'
    RMB       = 'RMB'
    MMB       = 'MMB'

    A         = 'A'
    B         = 'B'
    C         = 'C'
    D         = 'D'
    E         = 'E'
    F         = 'F'
    G         = 'G'
    H         = 'H'
    I         = 'I'
    J         = 'J'
    K         = 'K'
    L         = 'L'
    M         = 'M'
    N         = 'N'
    O         = 'O'
    P         = 'P'
    Q         = 'Q'
    R         = 'R'
    S         = 'S'
    T         = 'T'
    U         = 'U'
    V         = 'V'
    W         = 'W'
    X         = 'X'
    Y         = 'Y'
    Z         = 'Z'
    Å         = 'Å'
    Ä         = 'Ä'
    Ö         = 'Ö'

    N1        = '1'
    N2        = '2'
    N3        = '3'
    N4        = '4'
    N5        = '5'
    N6        = '6'
    N7        = '7'
    N8        = '8'
    N9        = '9'
    N0        = '0'

    SPACE     = ' '
    TAB       = 'TAB'
    ENTER     = 'ENTER'
    BACKSPACE = 'BACKSPACE'

    SHIFT     = 'SHIFT'
    CTRL      = 'CTRL'
    CMD       = 'CMD'
    ALT       = 'ALT'

    MINUS     = '-'
    PLUS      = '+'
    DOT       = '.'
    COMMA     = ','

    UP        = 'UP'
    DOWN      = 'DOWN'
    LEFT      = 'LEFT'
    RIGHT     = 'RIGHT'






class FlowDirection():
    HORIZONTALLY = 0
    VERTICALLY = 1

class QuadSidesEnum():
    TOP = "TOP"
    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"
    LEFT = "LEFT"

class QuadCornersEnum():
    TOPLEFT = "TOPLEFT"
    TOPRIGHT = "TOPRIGHT"
    BOTTOMLEFT = "BOTTOMLEFT"
    BOTTOMRIGHT = "BOTTOMRIGHT"

# @extendEnum(QuadSidesEnum)
class QuadCorndersNSidesEnum(QuadCornersEnum, QuadSidesEnum):
    pass

class Platform:
    "If platform is unkown, return None"
    macos = 'macos'
    windows = 'windows'
    linux = 'linux'

    android = 'android'
    ios = 'ios'

    playstation = 'playstation'
    xbox = 'xbox'
    switch = 'switch'
    
    microPython = 'microPython'

class PlatformType:
    '''If platform type is unkown, return None

    If you need to know if your python instance is running as a server, use fast.data.isServer (bool) instead.'''
    desktop = 'desktop'
    mobile = 'mobile'
    console = 'console'
    tv = 'tv'
    "A smart TV of some sort, could for instance be a Blu-Ray player with webbrowsing capabilities."
    embedded = 'embedded'
    '''In this context, a device is only counted as embedded if its not running a desktop considerable OS, A raspberry Pi running linux would not count as embedded even if the Linux distro is heavily  shaved off features & barebones - and even if the raspberry pi is used for tasks typically given to embedded devices.
    
    A microcontroller running microPython would be an example of an embedded device as in this case, theres no OS.'''