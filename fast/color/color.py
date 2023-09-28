def hexToRgb(hexAsStr: str, formatToStr=False) -> list[int]|str:
    "Takes something like: #ffffff and outputs a list [255,255,255]. # in input is optional. formatToStr argument makes us return a CSS compatible str instead, like: rgb(0,0,0)"
    returnVal = tuple(int(hexAsStr.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    return f'rgb({returnVal[0]}, {returnVal[1]}, {returnVal[2]})' if formatToStr else returnVal