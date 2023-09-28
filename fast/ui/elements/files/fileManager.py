from __future__ import annotations
from nicegui import ui
from nicegui.element import Element
from .. import layout

from .... import files
# @todo Perhaps I should store data like what element is active, what folders are collapsed etc in some kind of database file and roll sort of like a key-value
# system stored on disk, in some permanent caching directory? That way we could refresh the entire folder hierarchy without consequences and the software
# could be restarted without the sidebars layout changing!
indentAmount = 10
import nicegui

# class Popup(Element):

#     def __init__(self, source: str = '') -> None:
#         """Image

#         Displays an image.

#         :param source: the source of the image; can be a URL or a base64 string
#         """
#         super().__init__(tag='q-img', source=source)

from nicegui.element import Element
from nicegui.elements.mixins.value_element import ValueElement


class popup(ValueElement):

    def __init__(self, *, value: bool = False) -> None:
        """Menu

        Creates a menu.
        The menu should be placed inside the element where it should be shown.

        :param value: whether the menu is already opened (default: `False`)
        """
        super().__init__(tag='q-popup-proxy', value=value, on_value_change=None)
        self._props['no-parent-event'] = True

    def open(self) -> None:
        self.value = True

    def close(self) -> None:
        self.value = False

# from nicegui import ui
# from nicegui.events import KeyEventArguments



class fileManagerElement():
    "Displays a folder's or file's name"
    def __init__(self, path: files.Path, nestedLevel:float, fileManagerS: fileManagerSidebar) -> None:
        self.row = ui.row()
        self.fileManagerS = fileManagerS
        # self.row.classes(add="fileManagerElement")
        self.row._classes.append("fileManagerElement")

        self.row.style(replace=f"height: 24px; width: 100%; margin:0; padding:0; padding-left: {indentAmount*nestedLevel}px; gap:4px; flex-wrap:nowrap; display: flex;")
        self.pathObj = path
        with self.row:
            if path.isFolder():
                ui.icon("folder")
            elif path.isFile():
                self.pathObj = files.File(self.pathObj)
                if self.pathObj.isImage():
                    ui.icon("image")
                elif self.pathObj.getExtension() == "pdf":
                    ui.icon("picture_as_pdf")
                else:
                    ui.icon("description")
            self.popup = popup()
            with self.popup:
                ui.label("hi")
            
                    
                
            ui.label(path.getName()).style(add="white-space: nowrap;")
        self.row.on("click", lambda: self.setActive(not self.active))
        # self.row.on("click.right", lambda: self.popup.open()) # @todo popup rmb menu
        # self.row.on("right", lambda: print("hi"))
        # self.row.on("keyup.0", lambda: print("0"))
        
        # self.row.on("click:right", lambda e: print(e))
    active = False
    def setActive(self, val):
        if val:
            self.fileManagerS.activeElement = self
                
            for el in self.fileManagerS.fileManagerFolder.getChildElementsRecursive(includeSelf=True):
                el.setActive(False)
            self.row.classes(add="fileManagerElementActive")
            try:
                # print(f"argcount: {self.fileManagerS.updateActiveElementCb.__code__.co_argcount}")
                if self.fileManagerS.updateActiveElementCb.__code__.co_argcount > 0:
                    self.fileManagerS.updateActiveElementCb(self.fileManagerS)
                else:
                    self.fileManagerS.updateActiveElementCb()
            except Exception as exc:
                print(f"setActiveupdateActiveElementCb exc: {exc}")
                from .... import debugging
                debugging.print(Exception('setActiveupdateActiveElementCb exc'))
        else:
            self.row.classes(remove="fileManagerElementActive")
        self.active = val



class fileManagerFolder(fileManagerElement):
    "Encapsulates a fileManagerElement & a fileManagerFolderContent"
    def __init__(self, path: files.Path, nestedLevel: float, fileManagerS: fileManagerSidebar) -> None:
        self.column = ui.column().style(add="width: 100%; gap: 0px; flex-wrap: nowrap;")
        with self.column:
            super().__init__(path, nestedLevel, fileManagerS)
            self.folderObj = files.Folder(path)
            self.fileManagerFolderContent = fileManagerFolderContent(path, nestedLevel, fileManagerS)

    def collapse(self):
        pass # @todo

    # def __iter__(self):
    #     for element in self.fileManagerFolderContent.column.default_slot.children:
    #         yield element

    def getChildElementsRecursive(self, includeSelf = False):
        if includeSelf:
            yield self
        for element in self.fileManagerFolderContent.files:
                yield element
        for element in self.fileManagerFolderContent.folders:
                yield element
                for elementInner in element.getChildElementsRecursive():
                    yield elementInner

