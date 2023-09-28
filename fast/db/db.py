from typing import Any, TYPE_CHECKING
from .. import files
from collections.abc import Iterable

import pickle

# pickle.dump

from pydoc import locate

class LocalStorageContainer():
    """An object that can be iterated over and that can host child values"""
    # _hasFinishedInitialization = False
    useCompression = True
    # folder = None
    def __init__(self, path: str|files.Folder, createFolder=True) -> None:
        self.folder = files.Folder(str(path))
        if createFolder:
            self.folder.createFolder()
    def __new__(self, path: str|files.Folder, createFolder=None):
        import inspect
        from .. import debugging
        # print(f"newFolder {debugging.print(Exception(''))} <-")
        return super(LocalStorageContainer, self).__new__(self)
        # self._hasFinishedInitialization = True

    def __getattr__(self, __name: str) -> Any:
        # __name = str(__name)
        ls = LocalStorageContainer(self.folder + __name)
        if ls.folder.exists():
            if ls.folder.isFolder():
                return ls
            rawFileContent = files.File(ls.folder).getContent(binary=True)
            if str(rawFileContent[0]) == '40': # Assume that this means the data is compressed.
                                               # 40 in the ascii table is '('
                import zstandard as zstd
                rawFileContent = zstd.decompress(rawFileContent)
            if not b'\n' in rawFileContent:
                # print("noNewLine")
                return None
            type, value = rawFileContent.split(b'\n', 1)
            type = type.replace(b'\r', b'')
            # value = value.replace(b'\\\\', b'\\')
            if type == b'pic':
                return pickle.loads(value)
            elif type == b'dil':
                import dill
                return dill.loads(value)
            # print(type)
            # print(f"value: '{value}, type: {type}")
            returnVal = locate(type.decode())(value)
            return returnVal[2:-1] if type == b'str' else returnVal
        # print(f"doesnt exist: {ls.folder} selffolder: {self.folder}")
        return None
    # self.__getattr__ = __getattr__
    
    def __setattr__(self, __name: str, __value) -> Any:
        originalValue = __value
        alwaysCompress = False
        if __name in ['folder', 'treatIndex']:
            self.__dict__[__name] = __value
            return __value
        if isinstance(__value, Iterable) and not isinstance(__value, str):
            return LocalStorageContainer(self.folder + __name)
        else:
            if type(__value)  in [str, int, float, bytes]:
                varType = bytes(type(__value).__name__, 'utf-8')
                __value = str(__value).encode()
                # decode = False
            else:
                # decode = True
                # Pickle
                alwaysCompress = True
                try:
                    __value = pickle.dumps(__value)
                    varType = b'pic' # for pickle, everything to save those bytes :P
                except:
                    import dill
                    __value = dill.dumps(__value)
                    varType = b'dil' # for dill, everything to save those bytes :P
            # @todo remove any potential folder that could already be living here
            file =  files.File(self.folder + __name)
            # print(f"setContent file: {file}, name: {__name}, val: \n{__value}\n")
            # file.setContent()
            # import zstd
            finalBytes = varType + b'\n' + __value
            if self.useCompression and (finalBytes.__len__() > 200 or alwaysCompress): # If compression is enabled, compress anything with a charcount longer than 200 or if using dill or pickle
                import zstandard as zstd
                finalBytes = zstd.compress(finalBytes, 2)
            files.dangerZone.removePath(file)
            file.createFile()
            file.setContent(finalBytes)
            # file.addContent(str(__value)[2:-1] if decode else __value)
            return originalValue
        
    def __iter__(self):
        for path in self.folder.pathlibObj.iterdir():
            # print(f"pathName: {path.name}")
            if path.name == '-':
                continue
            yield self.__getitem__(path.name)

    def treatIndex(self, index: int):
        "Takes something like -5 and spits out its coresponding positive value. If were given a non-integer, we return the value that was fed in."
        if isinstance(index, int) and index < 0:
            dataFile = files.File(self.folder + '-')
            if dataFile.exists():
                numberOfItems = int(dataFile.getContent()) # 1 means 1 file.
                return numberOfItems+index # eg 5 + -1
        return str(index)
    def getLastIndex(self):
        "Returns -1 if there are no items in the list yet"
        dataFile = files.File(self.folder + '-')
        if dataFile.exists():
            numberOfItems = int(dataFile.getContent()) # 1 means 1 file.
            return numberOfItems # eg 5 + -1
        return -1
        
    def pop(self, index):
        self.__delattr__(index)
    def __delattr__(self, __name: str) -> None:
        files.dangerZone.removePath(self.folder + __name)
    def append(self, data):
        self.__setattr__(str(self.getLastIndex()+1), data)
        
    def __delitem__(self, __name):
        self.__delattr__(__name)
    def __getitem__(self, __name):
        # print(f"__nameUntreated {__name} __nameTreated {self.treatIndex(__name)}")
        return self.__getattr__(self.treatIndex(__name))
    def __setitem__(self, __name, __value):
        # print(f"__nameUntreated {__name} __nameTreated {self.treatIndex(__name)}")
        __name = self.treatIndex(__name)
        path: files.Path = self.folder + __name
        dataFile = files.File(self.folder + '-')
        dataFileExists = dataFile.exists()
        if not path.exists() or not dataFileExists:
            if dataFileExists:
                previosNumberOfFiles = int(dataFile.getContent())
            else:
                previosNumberOfFiles = 0
                dataFile.createFile()
            dataFile.setContent(previosNumberOfFiles+1)
        self.__setattr__(__name, __value)
        return __value
        
    # self.__setattr__ = __setattr__
# class LocalStorageValue():
#     "An object that stores a simple string on disk"
#     def __init__(self, path: str|files.File) -> None:
#         self.file = files.File(str(path))
#         self.file.createFile()
#     def 
class LocalStorage(LocalStorageContainer):
    def __init__(self, path: str|files.Folder, createFolder=True) -> None:
        # self._hasBeenInitialized = initializeDir
        self.folder = files.Folder(str(path))
        # if initialize:
        super().__init__(path, createFolder=createFolder)
    
    # def initialize(self):
    #     if not self._hasBeenInitialized:
    #         super().__init__(self.folder)
    #     self._hasBeenInitialized = True

class AppData(LocalStorage):
    if TYPE_CHECKING:
        userSettings: LocalStorageContainer


from .. import data
appdata = AppData(data.appDataDirectory+'fastdb', createFolder=False)







# class RemoteStorage():
#     def __init__(self, adress:str, username: str, password: str) -> None:
#         "adress is 123.123.123:3213, could point to local IPs"