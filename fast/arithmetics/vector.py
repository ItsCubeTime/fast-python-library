import math
import numpy as np
class vector:
    "Contains a series of tools for vector/point manipulation. Do not instanciate"
    def getAngleBetweenPoints2D(vector1: list, vector2: list, radiansInsteadOfDegrees=False):
        "Returns degrees by default"
        try:
            vector1[0]
        except:
            vector1 = [vector1.x, vector1.y]
        try:
            vector2[0]
        except:
            vector2 = [vector2.x, vector2.y]
        returnValueRadians = math.atan2(-(vector2[1]-vector1[1]), vector2[0]-vector1[0])*-1
        if radiansInsteadOfDegrees:
            return returnValueRadians
        else:
            return math.degrees(returnValueRadians)
        
    def normalize(vector: list):
        return vector/np.linalg.norm(vector)