from nicegui import ui
from nicegui.element import Element
from ... import serveFiles

serveFiles.linkThisFilesCss()

class gridResize(Element):
    def __init__(self) -> None:
        super().__init__('div')
        self.classes(add='grid-resize')
class gridResizeElement(Element):
    def __init__(self) -> None:
        super().__init__('div')
        self.classes(add='grid-resize-element')