import socket
import threading
import uuid
import fast

randomStr = """Based on your input, get a random alpha numeric string. The random string generator creates a series of numbers and letters that have no pattern. These can be helpful for creating security codes.With this utility you generate a 16 character output based on your input of numbers and upper and lower case letters.  Random strings can be unique. Used in computing, a random string generator can also be called a random character string generator. This is an important tool if you want to generate a unique set of strings. The utility generates a sequence that lacks a pattern and is random.Throughout time, randomness was generated through mechanical devices such as dice, coin flips, and playing cards. A mechanical method of achieving randomness can be more time and resource consuming especially when a large number of randomized strings are needed as they could be in statistical applications.  Computational random string generators replace the traditional mechanical devices. Possible applications for a random string generator could be for statistical sampling, simulations, and cryptography.  For security reasons, a random string generator can be useful. The generation of this type of random string can be a common or typical task in computer programming.  Some forms of randomness concern hash or seach algorithms.  Another task that is random concerns selecting music tracks.In statistical theory, randomization is an important principle with one possible application involving survey sampling.Many applications of randomization have caused several methods to exist for generating random data. Lottery games is one current application. Slot machine odds are another use of random number generators."""
machinery =""
# (function() {
#   function create_UUID() {
#     var dt = new Date().getTime();
#     var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
#       var r = (dt + Math.random() * 16) % 16 | 0;
#       dt = Math.floor(dt / 16);
#       return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
#     });
#     return uuid;
#   }
  
#   var uuid = create_UUID();
#   if (!document.cookie.includes('f_sid')) {
#     document.cookie = "f_sid=" + uuid + `; expires=${new Date(Date.now() + 86400000/*24 hours*/).toUTCString()};  path=/`; // Fri, 31 Dec 9999 23:59:59 GMT
#   }
#   })();
# """ 
from .. import time as ftime
import datetime
import pytz
import typing
from classes import property
class Request():
    def __init__(self, request: str) -> None:
        self.request = request
        self.values: dict[str,str] = dict()
        self.path: str
        self.parameters: dict[str,str]
        self.cookies: dict[str,str] #  self.getValue('Cookie')
    @property
    def domain(self) -> str:
        return self.getValue('Host') 
    @property
    def domain(self) -> str:
        return self.getValue('Host') 
    def getValue(self, key: str):
        "getValue('Host') would return localhost:8000"
        if key in self.values:
            return self.values[key]
        else:
            startIndex =  self.request.find(key)+key.__len__()+2
            endIndex = self.request.rfind(' ', startIndex ,self.request.find(': ',startIndex))
            return self.request[startIndex:endIndex]
    
class HttpServer():
    def handleRequestInternal(self, clientSocket, address):
        request:str = clientSocket.recv(1024).decode()
        _fsidStartIndex=request.rfind('f_sid')
        if _fsidStartIndex == -1:
            fsid=False
        else:
            fsid= request[_fsidStartIndex:request.rfind(';', _fsidStartIndex)]
        url = request.split()[1] 
        
        responseMsg = f"<script>{machinery}</script><h1>Hello, world! You requested {url} from ip {address}</h1><p>{randomStr}</p><h2>full request: {request}</h2><p>end</p>"
        response = f"HTTP/1.1 200 OK\nContent-type: text/html\nCache-Control: max-age=86400\nSet-Cookie: {'' if fsid else 'f_sid=' + str(uuid.uuid4())} max-age=86400;\nContent-length: {len(responseMsg)}\n\n{responseMsg}".encode() # max-age controls how long static files are cached on the user, preventing static assets from being transfered from the server several times over. Measured in seconds, so 86400 is 24 hours (24*60*60).
        clientSocket.send(response)
        clientSocket.close()
    if typing.TYPE_CHECKING:
        def handleRequest(self, request: Request) -> str | typing.Callable:
            pass
    def __init__(self, adress='127.0.0.1', port=80, handleRequest: str | typing.Callable="Override handleRequest on HttpServer to change the content of this page.") -> None:
        self.adress = adress
        self.port = port
        self.handleRequest = handleRequest
    def getAdressStr(self):
        return f"{self.adress}:{self.port}"
    def start(self):
        "Start webserver, listen to requests. Blocking operation"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.serverSocket:
            self.serverSocket.bind((self.adress, self.port))
            self.serverSocket.listen()

            print(f"Serving on {self.getAdressStr()}")

            while True:
                client_socket, address = self.serverSocket.accept()
                threading.Thread(target=self.handleRequestInternal,args=(client_socket,address)).start()
