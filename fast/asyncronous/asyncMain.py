import queue
import asyncio
import inspect
import os
import signal
import threading
import time
import typing

from .. import debugging


def killProcess(pid=os.getpid()):
    "@DEPRECATED - Use killProcess in fast.processes instead. Kills the entire Python instance. If using something like the multiprocessing module this will only terminate the current process."

    os.kill(pid, signal.SIGTERM)


class runAsyncLooping():
    "Runs a method asyncronously in a loop with 2 ways of exiting. self.isRunning being set to false (done externally) or maxLoops being reached"
    isRunning = True

    def __bool__(self):
        return self.isRunning

    def __init__(self, asyncFunc: typing.Callable, intervalSec=1, maxLoops=-1, useThreading=False):
        self.asyncFunc = asyncFunc
        self.intervalSec = intervalSec
        self.maxLoops = maxLoops
        self.useThreading = useThreading

        def runAsyncWrapper():
            nonlocal self
            loops = 0
            while (self.isRunning and (loops < maxLoops or maxLoops < 0)):
                loops += 1
                try:
                    if asyncFunc.__code__.co_argcount == 2:
                        asyncFunc(self)
                    else:
                        asyncFunc()
                except Exception as exc:
                    debugging.print(exc)
                    # print(f"Exception in runAsyncLooping {exc}")
                time.sleep(intervalSec)
            self.isRunning = False
        runAsync(runAsyncWrapper, useThreading=useThreading)


def runAsync(asyncFunc: typing.Callable, *arguments, useThreading=False):
    """Takes a syncronous function and tries to execute it asyncronously. Note that you wont get any return value.

    arguments is a series of parameters that will be passed along to the function you feed as the first argument. arguments takes several arguments

    You could of course also feed in a lambda, like runAsync(lambda: print("hello", "there"))

    # Demo usage
    import time
    def hello(text):
        time.sleep(0.1)
        print(text)
    runAsync(hello, "hi2")
    print("hi") # hi will print first
"""
    def functionWrapper():
        try:
            
            if isinstance(asyncFunc,typing.Coroutine):
                runSync(asyncFunc,dontWait=True)
            else:
                returnVal = asyncFunc()
                if isinstance(returnVal,typing.Coroutine):
                    runSync(returnVal,dontWait=True)
        except Exception as exception:
            debugging.print(exception)

    if useThreading:
        t = threading.Thread(target=functionWrapper, args=())
        t.daemon = True
        t.start()
    else:
        try:
            # eventLoop = asyncio.get_event_loop() # Deprecated apparently? Keeps seeing warnings
            eventLoop = asyncio.get_running_loop()  # Supposedly the replacement 3 10 2023
        except:
            eventLoop = asyncio.new_event_loop()
        eventLoop.run_in_executor(None, functionWrapper, *arguments)


