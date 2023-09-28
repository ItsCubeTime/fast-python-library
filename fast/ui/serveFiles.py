"""Serves files using FastAPI via nicegui & HTTP. Ive chosen to put this under the ui module instead of the networking module as
 I want to keep dependencies low in the networking module."""
import pathlib
from .. import networking
from .. import string
from nicegui import ui
import nicegui
import fastapi
from .. import files

class ServedString():
    # @todo add support for serving raw strings as well, not just files. Thinking a syntax like serveString("<p>page available under localhost/home<p>", "home")
    pass


class ServedFile():
    def __init__(self, filePath, url=None) -> None:
        filePath = str(filePath).replace('\\', '/').replace('//', '/')
        if filePath[-1] == '/':
            filePath = filePath[:-1]
        if url == None:
            url = f"{networking.urlEncode(filePath)}"
        # print(f"encodedFileUrl: {url}")
        self.filePath = filePath
        "Path on the harddrive"
        self.url = url
        # print(f"urlto dec: {url}")
        # print(f"appending url: {url}")
        servedData[url] = self

    def __str__(self):
        return self.url
    

class ServedFolder():
    "Somewhat computetionally heavy on requests as we are not using hashing or direct memory adresses for lookup, so, I recommend keeping the number of servedFolders limited"
    def __init__(self, filePath, url=None) -> None:
        filePath = str(filePath).replace('\\', '/').replace('//', '/')
        if filePath[-1] == '/':
            filePath = filePath[:-1]
        if url == None:
            url = f"{networking.urlEncode(filePath)}"
        self.filePath = filePath
        "Path on the harddrive"
        self.url = url
        servedFolders.append(self)
def serveFolder(filePath, url=None):
    return ServedFolder(filePath, url).url

servedData: dict[str, ServedFile | ServedString] = dict()
"""Keys are urls, lacking the domain & port. Because a dict can only store 1 value per key, if we try adding the same url several times older values should get deleted
by pythons garbage collector (assuming those older values arent being held onto somewhere)."""

servedFolders: list[ServedFolder] = []
"Somewhat computetionally heavy on requests as we are not using hashing or direct memory adresses for lookup, so, I recommend keeping the number of servedFolders limited"

