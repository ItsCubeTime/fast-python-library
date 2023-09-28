import subprocess
import os
import sys
class EnumConsoleType:
    OSDefault= "OSDefault"
    "On Windows, this is CMD prompt, on Linux, Bash"
    PowerShell ="PowerShell"
    "Only available on Windows"
    Python = "Python"
    "Python console is not yet functional. Will fire up a new Python process in interactive mode & let you give it Python cmds just like running it in the terminal"
class _RunCmdMsg:
    "Used internally to communicate with elevated process"
    def __init__(self,key: str,content:str, waitForResponse: bool) -> None:
        self.waitForResponse = waitForResponse
        self.key = key
        self.content = content
class _RunCmdResponse:
    "Used internally to communicate with elevated process"
    def __init__(self,key: str,content:str) -> None:
        self.key = key
        self.content = content
class Console():
    """Execute console cmds & get stdout + return code. Has a bug where if you dont store a reference to the Console() instance and call runCmd without waitForResponse, the terminal appears to shut down before it has enough time to execute the cmds (not sure what the cause is, but I suspect some kind of garbage collection).
    
    Can also be used to communicate with the console of existing programs, by providing the pid parameter.
    
    Aims to be crossplatform, however currently only offers Windows support"""
    def _receive(*args):
        self, ignore, msg = args # For some odd reason we receive an extra argument. If receive is declared as such:
        # receive(self, ignore, msg) we end up receiving 4 arguments (always 1 too much). Hence I resolved to argument unpacking

        from .. import networking
        self: networking.FastSocket
        try:
            from .. import string
            # print(f"console.__init__.receive: ->{msg}\n<-")
            # print(f"console.__init__.receive type: ->{type(msg)}\n<-")
            msg: _RunCmdResponse = string.deserialize(msg)
            # print(f"console.__init__.receive type deser: ->{type(msg)}\n<-")
            # print(f"received-> {msg.content} \n<-")
            if isinstance(msg, _RunCmdResponse):
                self._response = msg.content
        except:
            import traceback
            # print(traceback.format_exc())
    def __init__(self, consoleType: EnumConsoleType = EnumConsoleType.OSDefault, elevatedPrivileges=False) -> None: #, pid: int=None
        self.elevatedPrivileges = elevatedPrivileges and os.name == 'nt' # @todo create wrapper for getting platform in fast
        self.consoleType = consoleType
        # if pid == None:
        if self.elevatedPrivileges:
            from .. import networking
            import sys
            from .. import files
            from .. import random
            self._fastSocket = networking.FastSocket(receive=self._receive, sendTimeoutPreventionPings=True)
            # args = [sys.executable, 
            runCmdViaSocketPath = str(files.File(__file__).getParentFolder() + "runCmdViaSocket.py")
            self._c = Console(EnumConsoleType.PowerShell)
            self._key = random.getRandomUniqueIdentifier(16)
            startProcessCmd = f'''Start-Process "{sys.executable}" -Verb runAs -ArgumentList "`"{runCmdViaSocketPath}`"", "{self._fastSocket.port}", "{self._key}", "{self.consoleType}"'''
            # print(f"startProcessCmd: {startProcessCmd}")
            self._c.runCmd(startProcessCmd)
            # self._p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            if self.consoleType == EnumConsoleType.PowerShell:
                args = ['powershell.exe', '-Command', r'-']
            elif self.consoleType == EnumConsoleType.Python:
                import sys
                # args = 'python'
                args = [f'{sys.executable}'.replace('\\', '/').replace('//', '/'), '-i']
            else:
                args = ['cmd', 'f']
                # if elevatedPrivileges:
                #     args[0] = __file__.replace('\\','/')[:__file__.replace('\\','/').rfind('/')+1] + 'cmd.exe- elevated'
                #     print(f"yo {args[0]}")
            self._p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
            # self.pid = self._p.pid
            # else:
                # import os.path
                # open(os.path.join('/proc', str(pid), 'fd', '1'), 'a')

    def terminate(self):
        self._p.terminate()
    def runCmd(self, cmd:str, waitForResponse=False):
        if self.elevatedPrivileges:
            import time
            self._response = False
            from .. import string
            
            self._fastSocket.send(string.serialize(_RunCmdMsg(self._key, cmd, waitForResponse)))
            if waitForResponse:
                while False == self._response:
                    # print("Is False")
                    time.sleep(0.05)
                # print(string.putTextInBox("Is not false"))
                return self._response
            return
                    
        else:
            if self.consoleType == EnumConsoleType.PowerShell:
                initWrite = f'echo "BEGIN*_.-_"; {cmd}; echo "FINISHED*_.-_";\r\n'
            elif self.consoleType == EnumConsoleType.Python:
                initWrite = f'print("BEGIN*_.-_")\n{cmd}\nprint("FINISHED*_.-_")\n'
            else:
                initWrite = f'echo BEGIN*_.-_ & {cmd} & echo FINISHED*_.-_\r\n'
            # print("1")
            self._p.stdin.write(initWrite.encode())
            # print("2")
            self._p.stdin.flush()
            # print("3")
            if not waitForResponse:
                return

            returnVal = b""
            line      = b""
            # while True: # @note Uncomment to print everything to console (use for debugging)
            #     # self._p.stdout.flush()
            #     # print("4")
            #     # self._p.stdout.flush()
            #     msg = str(self._p.stdout.readline())
            #     print(msg)
            #     if msg != "b''" and msg != "":
            #         print(msg)
            #     msg = f"stdout.read(): {msg}"
            import time
            while  self._p.stdout.readline() != (b'BEGIN*_.-_\r\n' if self.consoleType == EnumConsoleType.PowerShell else b'BEGIN*_.-_ \r\n'): # @note Cmd prompt adds a space after newlines
                # print("waiting for begin")
                pass
                time.sleep(0.02)
            while True:
                # print("waiting for  finished")
                line = self._p.stdout.readline()
                if line == b'FINISHED*_.-_\r\n':
                    break
                returnVal += line
            return returnVal.decode().strip('\n')