# Fast String Manipulation Library
import math
from .formatColumn import formatListOfClassesToColumnStr, numericToStr
from .serializeToString import serialize, deserialize
def containsLowerCase(string):
    # string: str = ""
    for letter in string:
        if letter.islower():
            # print("aaa")
            return True
    return False

def capitalizeLetterAfterEachSpace(string: str):
    return string.title()

def PascalCaseTo_snake_case(string):
    # string = 


    string: str =  'A' + string.replace(" ", "_") + 'A'
    outputString: str = string.lower()

    firstRun = True
    for index in range(string.__len__()-1, -1, -1):
        letter = string[index]
        if not firstRun and index != 1:
            nextLetter = string[index+1]
            previousLetter = string[index-1]
            if letter.isupper() and (nextLetter.islower() or previousLetter.islower()) and (index != 0) and containsLowerCase(string[:index]):
                if not '_' in [letter, nextLetter, previousLetter] and not '.' in [letter, nextLetter, previousLetter]:
                    outputString = outputString[:index] + "_" + outputString[index:]
                    # print(index)
        else:
            firstRun = False
    
    

    outputString = outputString[1:-1]

    return outputString

def insertSpaceAfterCapital(string):
    string: str = str(string)
    outputString = string
    for index in range(string.__len__()-1, -1, -1):
        letter = string[index]
            
        if letter.isupper():
            if index != 0 and index != string.__len__()-1:
                nextLetter = string[index+1]
                previousLetter = string[index-1]
                if previousLetter.islower() or nextLetter.islower() and containsLowerCase(string[:index]):
                    outputString = outputString[:index] + " " + outputString[index:]

    return outputString

def snake_caseToPascalCase(string: str, maintainPrecedingAndTrailingUnderscores: bool = False):
    i = -1
    hasAnyLetterSoFarBeenAnythingOtherThanUnderscore = False
    returnValue = ""
    def appendLetterToReturnValue(_letter: str):
        nonlocal returnValue
        if _letter != "_":
            returnValue += _letter

    for letter in string:
        i += 1
        previousLetter = string[max(i-1, 0)]
        nextLetter = string[min(i+1, string.__len__()-1)]
        shouldBeUpperCase = False
        if previousLetter == "_":
            shouldBeUpperCase = True
        if i == string.__len__()-1 or not hasAnyLetterSoFarBeenAnythingOtherThanUnderscore or i == 0:
            shouldBeUpperCase = False
        if letter != "_":
            hasAnyLetterSoFarBeenAnythingOtherThanUnderscore = True
        appendLetterToReturnValue(letter.upper() if shouldBeUpperCase else letter)
    if maintainPrecedingAndTrailingUnderscores:
        numberOfPrecedingUnderscores = 0
        numberOfTrailingUnderscores = 0
        hasAnyLetterSoFarBeenAnythingOtherThanUnderscore = False
        for letter in string:
            if letter != "_":
                break
            numberOfPrecedingUnderscores += 1
        for letter in string[::-1]:
            if letter != "_":
                break
            numberOfTrailingUnderscores += 1
        while numberOfPrecedingUnderscores > 0:
            returnValue = "_" + returnValue
            numberOfPrecedingUnderscores -= 1
        while numberOfTrailingUnderscores > 0:
            returnValue += "_"
            numberOfTrailingUnderscores -= 1

    return returnValue

def putTextInBox(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐'] 
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)

def indexOfSubstring(string, substring, occurence=1, revese=False):
    "Eg: indexOfSubstring(http://www.google.com/search), '/', 3) would return the index of the 3rd /."
    start = string.find(substring)
    while start >= 0 and occurence > 1:
        start = string.find(substring, start+1)
        occurence -= 1
    return start


def getVariables(string: str, varBeginSubstr="{", varEndSubstr="}", filterDuplicates = True):
    "Eg getVariables('{lemon}, book, {glasses}') would return [lemon, glasses]" 
    returnVal: list[str] = []
    inString = False
    for char in string:
        if char==varEndSubstr:
            inString = False
        elif inString:
            returnVal[-1] += char
        elif char==varBeginSubstr:
            inString = True
            returnVal.append('')
    if filterDuplicates:
        returnVal = list(dict.fromkeys(returnVal))
    return returnVal


# @note I think "slicing" operations like these are a little too much? Better keep to STD for this.
# class slice:
#     "String slicing operations. Do not instanciate"
#     def removeAfterText(string: str, removeAfterText: str, keepRemoveAfter = True):
#         return string[:string.find(removeAfterText)+(1 if keepRemoveAfter else 0)]
    
#     def removeAfterLastText(string: str, removeAfterText: str, keepRemoveAfter = True):
#         "return string[:string.rfind(removeAfterText)+(1 if keepRemoveAfter else 0)]"
#         return string[:string.rfind(removeAfterText)+(1 if keepRemoveAfter else 0)]
    
# def getBefore(string: str, beforeMe: str, rfind = False, includeSubstring = False):
#     return string[:(string.rfind(beforeMe) if rfind else string.find(beforeMe))+(0 if includeSubstring else 1)]

# currentDirectory = fast.string.slice.removeAfterLastText(__file__, '\\')
# currentDirectory = fast.string.getBefore(__file__, '\\', rfind=True)
# currentDirectory = fast.string.slice(__file__, '', '\\', lastOccurence=True)




# print(snake_caseToPascalCase("____Awesome__SNake_case_text_"))