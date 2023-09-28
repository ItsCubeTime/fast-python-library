# Used internally by console.py 
try:
    import fast
    print(fast.string.putTextInBox(f"""\
                            elevatedPrivileges executor                        """) + "\n" + fast.string.putTextInBox('''\
For details of this program, see "fast.console.Console()", "runCmdViaSocket.py"'''))
    import json
    import sys
    from fast.console.console import _RunCmdMsg, _RunCmdResponse
    debug = sys.argv.__len__() < 3
    import os
    try:
        os.mkdir("iExist123")
    except:
        pass
    if debug:
        port: int = 0
        key:str = "8fj48gur7fidk4720g7fhrk4jg75hgia" # Used to filter out messages to prevent other programs from sending cmds. Will be appended in the beginning of every
        # message sent between processes (and truncated once identified).
        consoleType: fast.console.EnumConsoleType = fast.console.EnumConsoleType.OSDefault
    else:
        port: int = int(sys.argv[1])
        key:str = sys.argv[2] # Used to filter out messages to prevent other programs from sending cmds. Will be appended in the beginning of every
        # message sent between processes (and truncated once identified).
        consoleType: fast.console.EnumConsoleType = sys.argv[3]
    # elevatedPrivileges = bool(sys.argv[4]) == 'True'
    c = fast.console.Console(consoleType=consoleType, elevatedPrivileges=False) #If this process is elevated, subprocess.Popen() should also be
    def receive(self: fast.networking.FastSocket, message: str):
        try:
            if message == "terminate":
                c.terminate()
                fast.asyncronous.killProcess()
                return
            # print(f"messageType: {type(message)}")
            
            runCmdMsg: _RunCmdMsg = fast.string.deserialize(message)
            if isinstance(runCmdMsg, _RunCmdMsg):
                # runCmdMsg.waitForResponse = True
                if runCmdMsg.key == key:
                    returnVal = c.runCmd(runCmdMsg.content, runCmdMsg.waitForResponse)
                    if runCmdMsg.waitForResponse:
                        fs.send(fast.string.serialize(_RunCmdResponse(key, returnVal)))
                        print(runCmdMsg.content + '\n' + returnVal)
                        return returnVal
                    print(runCmdMsg.content)
        except Exception as exc:
            import traceback
            # print(traceback.format_exc())
        
        # if message.startswith(key):
        #     message = message[key.__len__():]
        #     waitForExecution = message[0]=='1'
        #     c.runCmd(message[1:], waitForExecution)
        #     if waitForExecution:
            
    fs = fast.networking.FastSocket(port=port, receive=receive, timeoutCb=lambda: fast.processes.killProcess())
    if debug:
        pass
        # receive(fs,"terminate") # Works
        foo = "foo"
        fooSer:bytes = fast.string.serialize("foo")
        # fooSer
        fooSerEnc = fast.networking.urlEncode(fooSer)
        fooSerDeEnc = fast.networking.urlDecode(fooSerEnc)
        fooSerDeEncDeSer = fast.string.deserialize(fooSerDeEnc)
        # print(f"""foo serialized:       {fooSer}""")
        # print(f"""foo serialized enc:   {fooSerEnc}""")
        # print(f"""foo fooSerDeEnc:      {fooSerDeEnc}""")
        # print(f"""foo fooSerDeEncDeSer: {fooSerDeEncDeSer}""")
        def receivedResponse(self: fast.networking.FastSocket, message: str):
            message = fast.string.deserialize(message)
    #         print(f"""receivedResponse ->
    # \n#####################################################################\n 
    # {message.content}
    # \n#####################################################################\n 
    # receivedResponse type: {type(message)}

    # """)

        fs2 = fast.networking.FastSocket(port=fs.port, receive=receivedResponse)
        returnVal = receive(fs,fast.string.serialize( _RunCmdMsg(key, "mkdir lemonadeMachine & echo hi", True)))

        # print(f"returned -> {returnVal} <-")
except:
    import traceback
    logFile = fast.files.File(fast.files.File(__file__).getParentFolder() + "runCmdViaSocket.log")
    logFile.setContent(traceback.format_exc())