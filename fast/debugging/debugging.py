
from .. import pkgsAndModules
pkgsAndModules.installPackageIfCorrespondingModuleIsUndefined("pygments", "pygments")
from pygments.style import Style
from pygments.token import (Comment, Error, Generic, Keyword, Literal, Name,
                            Number, Operator, Punctuation, String)
from pygments.token import (Comment, Generic, Keyword, Name, Number, Operator,
                            String, Token)
import inspect
import os
import sys
import textwrap
import traceback

from .. import data

# logLocation = dataLocation + 'logs/'
# "Defaults to %APPDATA%/fast/logs"

useTerminalColors = True
logFilePath = None


class MSG_TYPES:
    WARN = "WARN"
    ERROR = "ERROR"
    MSG = "MSG"


class LOG_TYPES:
    "Should always be stored in a list to enable support for multiple logging devices. You can override the values of this class to modify the behaviour"
    CONSOLE = "CONSOLE"
    DISK = "DISK"
    POPUP = "POPUP"
    "Spawns a popup window"
    DEFAULT = [CONSOLE]


class TERMINAL_COLORS:
    BLACK = '\u001b[30m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'
    MAGENTA = '\033[35m'
    YELLOW = '\033[33m'
    GRAY = '\033[90m'
    PYTHON = "PYTHON"
    # TEST = '\033[97m'
    LIGHTBLUE = '\033[38;5;153m'
    "Note; This color uses RGB colors - which may have less support (though, honestly Im not so sure if this is a problem in the 21st century)"

    ENDCOLOR = '\033[0m'


def colorString(string: str, color: TERMINAL_COLORS = ""):
    if useTerminalColors:
        if TERMINAL_COLORS.PYTHON == color:
            import pygments
            from pygments import formatters, lexers
            return pygments.highlight(string, lexers.PythonLexer(), formatters.Terminal256Formatter(style=VSCodeStyle))
        else:
            return color + str(string) + (TERMINAL_COLORS.ENDCOLOR if color != "" else "")
    else:
        return string


def print(
        string: str | Exception, color: TERMINAL_COLORS = "", stack: list[inspect.FrameInfo] = None,
        logTypes: list[LOG_TYPES] = LOG_TYPES.DEFAULT):
    "@note TODO: Create a write to log file feature for this method."
#     string = '''print("Cookie") if True else None
# class Test(): # wa
#     print("yo")'''
    if stack == None:
        stack = inspect.stack()
    isException = isinstance(string, Exception)
    if isException:
        msgTypeUncolored = "⚠️  ERROR "
        msgType = colorString(msgTypeUncolored, TERMINAL_COLORS.RED)
        if color == "":
            color = TERMINAL_COLORS.PYTHON
    else:
        msgTypeUncolored = "💭  MSG "
        msgType = colorString(msgTypeUncolored, TERMINAL_COLORS.LIGHTBLUE)
    baseIndentationLevelAsStr = "".join([" " for char in msgTypeUncolored])[1:]

    def formatFrameInfo(frameInfo: inspect.FrameInfo, string) -> str:
        fileName = frameInfo.filename
        lineNo = frameInfo.lineno
        func = frameInfo.function if frameInfo.function != "<module>" else "main"
        stackInfo = f"{func}() > {fileName}:{lineNo}:"
        string = str(textwrap.indent(string, "  "))

        minPrefixingSpacesPerLine = 99999999999999999999999
        stringSplit = string.split("\n")
        for subStr in stringSplit:
            i = -1
            while i < subStr.__len__() - 1:
                i += 1
                if subStr[i] != " ":
                    minPrefixingSpacesPerLine = min(minPrefixingSpacesPerLine+1, i+1)
                    break
        string = ""
        for subStr in stringSplit:
            string += "  " + subStr[minPrefixingSpacesPerLine-1:]
        string = colorString(string, color)
        return f"{colorString(stackInfo, TERMINAL_COLORS.GRAY)}\n{colorString(string, color=TERMINAL_COLORS.MAGENTA)}\n"

    if isException:
        exception = string
        string = ""
        i = -1
        for frameInfo in stack:
            i += 1
            if i == 0:
                continue
            print(f"code_context")
            
            
            def get_code_context(frame_info):
                frame = frame_info.frame
                frame_info = inspect.getframeinfo(frame)
                code_context = frame_info.code_context
                return code_context
            try:
                codeContext = get_code_context(frameInfo)[0]
            except:
                codeContext = "Code context inaccessible"
            string = formatFrameInfo(frameInfo, codeContext) + string
            # string = formatFrameInfo(frameInfo, frameInfo.code_context[0]) + string
        # @note Needs verificaiton if it does what its supposed to
        string += colorString(f"{traceback.format_exc(chain=False)}", TERMINAL_COLORS.GRAY)

        # string = colorString(string, TERMINAL_COLORS.GRAY)
    else:
        string = formatFrameInfo(stack[0], string)

    string = str(textwrap.indent(string, baseIndentationLevelAsStr)).lstrip(" ")
    finalStr = f"{msgType}{string}"
    if logTypes.__contains__(LOG_TYPES.CONSOLE):
        sys.stdout.write(finalStr)
    if logTypes.__contains__(LOG_TYPES.DISK and logFilePath != None):
        pass
    # sys.stdout.flush()


