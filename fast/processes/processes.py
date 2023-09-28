"A nicer interface for handling of processes. Designed with future cross-platform compatability in mind, though atm we only support Windows. Im making use of 'WMIC' under the hood which might be a little slow if youre planning to manage A LOT of processes."
from .. import console
import signal
import os
def killProcess(pid=os.getpid()):
    "Kills the entire Python instance. If using something like the multiprocessing module this will only terminate the current process."

    os.kill(pid, signal.SIGTERM)
    
def getAllProcessesRunningOnDevice() -> int:
    "Returns a list of ProcessIDs. @todo platform support beyond Windows"
    c = console.Console()
    wmicResponse = c.runCmd("wmic process get processid", True)
    return [int(i) for i in wmicResponse.replace('\r', '').replace(' ','').split(('\n')) if not i in ['','0', 'ProcessId']]


# def createProcess(executablePathAndArguments: str,  elevatedPrivileges: bool = False):
#     '''executablePathAndArguments - Eg: python.exe myFile.py''' 
#     c = console.Console(console.EnumConsoleType.PowerShell)
#     c.runCmd(executablePathAndArguments, elevatedPrivileges=elevatedPrivileges)
#     return Process(console=c)

# def runPythonScriptInNewProcess(script: str, isScriptAFilePath=False, elevatedPrivileges: bool = False):



class Process():
    """Designed to be lightweight by only preparing data when its actually needed. All data provided  by this class is derived from the Process PID.
    
    Aims to be suitable for when handling large sets of processes, like instanciating Process() once for every process running on a busy OS without a noticeable delay."""
    def __init__(self, pid=None, console:console.Console=None) -> None:
        self._console = console
        if console == None:
            self.pid = pid
        else:
            self.pid = self._console._p.pid
    @property
    def executablePath(self):
        if not hasattr(self, '_executablePath'):
            self._executablePath = console.Console().runCmd(f'wmic process {self.pid} get ExecutablePath', True).split('\n')[1].replace('\\', '/').strip()
        return self._executablePath
    
    @property
    def console(self) -> console.Console | None:
        """Only available on Process()es created with a console.Console object fed into the constructor. 

        The reason for this is that on Windows it appears to not be quite possible to get stdin/stdout of external processes that you don't control yourself.
        On Linux, stdin/out can be accessed via the OS file system:
        
        with open(f'/proc/{pid}/fd/1', 'a') as stdin:
            stdin.write('Hello there\n')
            
        But since I cant find anything equivalent on Windows atm, I won't be implementing this functionality until I find a way of doing so. 
        Any code contributions here would be highly appreciated (a partial & situation based solution would be better than no solution)."""
        return self._console


    def _getIcon(self, size):
        from .winicon import extract_icon, IconSize, win32_icon_to_image
        import sys
        size = IconSize.SMALL if size == "small" else IconSize.LARGE
        # Extract the icons from the Python interpreter.
        # yo = str(self.executablePath)
        # raw = 'F:/Olliver/Art and development/Hiding Software/dist/foobar.exe'
        # print(f"yo: {yo}\nraw {raw}\nyo: {yo.encode()}\nraw {raw.encode()}\nequ {yo == raw}")
        icon = extract_icon(self.executablePath, size)
        # icon = extract_icon(yo, size)
        # import time
        # time.sleep(60.5)
        # Convert them to PIL/Pillow images.
        return win32_icon_to_image(icon, size)
        
    @property
    def iconSmall(self):
        if not hasattr(self, '_iconSmall'):
            self._iconSmall = self._getIcon('small')
        return self._iconSmall
    @property
    def iconLarge(self):
        if not hasattr(self, '_iconLarge'):
            self._iconLarge = self._getIcon('large')
        return self._iconLarge
    