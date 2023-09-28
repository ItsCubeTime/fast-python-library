"A lean nicegui based component library built into fast"
from . import titlebar, files, layout, popups, boxes

class _:
    def __init__(self) -> None:
        from .. import serveFiles
        serveFiles.linkThisFilesCss()
_()