class VSCodeStyle(Style):

    background_color = '#282a36'
    styles = {
        Token:              'noinherit #9CDCFE',  # Supposed to be #D4D4D4. #bebebe
        Name.Function:      'noinherit #DCDCAA',
        Name.Label:         'noinherit #f1fa8c',
        Generic.Heading:    '          #f8f8f2 bold',
        Name.Attribute:     'noinherit #9CDCFE',
        # Operator.Word:      'noinherit #bebebe',
        Name.Entity:        'noinherit #f8f8f2',
        Generic.Emph:       'underline',
        Generic.Subheading: '          #f8f8f2 bold',
        Comment:            'noinherit #6A9955',
        Name.Variable:      'noinherit #9CDCFE',
        String:             'noinherit #CE9178',
        # Keyword:            'noinherit #C586B6', # Supposed to be #1f5dc2 for classes
        Keyword:            'noinherit #1f5dc2',  # Supposed to be #1f5dc2 for classes
        Generic.Deleted:    'noinherit #8b080b',
        # Keyword.Type:       'noinherit #4EC9B0',
        Name.Constant:      'noinherit #4FC1FF',
        Comment.Preproc:    'noinherit #ff79c6',
        Generic.Output:     'noinherit #525563',
        Name.Tag:           'noinherit #ff79c6',
        # Number.Float:       'noinherit #B5CEA8',
        Generic.Inserted:   'noinherit bg:#468410 bold',
        # Number:             'noinherit #bd93f9',
        Generic.Traceback:  'noinherit #f8f8f0',
        String.Escape:             '#D7BA5F',      # class: 'se'
        String.Affix:       'noinherit #1E50B3',
        String.Symbol:       'noinherit #1E50B3',
        # String.Backtick:  'noinherit #1E50B3',
        # String.Char:      'noinherit #1E50B3',
        # String.Delimiter: 'noinherit #1E50B3',
        # String.Doc:       'noinherit #1E50B3',
        # String.Double:    'noinherit #1E50B3',
        # String.Escape:    'noinherit #1E50B3',
        # String.Heredoc:   'noinherit #1E50B3',
        String.Interpol:  'noinherit #1E50B3',
        # String.Other:     'noinherit #1E50B3',
        # String.Regex:     'noinherit #1E50B3',
        # String.Single:    'noinherit #1E50B3',

        Number:                        'noinherit #aec980',  # abc57d
        Number.Bin:                    'noinherit #aec980',
        Number.Float:                  'noinherit #aec980',
        Number.Hex:                    'noinherit #aec980',
        Number.Integer:                'noinherit #aec980',
        Number.Integer.Long:           'noinherit #aec980',
        Number.Oct:                    'noinherit #aec980',
        Operator:                    'noinherit      #D4D4D4',
        Operator.Word:                    'noinherit #0000f3',
        Punctuation:                   'noinherit #D4D4D4',  # a8c27b
        Punctuation.Marker:            'noinherit #D4D4D4',


        #     Generic:                   'noinherit #09ff00',
        # Generic.Deleted:               'noinherit #09ff00',
        # Generic.Emph:                  'noinherit #09ff00',
        # Generic.Error:                 'noinherit #09ff00',
        # Generic.Heading:               'noinherit #09ff00',
        # Generic.Inserted:              'noinherit #09ff00',
        # Generic.Output:                'noinherit #09ff00',
        # Generic.Prompt:                'noinherit #09ff00',
        # Generic.Strong:                'noinherit #09ff00',
        # Generic.Subheading:            'noinherit #09ff00',
        # Generic.Traceback:             'noinherit #09ff00',

        # Literal:                       'noinherit #09ff00',
        # Name.Variable.Global:          'noinherit #09ff00',
        Name.Variable.Class:           'noinherit #9CDCFE',
        Name.Variable:             'noinherit #9CDCFE',
        Name.Variable.Global:      'noinherit #9CDCFE',
        Name.Variable.Instance:    'noinherit #9CDCFE',
        Name.Property:             'noinherit #9CDCFE',

        # Keyword:          'noinherit #0000f3',
        # Keyword.Namespace:             'noinherit #ff0000',
        # Keyword.Constant:          'noinherit #0000f3',
        # Keyword.Declaration:       'noinherit #ff0000',
        # Keyword.Namespace:         'noinherit #ff0000',
        # Keyword.Pseudo:            'noinherit #ff0000',
        # Keyword.Reserved:          'noinherit #ff0000',
        # Keyword.Type:              'noinherit #ff0000',

        # Name:                          'noinherit #ff0000',
        # Name.Attribute:                'noinherit #ff0000',
        # Name.Builtin:                  'noinherit #ff0000',
        # Name.Builtin.Pseudo:           'noinherit #ff0000',
        Name.Class:                    'noinherit #4bc49f',
        Name.Constant:                 'noinherit #ff0000',
        Name.Decorator:                'noinherit #DCDCAA',
        Name.Entity:                   'noinherit #ff0000',
        Name.Exception:                'noinherit #4bc49f',
        # Name.Function:                 'noinherit #ff0000',
        # Name.Function.Magic:           'noinherit #ff0000',
        # Name.Property:                 'noinherit #ff0000',
        # Name.Label:                    'noinherit #ff0000',
        # Name.Namespace:                'noinherit #ff0000',
        # Name.Other:                    'noinherit #ff0000',
        # Name.Tag:                      'noinherit #ff0000',
        # Name.Variable:                 'noinherit #ff0000',
        # Name.Variable.Class:           'noinherit #ff0000',
        # Name.Variable.Global:          'noinherit #ff0000',
        # Name.Variable.Instance:        'noinherit #ff0000',
        # Name.Variable.Magic:           'noinherit #ff0000',
    }
