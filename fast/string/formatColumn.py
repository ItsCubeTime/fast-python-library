import typing
import functools
class Variables:
    def __init__(self, name:str) -> None:
        self.name = name
        self.values = []
        self.maxLength = name.__len__()
        self.sum = -1.
    def addValue(self, val):
        self.values.append(val)
        if val.__class__ in [int, float]:
            self.sum=max(0,self.sum)+val
        self.maxLength = max(self.maxLength, numericToStr(val).__len__(), numericToStr(self.sum).__len__())
    def __eq__(self, __value: object) -> bool:
        return self.name == __value
    
def numericToStr(val, decimals=2):
    try:
        floatVal = float(val)
        if int(float(val))==float(val):
            return str(int(val))
        else:
            returnVal = f'%.{int(decimals)}f' % float(val)
            # print(f"returning {returnVal}")
            return returnVal
    except:
        pass
    return str(val)
def formatListOfClassesToColumnStr(listOfObjects: list, includeVariableNamesAtTop=True, includeSummation=True, includeAverage=True, spacesBetweenColumns=5, sort=False, sortOperator:typing.Callable=None) -> str:
    """
    Creates a string that aligns data to rows & columns by inserting spaces as needed
    Example usecase: 
    class Food:
        def __init__(self,name: str,price: int,daysItWillLast) -> None:
            self.name = name
            self.price=price
            self.daysItWillLast = daysItWillLast
            self.pricePerDay = price/daysItWillLast
        def __gt__(self, other):
            return self.pricePerDay > other.pricePerDay


    foods=[
        Food("bulgur",18,3),
        Food("mjölk",21,3 ),
        Food("stekmargarin",22,2),
        Food("grönsaker frysta",25,3),
        Food("toalettpapper",23,8),
        Food("hushållspapper",24,12),
        Food("pasta",12,3),
        Food("morötter",18,5),
        Food("energibröd",42,3),
        Food("ägg",41,15/3),
    ]



    import fast

    foodsAsStr = fast.string.formatListOfClassesToColumnStr(foods, sortOperator=lambda a, b: a.pricePerDay > b.pricePerDay)


    Output:
    name                 price     daysItWillLast     pricePerDay
    bulgur               18        3                  6
    mjölk                21        3                  7
    stekmargarin         22        2                  11
    grönsaker frysta     25        3                  8.33
    toalettpapper        23        8                  2.88
    hushållspapper       24        12                 2
    pasta                12        3                  4
    morötter             18        5                  3.60
    energibröd           42        3                  14
    ägg                  41        5                  8.20

    sum                  246       47                 67.01
    average              24.60     4.70               6.70
    """
    
    if sortOperator==None:
        if hasattr(listOfObjects,'__gt__'):
            sortOperator=listOfObjects.__gt__
    else:
        sort=True
    if sort:
        listOfObjects.sort(key=functools.cmp_to_key(sortOperator))
    returnStr = ""
    maxValueLength = 0
    variableNames: list[Variables] = []

    for food in listOfObjects:
        for var in food.__dir__():
            if var[:2] != "__":
                if not var in variableNames:
                    # print(f"{var} not in varnames")
                    variableNames.append(Variables(var))
                varVal = variableNames[variableNames.index(var)]
                varVal.addValue(food.__dict__[var])
                maxValueLength = max(maxValueLength, varVal.values.__len__())

    variableNamesAtTop = ""
    for var in variableNames:
        variableNamesAtTop += var.name + (var.maxLength - var.name.__len__()+spacesBetweenColumns) * ' '
    if includeVariableNamesAtTop:
        returnStr += variableNamesAtTop
    lineLength = returnStr.__len__()
    # returnStr += "\n" + ' '*lineLength
    i = -1
    while i < maxValueLength-1:
        i += 1
        returnStr +="\n"
        for var in variableNames:
            try:
                varValAsStr = numericToStr(var.values[i])
                returnStr += varValAsStr + (var.maxLength - varValAsStr.__len__()+spacesBetweenColumns) * ' '
            except:
                pass

    returnStr += "\n"
    returnStr += ' '*lineLength + "\n"
    if includeSummation:
        i = -1
        for var in variableNames:
            i += 1
            sumAsStr = numericToStr(var.sum) if i != 0 else "sum"
            returnStr += sumAsStr + (var.maxLength - sumAsStr.__len__()+spacesBetweenColumns) * ' '
    if includeAverage:
        i = -1
        returnStr += "\n"
        for var in variableNames:
            i += 1
            sumAsStr = numericToStr(var.sum/var.values.__len__()) if i != 0 else "average"
            returnStr += sumAsStr + (var.maxLength - sumAsStr.__len__()+spacesBetweenColumns) * ' '
    return returnStr