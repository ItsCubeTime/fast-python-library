from typing import Any
from pydoc import locate
from .. import pkgsAndModules
import pickle

# originally adapted from fast/db/db.py
def deserialize(value: bytes) -> Any:
    "Deserializes data serialized with the serialize() function"
    if isinstance(value, str):
        value = bytes(value, 'utf-8')
    if str(value[0]) == '40': # Assume that this means the data is compressed.
                                        # 40 in the ascii table is '('
        import zstandard as zstd
        value = zstd.decompress(value)
    if not b'\n' in value:
        return None
    type, value = value.split(b'\n', 1)
    type = type.replace(b'\r', b'')
    if type == b'pic':
        return pickle.loads(value)
    elif type == b'dil':
        pkgsAndModules.installPackageIfCorrespondingModuleIsUndefined("dill","dill")
        import dill
        return dill.loads(value)
    returnVal = locate(type.decode())(value)
    return returnVal[2:-1] if type == b'str' else returnVal

def serialize(object: Any, useCompression=True, compressAboveFinalDataLengthOf = 200) -> bytes:
    """Takes a python object of any type and attempts to turn it into a string :) 
    Smaller values remains readable & uncompressed where possible while larger data gets compressed.
    
    Based on str().encode(), pickle & dill. Uses str().enocode() where suitable to keep the data readable, pickle as secondary choice (as its a lot faster than dill) and dill where all other fails. 
    
    Remains type aware by making the first line represent the data type"""
    originalValue = object
    alwaysCompress = False
    if type(object)  in [str, int, float, bytes]:
        varType = bytes(type(object).__name__, 'utf-8')
        object = str(object).encode()
        # decode = False
    else:
        # decode = True
        # Pickle
        alwaysCompress = True
        try:
            object = pickle.dumps(object)
            varType = b'pic' # short for pickle, everything to save those bytes :P
        except:
            pkgsAndModules.installPackageIfCorrespondingModuleIsUndefined("dill","dill")
            import dill
            object = dill.dumps(object)
            varType = b'dil' # short for dill, everything to save those bytes :P
    # import zstd
    finalBytes = varType + b'\n' + object
    if useCompression and (finalBytes.__len__() > compressAboveFinalDataLengthOf or alwaysCompress): # If compression is enabled, compress anything with a charcount longer than 200 or if using dill or pickle
        import zstandard as zstd
        finalBytes = zstd.compress(finalBytes, 2)
    return finalBytes