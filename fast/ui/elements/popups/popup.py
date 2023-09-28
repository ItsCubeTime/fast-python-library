from __future__ import annotations
from nicegui import ui
from nicegui.element import Element
# from nicegui.binding import BindableProperty, 
import typing
from ... import serveFiles
from ... import input
class Popup(Element):
    def __init__(self, onShow: typing.Callable=lambda:None, onHide: typing.Callable=lambda:None) -> None:
        self.onShow = onShow
        self.onHide = onHide
        super().__init__('div')
        self.classes(add="popup")
        self.style(add="position: fixed; z-index: 100000; top: 0; left: var(--cursor);")

        self.bg = ui.element('div').style(add="background-color: rgba(0,0,0,0.0); position: fixed; top:0;left:0;right:0;bottom:0; z-index: 99999;")
        
        self.bg.on("click", self.delete)
        self.parent_slot.children.append(self.bg)
        
    def delete(self):
        self.parent_slot.parent.remove(self.bg)
        self.parent_slot.parent.remove(self)
        super().delete()
    # def __enter__(self) -> Popup:
    #     self.default_slot.__enter__()
    #     return self
        
        # self.hide()
    def show(self):
        input.getMousePos()
        self.visible = True
        print("show")
        # self.style(remove="visibility: hidden;")
        # self._props["onShow"]()
        self.onShow()
    def hide(self):
        self.visible = False
        print("hide")
        # self.style(add="visibility: hidden;")
        self.onHide()
        pass
    def toggle(self):
        self.visible = not self.visible
        # print("toggle")

        # self._props["onHide"]()
#class Popup(Element):
#    showing = False
#    def __init__(self, onShow: typing.Callable, onHide: typing.Callable) -> None:
#        super().__init__('q-popup-proxy')
#        self._props["onShow"] = onShow
#        # self._props["onHide"] = onHide
#        self._props["onHide"] = onHide
#        self.classes(add="popup")
#        # self.showing = BindableProperty()
#        
#    def show(self):
#        print("show")
#        self._props["onShow"]()
#    def hide(self):
#        self._props["onHide"]()
serveFiles.linkThisFilesCss()
ui.add_head_html('''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Asap:wght@500&family=Goldman:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<link href="
https://cdn.jsdelivr.net/npm/dejavu-sans@1.0.0/css/dejavu-sans.min.css
" rel="stylesheet">''')
class PopupButton(Element):
    def __init__(self, text: str, cb: typing.Callable=lambda:print("PopupButton!")):
        super().__init__('div')
        self.on("click", cb)
        with self:
            self.text = ui.label(text)
            self.text._classes.clear()
            self.text.classes(add="popupText")
            self.text.update()
            
        # with self:
        #     ui.add_body_html(f'<p classes="popupText">{text}</p>')
        self.classes(add="popupButton")