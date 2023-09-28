from __future__ import annotations
import inspect

import os
import pathlib
import time
import typing

from .. import asyncronous, classes
from ..classes import property

# @note Some notes about pathlib:
# * is_dir() is true also for folder like symlinks. is_file() is true for file like symlinks.


class Path(classes.Base):
    "A file or folder"
    def __new__(cls, path):
        returnVal = super().__new__(cls)
        if issubclass(cls, Path):
            return returnVal
        pathStr = str(path)
        pathlibObj = pathlib.Path(pathStr)
        if pathlibObj.is_file():
            return File(path)
        elif pathlibObj.is_dir():
            return Folder(path)

    def __init__(self, path: typing.Union[str, pathlib.Path, Path]) -> None:

        if isinstance(path, Path):
            pathAsStr = path.__str__()
        elif isinstance(path, str):
            pathAsStr = path
        elif isinstance(path, pathlib.Path):
            pathAsStr = path.resolve().__str__()
        else:
            raise Exception(f"Parameter 'path' {path} of invalid type {type(path)}.")
        self.pathlibObj = pathlib.Path(pathAsStr)

    def __str__(self) -> str:
        return self.pathlibObj.as_posix()

    def getName(self, includeFolderStructure=False, includeFileExtension=True):
        "Returns a file/folder name, including or excluding above file structure, including or excluding file extension."
        returnVal = self.__str__()
        if not includeFolderStructure and returnVal.__contains__('/'):
            returnVal = returnVal[returnVal.rindex('/')+1:]
        if not includeFileExtension and returnVal.__contains__('.'):
            returnVal = returnVal[:returnVal.rindex('.')]
        return returnVal

    def isFile(self):
        "Symlink pointing to file counts as file"
        return self.pathlibObj.is_file()
    
    def isImage(self):
        if self.isFile():
            extension = self.getExtension()
            if extension in ["png", "jpg", "jpeg", "exr", "webp"]:
                return True
        return False
    
    def getExtension(self):
        "Get the file extension excluding the . (dot)"
        name = self.getName()
        return name[name.rfind('.')+1:]
    
    def exists(self):
        return self.pathlibObj.exists()

    def isFolder(self):
        "Symlink pointing to folder counts as folder"
        return self.pathlibObj.is_dir()

    def getParentFolder(self):
        return Path(self.pathlibObj.parent)

    __watchers__: list[typing.Callable] = []
    __asyncRunner__ = None

    def addWatcher(self, cb: typing.Callable):
        """Limitations of this file watching functionality includes: 

        * file changes is checked on tick (on a separate thread), this introuce latency for detection.
        * If the top directory or file is renamed/moved we continue watching, but we wont be calling any callbacks to inform about this. In the future 
          I might add additional addCreationWatcher() & addDeletionWatcher() methods for this scenario (if ever needed).
        """
        self.__watchers__.append(cb)
        # Start watcher
        if not self.__asyncRunner__:
            self.__asyncRunner__ = asyncronous.runAsyncLooping(self.__watcherTick__, intervalSec=1/7, useThreading=True)
        return self

    def removeWatcher(self, cb: typing.Callable):
        while cb in self.__watchers__:
            self.__watchers__.remove(cb)
        if len(self.__watchers__) < 1:
            # Stop watcher
            self.__asyncRunner__.isRunning = False
        return self

    def removeAllWatchers(self):
        self.__watchers__.clear()
        if self.__asyncRunner__:
            self.__asyncRunner__.isRunning = False
        return self

    watcherMinTimeBetweenCallbacks = 1
    __watcherTickLastModifiedDate__ = time.time()+watcherMinTimeBetweenCallbacks
    watcherIgnorePathNames: list[str] = ["__pycache__"]

    "In seconds"

    def getLastModifiedTime(self):
        return os.path.getmtime(self.pathlibObj.as_posix())

    def __watcherTick__(self):
        if time.time() < self.watcherMinTimeBetweenCallbacks+self.__watcherTickLastModifiedDate__:
            return
        # self.pathlibObj.is_dir()
        if not self.pathlibObj.exists():
            return
        lastModifiedPath: Path = None
        newLastModifiedDate = self.getLastModifiedTime()
        if self.isFolder:
            for root, dirs, files in os.walk(self.pathlibObj.as_posix()):
                for name in files: # @note Turns out its not enough checking just dirs
                    file_path = os.path.join(root, name)
                    newLastModifiedDate = max(newLastModifiedDate, os.path.getmtime(file_path))
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    if dir_path in self.watcherIgnorePathNames:
                        continue
                    dir_path_last_mod_time = os.path.getmtime(dir_path)
                    if dir_path_last_mod_time > newLastModifiedDate:
                        newLastModifiedDate = dir_path_last_mod_time
                        lastModifiedPath = Path(dir_path)
        # print(f"new: {newLastModifiedDate} old: {self.__watcherTickLastModifiedDate__}")
        
        if newLastModifiedDate > self.__watcherTickLastModifiedDate__:
            if lastModifiedPath == None:
                lastModifiedPath = self
            for cb in self.__watchers__:
                try:
                    if (cb.__code__.co_argcount > 0 and not inspect.ismethod(cb)) or cb.__code__.co_argcount > 1:
                        cb(lastModifiedPath)
                    else:
                        cb()

                except Exception as exc:
                    print(f"file __watcherTick__ exception '{exc}'")
        self.__watcherTickLastModifiedDate__ = newLastModifiedDate

    def __appendPathsInternal__(self, firstPart, secondPart):
        "Implementation detail, do not call directly"
        return Path((str(firstPart) + '/' + str(secondPart)).replace('//', '/'))
    
    def __add__(self, other):
        "Enables use of the + operator, 'C:/path'+'hello' would return a path pointing to 'C:/path/hello'"
        return self.__appendPathsInternal__(self, other)
    
    def __radd__(self, other):
        "Enables use of the + operator, 'C:/path'+'hello' would return a path pointing to 'C:/path/hello'"
        return self.__appendPathsInternal__(other, self)
    
    def __truediv__(self, other):
        "Enables use of the / operator, 'C:/path'/'hello' would return a path pointing to 'C:/path/hello'"
        return self.__appendPathsInternal__(self, other)
    
    def __rtruediv__(self, other):
        "Enables use of the / operator, 'C:/path'/'hello' would return a path pointing to 'C:/path/hello'"
        return self.__appendPathsInternal__(other, self)


