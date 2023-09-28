import types

def reorderListByTypes(values: list, types: list, insertNoneValueForEachTypeInTypesListThatHasNoMatchingValueInValuesList=True, noneValue=None):
    """
Example:
    print(reorderListByTypes(["book", 5, lambda:print("yo")], [types.FunctionType, int, float, float, str, str]))
would print:
    [<function <lambda> at 0x000001B1F86F69E0>, 5, None, None, 'book', 'book']
"""
    returnVal = []
    for ourType in types:
        didWeFindMatch=False
        for value in values:
            if isinstance(value, ourType):
                returnVal.append(value)
                didWeFindMatch=True
                break
        if not didWeFindMatch and insertNoneValueForEachTypeInTypesListThatHasNoMatchingValueInValuesList:
            returnVal.append(noneValue)

    return returnVal
def isCollection(value):
    "Needs further testing, may not work for all collection types"
    return hasattr(value, "__iter__")