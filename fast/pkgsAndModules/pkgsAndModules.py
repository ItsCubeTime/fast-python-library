import importlib
import inspect
import os
import sys
import types
import typing
from .. import string

_sitePkgsDir = False

installedPackages: list[str] = []
def installPackage(package):
    try:
        import pip
    except:
        try:

            # from ... import pip
            import os
            sourceDir = __file__.replace('\\', '/')
            sourceDir = sourceDir.split('/')
            sourceDir = "/".join(sourceDir[:-3]) + "/pip"

            destDir: str = ""
            global _sitePkgsDir
            if not _sitePkgsDir:
                for dir in sys.path:
                    if dir.endswith("site-packages"):
                        _sitePkgsDir = dir.replace('\\', '/')
                        if _sitePkgsDir.__contains__('site-packages/site-packages'):
                            _sitePkgsDir = _sitePkgsDir[:_sitePkgsDir.index("site-packages", _sitePkgsDir.index("site-packages")+"site-packages".__len__())-1].replace('//', '/')
            destDir = _sitePkgsDir
            destDir = (destDir + '/pip')
            # destDir = (sysconfig.get_pahs()['platlib'].replace('\\', '/') + '/pip').replace('//', '/')
            # print(sourceDir)
            # print(destDir)
            os.symlink(sourceDir, destDir, True)
            import time
            
            time.sleep(0.5)
            import pip
        except Exception as exc:
            msg = f"Exc in fast.pkgsAndModules.installPackage: {exc}"
            print(msg)
            open(r"C:\Users\olliv\Desktop\Art And Development\Krita\Development\FastBlenderToKritaLiveLink\testing\con", "a+").write(msg)
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def installPackageIfCorrespondingModuleIsUndefined(packageName: str, moduleName: str): 
    if packageName.lower() in installedPackages:
        return
    # print(f"Importing module {moduleName}")
    try:
        importlib.import_module(moduleName)
        # from PIL import Image
    except Exception as error:
        # print(string.putTextInBox(f"Error: ---\n{error}\n---\nwhen attempting to import {moduleName}, we're assuming that you dont have {packageName} installed and will try to install it for you!"))
        installPackage(packageName)
        try:
            importlib.import_module(moduleName) # Doesnt actually work? 
        except:
            # print("First attempt of importing module failed, launching a new console and attempting from there.")
            stream = os.popen(f"{sys.executable} -m pip install {packageName}")
            
            # print(f"Output from pip install console \n\n->\n {stream.read()} \n<-\n\n")
        installedPackages.append(packageName.lower())

            
    

import importlib
import inspect
import types
import typing


