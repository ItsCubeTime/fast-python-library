import time
import typing
from .. import asyncronous
from .. import debugging
import sys

class Event():
    def __init__(self, functionToExecute: typing.Callable) -> None:
        self.function = functionToExecute
        self.lastExecutionTime: float = 0
        self.isRunning: float = False

class CallEveryXSecondsEvent(Event):
    def __init__(self, functionToExecute: typing.Callable, timeBetweenExecutions: float = 1) -> None:
        self.function = functionToExecute
        self.timeBetweenExecutions = timeBetweenExecutions 

callEveryXSeconds: list[CallEveryXSecondsEvent] = []
"Simply append any methods you want to automatically execute."

class EventManager:
    maxSleepTime = 1/20 # This is the minimum time in seconds that we sleep between event condition checks. Making this the theoretical max amount of unexpected latency
    # beyond what could be caused by the interpreter thread being too busy.
    def __init__(self) -> None:
        self.executeEventsHandler()
    def executeEventsHandler(self):

        asyncronous.runAsync(self.executeEvents)
        if callEveryXSeconds.__len__() == 0:
            time.sleep(self.maxSleepTime)
        else:
            time.sleep(min(self.maxSleepTime, self.smallestTimeBetweenExecutions) )
        asyncronous.runAsync(self.executeEventsHandler)

    def executeEvents(self):
        self.smallestTimeBetweenExecutions = sys.float_info.max
        for callEveryXSecondsEvent in callEveryXSeconds:
            currentTime = time.time()
            if currentTime - callEveryXSecondsEvent.timeBetweenExecutions > callEveryXSecondsEvent.lastExecutionTime:
                pass
            print("yes1")
            if currentTime - callEveryXSecondsEvent.timeBetweenExecutions > callEveryXSecondsEvent.lastExecutionTime:
                print("yes2")
                if not callEveryXSecondsEvent.isRunning:
                    print("yes3")
                    callEveryXSecondsEvent.lastExecutionTime = currentTime
                    
                    if self.smallestTimeBetweenExecutions > callEveryXSecondsEvent.timeBetweenExecutions:
                        self.smallestTimeBetweenExecutions = callEveryXSecondsEvent.timeBetweenExecutions
                    
                    def callFunction():
                        callEveryXSecondsEvent.isRunning  = True
                        callEveryXSecondsEvent.function()
                        callEveryXSecondsEvent.isRunning  = False
                    asyncronous.runAsync(callFunction)
        

                    

    
eventManager = EventManager() # Init