def _serveFileInit():
    # print("initServeFile")

    # @nicegui.app.get("/{item_id}")
    # async def read_item(item_id):
    #     # print(f"drivePath: {servedData[item_id].filePath}")
    #     pathlibObj = pathlib.Path(servedData[item_id].filePath)
    #     fileStream = pathlibObj.open(errors="ignore")
    #     returnVal = fileStream.read()
    #     return returnVal

    # @nicegui.app.get("/serveFile/{item_id}")
    # async def read_item2(item_id):
    #     return await read_item(item_id)

    # @nicegui.app.get("/foobar/")
    # async def read_item2(request: fastapi.Request):
    #     return fastapi.responses.FileResponse(servedData[request.url.path[1:]].filePath)

    # @nicegui.app.middleware("http")
    def prepareResponseFromFile(filePath):
        responseFile = open(filePath, mode="rb")
        mediaType = None
        fileExt = filePath[filePath.rindex('.')+1:]
        if fileExt == 'js': # @note for some reason js files cant be loaded in <script src="myLink.js"></script> unless the file the link has an associated media type/"Mime" type. So far I havent seen any similar issues with other file types.
            mediaType = 'text/javascript'
        return fastapi.responses.StreamingResponse(responseFile, media_type=mediaType)  # @todo Figure out why request.url.path gives a
        # @todo Figure out if StreamingResponse is really better over FileResponse for this usecase.
        # return fastapi.responses.FileResponse(servedData[request.scope["raw_path"][1:]].filePath)  # @note attempted fix
        # decoded string, when I really want the raw url.


    @nicegui.app.middleware("http")
    async def catch_all(request: fastapi.Request, call_next):
        # print(f"requestedUrl {request.url},requestedUrlPath {request.scope['raw_path'][1:]}, servedData: {servedData}")
        # print(f"requestedUrl {request.url},requestedUrlPath {request.url.path[1:]}, servedData: {servedData}")
        try:
            # import os
            # os.system('cls')
            # print(f"Incoming request {request.url._url}")
            # return fastapi.responses.FileResponse(servedData[networking.urlEncode(request.url.path[1:])].filePath)

            url = networking.urlEncode(request.url._url)
            # afterDomainNPort = url[22+4:]
            afterDomainNPort = url[string.indexOfSubstring(url, '/', 3)+1:]
            # print(f"afterDomainNPort: {afterDomainNPort}")
            # afterDomainNPort = url[find_nth_overlapping(url, '/', 3)+1:]
            filePath = servedData[afterDomainNPort].filePath
            # filePath = servedData[networking.urlEncode(request.url.path[1:])].filePath
            # print(f"Awesome file path: {filePath}")
            # if filePath.__contains__('.css'):
            #     print(f'Responding w file: {filePath}')
            return prepareResponseFromFile(filePath)
        # @todo Its somewhat undesireable that servedData now overrides/takes
        # presedence over other urls registered, but we cannot call "call_next()" it seems as it will start to generate a response, that will inform the client
        # of the desired file type - which may not match with the file we are trying to serve if it turns out servedData has a match against the requested url.

        except Exception as exc:
            try:
                for servedFolder in servedFolders:
                    if afterDomainNPort in servedFolder.url:
                        # Hit
                        filePath = networking.urlDecode(afterDomainNPort)
                        return prepareResponseFromFile(filePath)
            except Exception as exc:
                pass
            # from .. import debugging
            # if str(exc).__contains__('fileManagerSidebar.css'):
            # print(f"possible keys: {servedData.keys()}")
            # print(f"Super exc: {exc}")
            # debugging.print(exc)
            response = await call_next(request)
            # from fastapi.send
            # return fastapi.responses.StreamingResponse(open(servedData[request.url.path[1:]].drivePath, mode="rb"), media_type="image/png")
            # return fastapi.responses.FileResponse(filename=servedData[request.url.path[1:]].drivePath, media_type="image/png")
            # return fastapi.Response(content=await read_item(request.url.path[1:]))
        # if response.status_code == 404:
        #     url = str(request.url)
            # print(f"redirecting {request.url.path}")

            # print(f"redirecting {url[url.find('/'):]}")

        return response
_serveFileInit()

def serveFile(filePath: str, url: str = None):
    "Serves a file on the nicegui server, like a png, jpg, txt, svg or html document and gives you the url we are serving under."

    # @nicegui.app.get(url)
    # async def httpResponse(request: fastapi.Request):
    #     return pathlib.Path(filePath).open().read()
    servedFile = ServedFile(filePath, url)
    return servedFile.url



def linkCss(origin:str, originIsLink=False):
    """origin expects a local filepath as str if originIsLink is false, otherwise it expects a linked css document from the web, or hosted locally.
    
    @todo Make it so a document can only link once per page"""
    originLink = origin if originIsLink else serveFile(origin)
    ui.add_head_html(f'<link rel="stylesheet" href="{originLink}">')


def addJsToDom(origin:str, originIsLink=False):
    """Takes a local js file, serves it under a url and injects it to the page via a script <script src="..."> tag"""
    originLink = origin if originIsLink else serveFile(origin)
    finalStr = f'<script src="/{originLink}" type="module"></script>/>'
    # print(finalStr)
    ui.add_head_html(finalStr)

import traceback

def linkThisFilesCss():
    "Assumes the existence of a file by the same name as the file where this function was called, but with a file extension .css and tries to link it to the document."
    stack = traceback.extract_stack()
    fileName = stack[-2].filename
    fileName = fileName[:fileName.rfind('.')] + ".css"
    linkCss(fileName)