class fileManagerFolderContent():
    "A list of fileManagerElements, Should always have a fileManagerElement placed above displaying the folders own name."
    def __init__(self, path: files.Folder, nestedLevel:float, fileManagerS: fileManagerSidebar) -> None:
        self.folderObj = files.Folder(path)
        self.column = ui.column()
        self.column.style(replace=f"width: 100%; flex: 1; gap:0px; overflow: visible; flex-wrap: nowrap;")
        self.nestedLevel = nestedLevel
        self.files : list[fileManagerFile] = []
        self.folders: list[fileManagerFolder] = []
        with self.column:
            for child in self.folderObj.getChildPaths():
                if child.isFolder():
                    self.folders.append(fileManagerFolder(child, self.nestedLevel+1, fileManagerS))
                if child.isFile():
                    self.files.append(fileManagerFile(child, self.nestedLevel+1, fileManagerS))


class fileManagerFile(fileManagerElement):
    "A file, encapsulates fileManagerElement"

_hasLinkedCss = False
from fast.ui import serveFiles
def scrollable_div(width = '100%', height = '100%'):
    return ui.element('div').style(replace='flex-wrap: nowrap; display: flex; justify-content: start; align-items: start; flex-direction: column; flex-grow: 1; margin: 20px; max-width:100%; max-height:100%;')
# C%3A/Users/olliv/AppData/Local/Programs/Python/Python310/lib/site-packages/fast/ui/elements/files/fileManager.css
# C%3A/Users/olliv/AppData/Local/Programs/Python/Python310/lib/site-packages/fast/ui/elements/files/fileManager.css
class fileManagerSidebar():
    activeElement: fileManagerElement = None
    def __init__(self, path: files.Path, updateActiveElementCb=lambda: None) -> None:
        self.updateActiveElementCb = updateActiveElementCb
        global _hasLinkedCss
        if not _hasLinkedCss:
            _hasLinkedCss = True
            cssFile = __file__[:__file__.rfind('.')] + '.css'
            # cssFile = (('C:/Users/olliv/Desktop/scriptingFolderOpsTestDir/I have spaces/'+'fileManagerSidebar.css')) # @note Todo: Fix serveFile with spaces
            # cssFile = ((files.File(__file__).getParentFolder()+'fileManagerSidebar.css'))
            # print(f"FILE: {cssFile}")
            # serveFiles.serveFileInit()
            # try:
            ui.html(f'''<link rel="stylesheet" href="{serveFiles.serveFile(cssFile)}">''')
            # except:
            #     pass
            
            # print(f"servedData: {serveFiles.servedData}")
            # ui.html(f'''<link rel="stylesheet" href="{serveFiles.serveFile((files.Path(__file__).getParentFolder()+'fileManagerSidebar.css'), "foo")}">''')
        # self.content = scrollable_div()
        # with self.content:
            # self.content.style(add='height: 100%; overflow: auto;')
        self.fileManagerFolder = fileManagerFolder(path, nestedLevel=0, fileManagerS=self)
        # self.fileManagerFolder.fileManagerS = self
        self.fileManagerFolder.setActive(self.fileManagerFolder)
        self.fileManagerFolder.column.style(add="width: 100%; height: 100%; overflow: visible;")
            # self.fileManagerFolder.column.style(add='display: flex; flex-direction: column; overflow-y:overlay; overflow-x:clip;max-height: 100%; max-width: 200px;')
            # self.fileManagerFolder.column.style(add='min-height: 100%;')
        # self.content.column.style(add='display: flex; flex-direction: column; overflow:scroll; max-height: 100%; max-width: 100%; overflow-y:overlay; overflow-x:clip;')

from .... import string


import typing
from ... import device
from .... import classes
class Editor(Element):
    """https://github.com/quasarframework/quasar/blob/dev/ui/src/components/editor/QEditor.js
    https://quasar.dev/vue-components/editor/"""
    def __init__(self, defaultText="", placeholderWhenEmpty="Click here to type!", onChange: typing.Callable=lambda:None, onSave: typing.Callable=lambda:None, saveContentToFileOnSave: str = None, *pack, notifyOnSave = False) -> None:
        super().__init__('q-editor')
        self._registeredOnSaveCb = False
        self.notifyOnSave = notifyOnSave
        self.saveContentToFileOnSave = saveContentToFileOnSave
        self.onSave = onSave
        self.onChange = onChange
        self._props['placeholder'] = placeholderWhenEmpty
        # self._props['flat'] = True
        self.setText(defaultText)
        self.on('update:modelValue', self._onChange)

    def setText(self, val):
        self.text =  val
        self._props['modelValue'] = val
        
    async def _onChange(self, newVal):
        import html
        newVal= html.unescape(newVal)
        newVal: str  = newVal['args']
        self.text =  newVal
        # self.text =  self._props['modelValue']
        if not self._registeredOnSaveCb:
            # self.on('keydown.s.ctrl', self._onSave)
            # print("editor")
            self.on('keydown.s.metaKey.prevent' if {device.getPlatform() == classes.enums.Platform.macos} else 'keydown.s.ctrl', self._onSave)
            self._registeredOnSaveCb = True
            self.update()
        self.onChange()
        
    async def _onSave(self):
        ui.keyboard
        if self.saveContentToFileOnSave != None:
            try:
                files.File(self.saveContentToFileOnSave).setContent(self.text)
                # print(f"Setting content of {self.saveContentToFileOnSave} to {self.text}")
            except Exception as exc:
                print(f'Editor exc: {exc}')
        if self.notifyOnSave:
            ui.notify(f"Saved to file:\n{self.saveContentToFileOnSave}" if self.saveContentToFileOnSave else "Saved!")
        self.onSave()

