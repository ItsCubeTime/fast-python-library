import os
import sys
import time
import typing

from .. import asyncronous, files

import pathlib


def reloadOnChange(paths=[sys.argv[0], pathlib.Path(__file__).parent.parent.as_posix()], blocking=True, watchDir=True, cb: typing.Callable | list = [], parameters: str = "", parametersCb = lambda: "", restartLatency=0):
    "watchDir watches the entire directory if a file path is fed in."
    if not isinstance(cb, typing.Collection):
        cb = [cb]
    if not isinstance(paths, typing.Collection) or isinstance(paths, str):
        paths = [paths]
    fileToStartUponReload = sys.argv[0]
    for path in paths:
        # path = paths[0]
        # if True:
        path = files.Path(path)
        if watchDir and path.isFile():
            path = path.getParentFolder()

        def watchCb(path: files.Path):
            # if not path.getName().lower() in ["__pycache__", "tempCodeRunnerFile.py"]:
            from .. import debugging
            from .. import string
            from .. import data
            print(debugging.colorString(string.putTextInBox(f"{data.libraryName}: Reloading, file changes detected in: {path}"), debugging.TERMINAL_COLORS.GREEN))
            time.sleep(restartLatency)
            os.system(f'''{sys.executable} "{fileToStartUponReload}" {parameters} {parametersCb()} reload''') 
            # os.system(f'''{sys.executable} {(pathlib.Path(__file__).parent / 'startWithLatency.py').as_posix()} 0.2 {sys.executable} "{fileToStartUponReload}" {parameters} {parametersCb()} reload''')
            asyncronous.killProcess(os.getppid())
    #         os.system(f''' 
    # python -c """
    # import time
    # import os
    # time.sleep(2)
    # os.system(f'"{sys.executable}" "{pathStr}"')
    # """
    #         ''')
        for callback in cb:
            path.addWatcher(callback)
        path.addWatcher(watchCb)
    if blocking:
        while True:
            time.sleep(10000)