class File(Path):
    "A file"

    def getContent(self, binary=False):
        "Returns text content of file as str, if theres no valid file at this path, return an empty str."
        if self.pathlibObj.exists() and self.isFile():
            with self.pathlibObj.open(mode='rb' if binary else 'r') as file:
                return file.read()
        return ""

    def createFile(self):
        self.pathlibObj.open("w+")
        return self

    def setContent(self, string: str|bytes):
        "Overrides existing text contents of file. Does nothing if theres something that isnt a file on this path (like a folder). Writing data in binary can cut file sizes in half compared to storing the binary data as strings!"
        binary = isinstance(string, bytes)
        if not binary:
            string = str(string)
        if not self.exists() or not self.isFile():
            self.createFile()
        with self.pathlibObj.open(mode='w' if not binary else 'wb') as file:
            file.write(string)
        return self

    def addContent(self, string: str|bytes):
        "Adds to existing text contents of file. Does nothing if theres something that isnt a file on this path (like a folder). Writing data in binary can cut file sizes in half compared to storing the binary data as strings!"
        binary = isinstance(string, bytes)
        if not binary:
            string = str(string)
        if not self.exists() or not self.isFile():
            self.createFile()
        with self.pathlibObj.open(mode='a' if not binary else 'ab') as file:
            file.write(string)
        return self


def createFile(path: Path, createFolderStructureIfNeeded=True):
    path = Path(path)
    if not path.pathlibObj.exists():
        try:
            path.pathlibObj.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            if not 'already exists' in str(exc):
                raise Exception
    return File(Path)


def createFolder(path: Path, createFolderStructureIfNeeded=True):
    path = Path(path)
    if not path.pathlibObj.exists():
        try:
            path.pathlibObj.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            if not 'already exists' in str(exc):
                raise Exception
    return Folder(path)


# class fileWatch:
#     "File/folder watching functionality with no dependencies beyond STD"
#     def watchDirectory(callback: typing.Callable):
#         pass


class Folder(Path):
    "A folder"

    def getChildPathsRecursive(self: Folder) -> list[Path]:
        "Returns every file and folder in a directory recursively, excluding the directory you feed in."
        returnVal: list[Path] = []

        def appendChildren(path: pathlib.Path):
            for pathInner in path.glob('*'):
                pathInner: pathlib.Path
                if pathInner.is_dir():
                    appendChildren(pathInner)
            returnVal.append(path)
        appendChildren(self.pathlibObj)
        returnVal = [Path(path) for path in returnVal]
        return returnVal

    def getChildPaths(self: Folder) -> list[Path]:
        "Get files n folders in this folder."
        returnVal: list[Path] = []
        path = self.pathlibObj
        for path in path.glob('*'):
            returnVal.append(Path(path))
        return returnVal
    
    def getAvailableSubpath(self: Folder, subpathNameLength=4):
        """@todo see if its possible to get an available folder name more directly, currently this function is not suitable for creating a large set of subdirectories as it will get slower the more folders you create with it.
        
        fast.db uses a solution where we create a file in each directory to keep track of folders we've already created, so it might be a better fit for situations where you want a lot of files."""
        import uuid
        while True:
            random = uuid.uuid4()[:subpathNameLength]
            newPath = Path(self+random)
            if not newPath.exists():
                return newPath


    def createSubfolder(self: Folder, name=None):
        return createFolder(self.getAvailableSubpath() if name==None else self+name)

    def createSubfile(self: Folder, name=None):
        return createFile(self.getAvailableSubpath() if name==None else self+name)

    createFile = createFile
    createFolder = createFolder


class dangerZone():
    def removePath(path: Path, deleteNestedDirectory=False, deleteContentsOfSymlinks=False) -> bool:
        "Deletes files, symlinks & directories. Returns success state. "
        success = False
        path = Path(path)
        if deleteNestedDirectory:
            filesToDel: list[pathlib.Path] = []
            foldersToDel: list[pathlib.Path] = []

            def deleteNestedDirectory_(pth: pathlib.Path):
                for child in pth.glob('*'):
                    if child.is_file():
                        filesToDel.append(child)
                    else:
                        if child.is_dir():
                            deleteNestedDirectory_(child)
                foldersToDel.append(pth)

            deleteNestedDirectory_(path.pathlibObj)

            success = True
        else:
            if path.pathlibObj.is_file():
                path.pathlibObj.unlink()
                success = True
            if path.pathlibObj.is_dir():
                hasChildren = False
                for childPath in path.pathlibObj.glob('*'):
                    hasChildren = True
                    break
                if not hasChildren or deleteNestedDirectory:
                    path.pathlibObj.rmdir()
                    success = True

        return success

from .. import data
tempDir = createFolder(Folder(data.tempDir))
"Create subfolders & file in me."
import atexit
atexit.register(lambda a=None: dangerZone.removePath(tempDir))