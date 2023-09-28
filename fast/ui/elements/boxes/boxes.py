from typing import Optional
from nicegui import ui
from nicegui.client import Client
from nicegui.element import Element
import typing
from ... import serveFiles

serveFiles.linkThisFilesCss()

class Card(Element):
    def __init__(self) -> None:
        super().__init__('div')
        self.classes(add="fastCard")