def runSync(coroutine: typing.Coroutine, dontWait = False):
    """Takes a coroutine and runs it syncronously, giving you the returnvalue.

    Current implementation spins up a new thread, creates a new asyncio event loop in there and executes the corotine,
    this should theoretically create a pretty meaningful amount of overhead as we're creating a new thread.

    Hence I will make it a @todo to use a pre spun up thread that gets created first time runSync is called and then
    reused for every call afterwards.

    Before doing the current implementation I spent several hours trying to figure out a way to make runSync work
    without creating a new thread, it simply did not seem to be possible at least with asyncio alone, hence the  current
    threading based implementation. The issue is that if theres an already running event loop in the current thread
    we cannot seem to be able to append new coroutines to it without being in an async scope already - so we need
    a new event loop and run it, which we cannot do without interrupting and stopping the currently running event
    loop (which in its turn we cannot do without likely interrupting other code running in the current thread, likewise we
    cannot seem to be able to just "pause" event loops without consequences).
    
    dontWait wont wait for the execution to finish, so setting it to True effectively makes this more or less runAsync.
    """

    async def threadAsyncCb():
        return await coroutine
    # debugging.print(Exception("Hi"))
    def threadMain(out_queue1):
        loop = asyncio.new_event_loop()  # Because were in a new thread
        # we can be confident theres no already running event loop.
        out_queue1.put(loop.run_until_complete(threadAsyncCb()))
        loop.close()
        # asyncio.run(self._run())    In Python 3.7+

    out_queue1 = queue.Queue()
    t1 = threading.Thread(target=threadMain, args=(out_queue1,))
    t1.start()
    if dontWait:
        return t1
    t1.join()
    return out_queue1.get()

    # returnVal = 1

    # async def _run():
    #     await coroutine

    # def run():
    #     loop = asyncio.new_event_loop()  # loop = asyncio.get_event_loop()
    #     nonlocal returnVal
    #     returnVal = loop.run_until_complete(_run())
    #     loop.close()
    #     # asyncio.run(self._run())    In Python 3.7+

    # t = threading.Thread(target=run, args=())
    # t.daemon = True
    # t.start()
    # t.join()
    # return returnVal

    # if asyncio.get_event_loop().is_running():
    #     # If there is no event loop running, create a new one with a custom event loop policy
    #     loop = asyncio.new_event_loop()
    #     oldLoop = asyncio.get_event_loop()
    #     oldLoop.stop()
    #     asyncio.set_event_loop(loop)
    #     asyncio.set_event_loop(loop)
    #     result = loop.run_until_complete(coroutine)
    #     loop.close()
    #     asyncio.set_event_loop(oldLoop)
    #     oldLoop.run_forever()
    # else:
    #     # If there is an event loop running, use asyncio.run()
    #     result = asyncio.run(coroutine)
    # return result

    # loop = asyncio.get_event_loop()  # Create a new event loop
    # asyncio.set_event_loop(loop)  # Set the new event loop as the current event loop
    # task = loop.create_task(coroutine)  # Create a new task for the coroutine
    # loop.run_in_executor
    # result = loop.run_until_complete(task)  # Use loop.run_until_complete() to run the task and wait for its result
    # loop.close()  # Close the event loop
    # return result
###
    # task = asyncio.create_task(asyncFunc())  # Create a new task for the coroutine
    # result = await asyncio.gather(task)  # Use asyncio.gather() to run the task and wait for its result
    # return result[0]
###
    # return asyncio.run(coroutine)

    # try:
    #     eventLoop = asyncio.get_running_loop()
    # except:
    #     eventLoop = asyncio.new_event_loop()
    # future = eventLoop.(coroutine, eventLoop)

    # future = asyncio.run_coroutine_threadsafe(coroutine, eventLoop)
    # print(f"isRun {eventLoop.is_running()}")
    # eventLoop.run
    # while not future.done():
    #     asyncio.sleep(0.001)
    return future.result(timeout=2)
    # task = eventLoop.create_task(coroutine)
    # eventLoop.run_in_executor(None, coroutine, *arguments)

    # return eventLoop.run_until_complete(task)
    # task.__await__()

    # asyncio.wait([eventLoop.run_in_executor(None, asyncFunc, )])

    # eventLoop.run_until_complete(asyncFunc)

# def runAsync(asyncFunc: typing.Callable, *arguments):
#     """Takes a syncronous function and tries to execute it asyncronously.

#     arguments is a series of parameters that will be passed along to the function you feed as the first argument. arguments takes several arguments

#     You could of course also feed in a lambda, like runAsync(lambda: print("hello", "there"))

#     # Demo usage
#     import time
#     def hello(text):
#         time.sleep(0.1)
#         print(text)
#     runAsync(hello, "hi2")
#     print("hi") # hi will print first
# """
#     def functionWrapper():
#         try:
#             asyncFunc()
#         except Exception as exception:
#             debugging.print(exception)
#     useThreading = False
#     if useThreading:
#         t = threading.Thread(target=functionWrapper, args = ())
#         t.daemon = True
#         t.start()
#     else:
#         try:
#             # eventLoop = asyncio.get_event_loop() # Deprecated apparently? Keeps seeing warnings
#             eventLoop = asyncio.get_running_loop() # Supposedly the replacement 3 10 2023
#         except:
#             eventLoop = asyncio.new_event_loop()

#         eventLoop.run_in_executor(None, functionWrapper, *arguments)


# Demo
# import time
# def hello(text):
#     time.sleep(0.1)
#     print(text)
# runAsync(hello, "hi2")
# print("hi") # hi will print first
