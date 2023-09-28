import random
import typing
def getRandomValueInCollection(collection: typing.Iterable):
    return collection[(random.random()*len(collection)).__floor__()]
import uuid

def getRandomUniqueIdentifier(length = 32):
    """Can be used to generate secure passwords, or keys that are practically guaranteed to be unique. Uses only alphanumeric characters, that is a-z (all letters lowercase) & 0-9
    
    Go to function definition for an example that demonstrates how large the risk of conflict is depending on length"""
    returnVal = ""
    while returnVal.__len__() < length:
        returnVal += str(uuid.uuid4()).replace('-', '')
    return returnVal[:length]

#@note The  following loop demonstrates that the risk of getting the same UUID twice if you were to run this loop for an entire day
#on an i9-12900K processor:
# 
# 0.000000000000000000000000000000000000038479 if length = 32
# 0.000000000000203981936776429149052094656491 if length = 16
# 0.475121139604031128556016483344137668609619 if length = 8
# Basically you would have to be really unfortunate
# i = 0
# rand = getRandomUniqueIdentifier()
# sec = 5
# len = 16
# import time
# lastTime = 0
# startTime = time.time()
# while True: 
#     i += 1
#     currentTime = time.time()
#     if lastTime + sec < currentTime:
#         lastTime = currentTime
#         perDay = i/(currentTime-startTime)*60*60*24 if currentTime-startTime > 0 else 0
#         print(f"""i {i}
# i/(currentTime-startTime)*60*60*24: {perDay }
# perDay/pow(35,len) {'{0:.42f}'.format(perDay/pow(35,len))} # prints about 0.000000000000000000000000000000000000038479
# rand {rand}
# rand len {rand.__len__()}
# pow(35,len) {pow(35,len)}""") # @note there are 26 letters in the alphabet + 9 numbers
#         print(rand.__len__())
#         print(pow(35, len))