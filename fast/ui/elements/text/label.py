from typing import Optional
from nicegui import ui
from nicegui.client import Client
from nicegui.element import Element
import typing
from ... import serveFiles

class Label(Element):
    def __init__(self) -> None:
        super().__init__('p')
        self.style(add="color: var(--neutral_Opposite);")