class importModule(types.ModuleType, object):
    """Acts as an alternative to pythons import statement. Returns a module by module name. Usage eg: 'importModule('math')'.
    If lazyLoad==True we return a dummy object that will replace itself with the proper module the first time you try accessing a module inside it. This can help avoid
    runtime initialization errors if an unused part of a module has issues, say if an unused submodule of a module has dependencies that arent installed. Could
    also reduce program startup times significantly. 
    
    For instance: Say you've written a library that uses no dependencies, except for a particular submodule which requires, say open-cv. 
    With the help of lazyLoading you can make it so you can still use your library without open-cv as long as you dont access any members of the submodule that requires
    open-cv, by using importModule to import the submodule in your parent package.
    
    PyLance doesnt support dynamic imports, for this reason you may need to accompany this statement with a simple import moduleName to get autocompletion features in your  IDE.

    ✨Demo:

    import typing

    if typing.TYPE_CHECKING:
        import math
    else:
        importModule("math)

    ✨or a shorter variant which does the same thing:

    if importModule("math").TYPE_CHECKING: # Yes, this actually creates a new identifier "math" in the scope were calling importModule()
        import math                        # This never executes in a real program, only meant to add support for type hinting.

    ✨and something more elaborate:

    if importModule("math").TYPE_CHECKING:
        import math # This line enables intellisense, at runtime, this never actually executes
    if importModule("from . import testModule").TYPE_CHECKING:
        from . import testModule # This line enables intellisense, at runtime, this never actually executes
    import time
    time.sleep(1.5)
    print(testModule.testVar) # This is when testModule gets imported
    time.sleep(1.5)
    print(math.acos(0.4))     # This is when math gets imported
    """
    
    __finishedInitialization__ = False
    hasModuleBeenLoaded = False
    def __new__(cls, moduleNameOrImportExpression: str, lazyLoad = True, __callStack__: inspect.FrameInfo = None):
        
        if __callStack__ == None:
            __callStack__ = inspect.stack()[1]
        # print("moduleName: ", moduleName)

        # Prep variables BEGIN
        moduleNameOrImportExpressionSplit = moduleNameOrImportExpression.split(' ')
        if moduleNameOrImportExpressionSplit.__len__() > 1:
            if moduleNameOrImportExpression.__contains__("import"):
                moduleName = moduleNameOrImportExpressionSplit[moduleNameOrImportExpressionSplit.index("import")+1]
                moduleImportExpression = moduleNameOrImportExpression
            else:
                Exception("Invalid value of moduleNameOrImportExpression in importModle initialization.")
        else:
            moduleName = moduleNameOrImportExpression.replace('.', '')
            moduleImportExpression = f"import {moduleNameOrImportExpression}"
        # Prep variables END

        if typing.TYPE_CHECKING or not lazyLoad: 
            # print(f"locals -> {__callStack__} \n\n{os.path.dirname(__callStack__.filename)}<-")
            # __import__
            backSlash = "\\"
            pathToInsert = os.path.dirname(__callStack__.filename).replace(backSlash, "/")
            
            exec(fr"""
import sys 
sysPathContainedPath = True
if not sys.path.__contains__("{pathToInsert}"): # @note Not sure if the 1 index is a special index that could potentially cause issues if sys.path
    sys.path.insert(-1, r'{pathToInsert}')         # already contained the path we are searching, but on a different index than one.
    sysPathContainedPath = False
if locals().__contains__("{moduleName}"):
    del {moduleName} # @note the identifier corelated to the module we are about to import have already been defined as our ImportModule dummy object
                     # if we used ImportModule with lazyLoad = True. For that reason, if we were to run from . import subModule, it would import this
                     # dummy object again rather than the actual module! So we need to delete it first & then import to override with the true module.
{moduleImportExpression} 
globals()['{moduleName}'] = {moduleName}
if not sysPathContainedPath:
  sys.path.remove("{pathToInsert}")
""",                                                       __callStack__[0].f_locals) # Unfortunately this doesn't let PyLance see the import,  it requires a
            returnVal = eval(f"globals()['{moduleName}']", __callStack__[0].f_locals) # "Hardcoded" module name that cant be passed by string via the import statement. 
                                                                                      # Im hoping this will enable autocompletion in other language servers however      
            returnVal.hasModuleBeenLoaded = True
            # print(f"fast.pkgsAndModules.importModule moduleImportExpression: '{moduleImportExpression}' moduleName: '{moduleName}' __callStack__: {__callStack__}")
                                                
        else:
            # print("fast.pkgsAndModules.importModule Creating instance")
            returnVal = super(importModule, cls).__new__(cls)
            returnVal.hasModuleBeenLoaded = False
        returnVal.__callStack__ = __callStack__
        returnVal.moduleName = moduleName
        returnVal.TYPE_CHECKING = typing.TYPE_CHECKING
        __callStack__[0].f_locals[moduleName] = returnVal
        # inspect.stack()[1][0].f_locals[moduleName] = returnVal
        returnVal.moduleNameOrImportExpression = moduleNameOrImportExpression
        returnVal.__finishedInitialization__ = True
        return returnVal
    
    def __init__(self, moduleName: str, lazyLoad = True, __callStack__=None) -> None: # Necessary to get auto completion to figure out what the parameters should be
        pass
            
    def loadModule(self):
        if self.__finishedInitialization__ and not self.hasModuleBeenLoaded:
            # print("Loading module")
            # print(f"self.hasModuleBeenLoaded {self.hasModuleBeenLoaded}")
            self = importModule(self.moduleNameOrImportExpression, False, __callStack__=self.__callStack__)
            # print(f"self.__finishedInitialization__ {self.__finishedInitialization__} self.hasModuleBeenLoaded {self.hasModuleBeenLoaded}\n\n{dir(self)}\n\n")
            self.hasModuleBeenLoaded = True
        return self
    

    def __getattr__(self, item):
        # print("getattr ", item)
        returnVal = self.loadModule()
        returnVal = eval(f"returnVal.{item}")
        return returnVal

    def __dir__(self):
        # print("dir")
        return dir(self.loadModule())
    
if False: # Demo
    if importModule("math").TYPE_CHECKING:
        import math  # This line enables intellisense, at runtime, this never actually executes
    if importModule("from . import testModule").TYPE_CHECKING:
        from . import testModule # This line enables intellisense, at runtime, this never actually executes
    import time
    time.sleep(1.5)
    print(testModule.testVar) # This is when testModule gets imported
    time.sleep(1.5)
    print(math.acos(0.4))     # This is when math gets imported
    