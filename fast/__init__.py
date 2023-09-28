####################################################
# Fast is a general purpose developer productivity #
# library for Python. Written by Olliver Aira.     #
####################################################
#                ______           __               #
#               / ____/___ ______/ /_              #
#              / /_  / __ `/ ___/ __/              #
#             / __/ / /_/ (__  ) /_                #
#            /_/    \__,_/____/\__/                #
#                                                  #
####################################################
# Text generated with https://www.fancytextpro.com/BigTextGenerator/Slant
"""
Fast is a general purpose developer productivity 
library for Python. Written by Olliver Aira.     
"""
from . import pkgsAndModules

moduleName = "fast"
dependencyList = [  # @todo move dependencies into each respective submodule now that we have lazy loading for partial module initialization,
                    #       current approach also clutters the fast namespace.
    # ["packageName", "moduleName"],
    ["opencv-python", "cv2"],
    ["mss", "mss"],  # used for  video recording.
    ["pillow", 'PIL']
]
"""@note This list strive towards being a complete list of libraries
that we depend on (that doesnt ship with the cpython interpreter).
All packages used here should be available via PyPi. If you see a
dependency used  anywhere in this project that isnt listed here,
please add it!"""


def installDependenciesViaPypi():
    "Installs all missing dependencies of this module via PyPi"
    for pkgAndModule in dependencyList:
        pkgsAndModules.installPackageIfCorrespondingModuleIsUndefined(pkgAndModule[0], pkgAndModule[1])
class _:
    import sys
    if sys.platform == "win32":
        try:
            import win32api
            import os
            win32api.SetConsoleCtrlHandler(lambda a=None: _.os.kill(_.os.getpid(), 15)) # Enables ctrl+C to kill the terminal on Windows. 15 == signal.SIGTERM
        except:
            pass
# import sys
# sys.path.append(r"C:\PythonPathLibraries")
hiddenimports = "classes"
try:
    # if pkgsAndModules.importModule("from .data import data").TYPE_CHECKING:
    from . import debugging
    from .debugging import print
    from .data import data
    if pkgsAndModules.importModule("from . import arithmetics").TYPE_CHECKING:
        from . import arithmetics
    if pkgsAndModules.importModule("from . import string").TYPE_CHECKING:
        from . import string
    if pkgsAndModules.importModule("from . import color").TYPE_CHECKING:
        from . import color
    if pkgsAndModules.importModule("from . import asyncronous").TYPE_CHECKING:
        from . import asyncronous
    if pkgsAndModules.importModule("from . import video").TYPE_CHECKING:
        from . import video
    if pkgsAndModules.importModule("from . import classes").TYPE_CHECKING:
        from . import classes
    if pkgsAndModules.importModule("from . import input").TYPE_CHECKING:
        from . import input
    if pkgsAndModules.importModule("from . import files").TYPE_CHECKING:
        from . import files
    if pkgsAndModules.importModule("from . import events").TYPE_CHECKING:
        from . import events
    if pkgsAndModules.importModule("from . import collections").TYPE_CHECKING:
        from . import collections
    if pkgsAndModules.importModule("from . import networking").TYPE_CHECKING:
        from . import networking
    if pkgsAndModules.importModule("from . import ui").TYPE_CHECKING:
        from . import ui
    if pkgsAndModules.importModule("from . import db").TYPE_CHECKING:
        from . import db
    if pkgsAndModules.importModule("from . import console").TYPE_CHECKING:
        from . import console
    if pkgsAndModules.importModule("from . import random").TYPE_CHECKING:
        from . import random
    if pkgsAndModules.importModule("from . import processes").TYPE_CHECKING:
        from . import processes
    if pkgsAndModules.importModule("from . import devTools").TYPE_CHECKING:
        from . import devTools
    if pkgsAndModules.importModule("from . import visualize3d").TYPE_CHECKING:
        from . import visualize3d
    # if pkgsAndModules.importModule("from . import debugging; from .debugging import print").TYPE_CHECKING:

except ModuleNotFoundError as exception:
    print("####################################")
    print("# Module Not Founder Error in Fast #")
    print("####################################")
    print(exception)