class FileView():
    def __init__(self, activePath: files.Path) -> None:
        self.activePath = activePath
        self.div = ui.element('div').style(add="height: 100%; height: 100%;")
        self.updateElements()
    def updateElements(self):
        # print("update el 1")
        self.div.default_slot.children.clear()
        with self.div:
            # with ui.element('div').style(replace="display:grid; gap: 10px; padding: 10px; background-color: gray; border-radius: 10px; border-color: transparent;"):
            if self.activePath.isFolder():
                with layout.gridResize().style(add='padding: 20px; gap: 8px; height: 100%; width: 100%;'):
                    folder = files.Folder(self.activePath)
                    for child in folder.getChildPaths():
                        # with ui.card().style(add="height: 200px; width: 200px;") as card:
                        # with el.layout.gridResizeElement().style(add="background-color: rgba(0, 0, 0, 0.014); height: 100px; width: 100px;"):
                        with ui.element('div').style(add="background-color: rgba(0, 0, 0, 0.014); height: 167px; width: 164px; border-radius: 11px; box-shadow: rgba(100, 100, 111, 0.1) 0px 2px 5px 0px; align-items: center; justify-content: center; text-align:center;"):

                            ui.label(child.getName())
                            if child.isFile():
                                child = files.File(child)
                                # with ui.card_section():
                                if child.isImage():
                                    ui.image(serveFiles.serveFile(str(child)))
                                else:
                                    ui.label(child.getContent()[:500])
                            elif child.isFolder():
                                child = files.Folder(child)
                                with layout.gridResize().style(add='padding: 2px; gap: 2px; transform: translate(7px, -4px);').classes(add="scale-hover"):  # align-items: center; justify-content: center;
                                    for childInner in child.getChildPaths()[:4]:
                                        with ui.element('div').style(add="padding: -10px; width: 90px; height: 86px; flex-direction: column;  border-radius: 10px; align-items: center; justify-content: center; display: flex; background-color: rgba(155, 155, 155, 0.06); zoom: 0.8; box-shadow: rgba(100, 100, 111, 0.1) 0px 2px 3px 0px;"):
                                            if childInner.isFile():
                                                childInner = files.File(childInner)
                                                pass
                                            if childInner.isFolder():
                                                childInner = files.Folder(childInner)
                                                ui.icon('folder').style("zoom: 3; margin: -3px; margin-top: 1px;")
                                            ui.label(childInner.getName(includeFileExtension=False)).style("padding: -10; zoom: 0.9; padding: 10px; text-align:center; margin: -8px;")

            elif self.activePath.isFile():
                file = files.File(self.activePath)
                variablesEl: list[ui.input] = []
                variablesStr: list[str] = []
                def addVariable(varName):
                    with variablesDiv:
                        variablesEl.append(ui.input(varName))
                        variablesStr.append(varName)
                def refreshVariables():
                    refreshedVars = string.getVariables(editor.text)
                    for var in refreshedVars:
                        if var in variablesStr:
                            continue
                        addVariable(var)
                    variablesStrRev = variablesStr.copy()
                    variablesStrRev.reverse()
                    for var in variablesStrRev:
                        if not var in refreshedVars:
                            i = variablesStr.index(var)
                            # .delete()
                            parent = variablesEl[i].parent_slot.parent
                            parent.remove(variablesEl[i])
                            parent.update()
                            variablesStr.pop(i)
                            variablesEl.pop(i)
                        

                with ui.element('div').style(replace="display:flex; gap: 10px; padding: 10px; background-color: transparent; border-radius: 10px; border-color: transparent; width: 100%; height: 100%;"):
                    # ui.label(file.getContent())
                    editor = Editor(file.getContent(), "File is empty, click here to type!", onSave=lambda a=None, b=None:print("save"), onChange=lambda:None, saveContentToFileOnSave=str(self.activePath), notifyOnSave=True).style(add="height: 1fr; width: 100%;")
                with ui.element('div').style(add="position:fixed; right:0; bottom:0;"):
                    # editor.text
                    variablesDiv = ui.element('div')
                    with variablesDiv:
                        for var in string.getVariables(editor.text):
                            addVariable(var)
                    ui.button("Refresh Variables", on_click=refreshVariables)