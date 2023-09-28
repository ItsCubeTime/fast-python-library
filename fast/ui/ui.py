from __future__ import annotations
import asyncio
from . import elements as el
from .. import asyncronous
import pathlib
from .import serveFiles
import sys
import time

import toga

from .. import asyncronous, devTools, string, networking
from ..data import data

import nicegui
from nicegui import ui
from .. import color
from . import colors
class TogaApp(toga.App):
    hideNativeTitlebar = False
    isWindowBeingResizedByUser = False
    _lastTime_isWindowBeingResizedByUser_WasFalse = 0
    _startupTime = -1
    def __init__(self, formal_name=None, app_id=None, app_name=None, id=None, icon=None, author=None, version=None, home_page=None, description=None, startup=None, windows=None, on_exit=None, factory=None):
    
        super().__init__(formal_name, app_id, app_name, id, icon, author, version, home_page, description, startup, windows, on_exit, factory)
    def startup(self):
        # self._impl.create_menus = lambda *x, **y: None # Remove menubar
        # print("START")

        main_box = toga.WebView(url=self.url)
        from toga import style
        
        main_box.style=style.Pack(padding_top=-10, alignment="top")
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        # self.main_window.h
        # self.Controls = False
        def removeTitlebar(e=None, a=None):
            # i = 0
            # while i < 7:
            #     i += 1
            #     time.sleep(i*0.15)
            # time.sleep(1.5)
            # print(f"isAccessible: {self._impl.interface.main_window._impl.isAccessible}")
            # print(f"isAccessible: {self._impl.native.isAccessible}")
            # print(f"isLoadingIn: {'Load' in self._impl.interface.main_window._impl.native.__dir__()}")
            # while not self._impl.interface.main_window._impl.native.Visible:
            #     print("Not vis")
            #     time.sleep(0.1)
            # print("Vis")
            # time.sleep(0.1)
            if False:
                time.sleep(2)
                # print(
                #     f"visible: {self._impl.interface.main_window._impl.native.Visible}")
                # self.main_window._impl.native.set_Text("")          # Windows only Use _impl.set_title instead.
                self.main_window._impl.native.FormBorderStyle = getattr(self.main_window._impl.native.FormBorderStyle, "SizableToolWindow")
                # self.main_window._impl.native.FormBorderStyle = self.main_window._impl.native.FormBorderStyle.__dir__()['Fixed3D']
                # self.main_window._impl.native.FormBorderStyle = eval("print(self.main_window._impl.native.FormBorderStyle.__dir__()['None'])")
                # self.main_window._impl.native.Text = ""
                self._impl.interface.main_window._impl.set_title("")
                self.main_window._impl.native.set_ControlBox(
                    False)  # Windows only
                print(self.main_window._impl.native.get_ShowInTaskbar())
                self.main_window._impl.native.set_ShowInTaskbar(True)
            else:
                # self.main_window._impl.native.BackColor = self.main_window._impl.native.BackColor.Red
                import ctypes
                from ctypes import wintypes
                user32 = ctypes.WinDLL("user32.dll")
                
                hwnd = self.main_window._impl.native.Handle
                hwndInt = int(str(hwnd))
                hwnd = wintypes.HWND(int(str(hwnd)))

                import win32con
                import win32gui
                import win32api
                # print(f"awesome -> {self.main_window._impl.native.__dir__()} <-")
                # self.main_window._impl.native.WndProc = lambda a=None: print("hi")
                # self.main_window._impl.native.DefWndProc = lambda a=None: print("hi")
                oldWndProc = win32gui.GetWindowLong(hwndInt,win32con.GWL_WNDPROC)
                # oldWndProc = self.main_window._impl.native.WndProc
                wndInitTime = time.time()

                from pynput.mouse import Listener


                def on_move(x, y):
                    pass
                    # print(x, y)


                def on_click(x, y, button, pressed):
                    print(x, y, button, pressed)


                def on_scroll(x, y, dx, dy):
                    pass
                    # print(x, y, dx, dy)


                Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
                    # listener.start()
                    # listener.join()


                def wndProc(hWnd, msg, wParam, lParam, *pack):
                    
                    import win32con

                    # if win32con.WM_PAINT == msg: 
                    # if win32con.WM_SIZE == msg: 
                        # win32gui.SendMessage(hwndInt, win32con.WM_PRINT, None, win32con.PRF_NONCLIENT)
                        # lParam = win32con.PRF_NONCLIENT
                        # wParam = None
                        # win32gui.UpdateLayeredWindow(hwndInt)


                    if self._startupTime == -1:
                        self._startupTime = time.time()
                    # nonlocal oldWndProc
                    # oldWndProc = ctypes.cast(oldWndProc, ctypes.POINTER(ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int))).contents
                    # if wParam:
                    #     pass
                        # res = win32gui.CallWindowProc(
                        #     wndProc, hWnd, msg, wParam, lParam
                        # )
                        # try:
                        #     lParam.rgrc[0].top -= -6
                        # except:
                        #     pass
                        # sz = win32gui.NCCALCSIZE_PARAMS.from_address(lParam)
                        # sz.rgrc[0].top -= 6 # remove 6px top border!
                        # return res
                    # if msg == win32con.WM_SIZE:
                    #     print("RESIZE STUFF")
                    #     win32api.SetWindowLong(hwndInt,
                    #                         win32con.GWL_WNDPROC,
                    #                         oldWndProc)
                    # if msg == win32con.WM_SIZING:
                    #     print("RESIZING STUFF")
                    # return oldWndProc()
                    # win32gui.CallWindowProc(ctypes.cast(lambda: print("hi"), ctypes.POINTER(ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int))).contents, hWnd, msg, wParam, lParam)
                    # self.main_window._impl.native.WndProc(hwndInt, msg, wParam, lParam)
                    # import inspect
                    # import ctypes.wintypes
                    # msgObj = ctypes.wintypes.MSG()
                    # msgObj.hWnd = hwndInt
                    # msgObj.message = msg
                    # msgObj.wParam = wParam
                    # msgObj.lParam = lParam
                    # print(WinForms.Message().__dir__())
                    # ctypes.cast(, )
                    # ctypes.pointer()



                    from System import IntPtr
                    from System import Int32
                    from toga_winforms.libs.winforms import WinForms
                    msgObj = WinForms.Message()
                    msgObj.set_HWnd  (IntPtr(hwndInt))
                    msgObj.set_Msg   (Int32(msg))
                    msgObj.set_WParam(IntPtr(wParam))
                    msgObj.set_LParam(IntPtr(lParam))


                    # print(inspect.getargspec(self.main_window._impl.native.WndProc))
                    # WM_NCCALCSIZE = 0x0083
                    # if int(msg) == int(WM_NCCALCSIZE):
                    #     return 0
                    # result = win32gui.DefWindowProc(hwndInt, msg, wParam, lParam, *pack)
                    # msgObj.set_Result(IntPtr(result))
                    # print(f"result -> {msgObj2.__dir__()} <- type: {type(msgObj2)}")
                    # return result.LParam
                    # self.main_window._impl.native.WndProc(msgObj)
                    # return result
                    # return 0
                    # print(f"dir: {msgObj2.WParam.__dir__()}")
                    # if win32con.WM_SIZING:
                    #     return 0
                    # user32 = ctypes.WinDLL('user32.dll') 
                    # win32api.GetProcAddress
                    # win32api.GetProcAddress(win32api.GetModuleHandle())
                    # NCCALCSIZE_PARAMS = user32.GetProcAddress(b'NCCALCSIZE_PARAMS')
                    # NCCALCSIZE_PARAMS = win32api.GetProcAddress(hwndInt, 'NCCALCSIZE_PARAMS')
                    # user32.NCCALCSIZE_PARAMS
                    # if wParam and msg == win32con.WM_SIZE:
                    # if wParam and msg == 13:


                    import keyboard
                    if int(msg) == win32con.WM_NCHITTEST and keyboard.is_pressed('w'):
                        result = win32con.HTCAPTION


                    if not win32gui.PeekMessage(hwndInt, msg, 0, msg):
                        return 0
                    # if msg != 49771:
                    
                    if int(msg) == win32con.WM_ENTERSIZEMOVE:
                    # if int(msg) == win32con.WM_LBUTTONDOWN:
                        # if (win32gui.IsCursorOnResizeBorder(hwnd, LOWORD(lParam), HIWORD(lParam))) {
                            # resizing = true;
                        win32gui.SetCapture(hwndInt)
                        win32gui.SendMessage(hwndInt, win32con.WM_SYSCOMMAND, win32con.SC_SIZE | win32con.WMSZ_BOTTOMRIGHT, 0)
                        if time.time() - self._lastTime_isWindowBeingResizedByUser_WasFalse > 0.08:
                            # print("True")
                            self.isWindowBeingResizedByUser = True
                            # return 0
                    # if int(msg) == win32con.WM_LBUTTONUP:
                    # if int(msg) == win32con.WM_EXITSIZEMOVE:
                        # self._lastTime_isWindowBeingResizedByUser_WasFalse = time.time()
                        self.isWindowBeingResizedByUser = False
                        # win32gui.ReleaseCapture()
                        # win32gui.SendMessage(hwndInt, win32con.WM_SYSCOMMAND, win32con.SC_SIZE | win32con.WMSZ_BOTTOMRIGHT, 0)
                        # win32gui.ShowWindow(hwndInt, win32con.SW_HIDE)
                        # win32gui.cursor
                        # win32gui.ShowWindow(hwndInt, win32con.SW_SHOW)
                        # print("False")
                    # if time.time() - self._lastTime_isWindowBeingResizedByUser_WasFalse  < 0.01:
                        return 0
                    # if win32con.WM_ERASEBKGND == int(msg):
                    #     return 0
                    # Necessary: 131 133 71
                    # if int(msg) == win32con.WM_SIZING:
                    #     self.main_window._impl.native.Controls[0].Update()
                    #     self.main_window._impl.native.Controls[0].UpdateBounds()
                        print("update")
                    if int(msg) in [ win32con.WM_SIZING,  win32con.WM_SIZE, win32con.WM_NCCALCSIZE, win32con.WM_MOUSEMOVE, win32con.WM_NCHITTEST]:
                    # if int(msg) in [20,  60, 61, 49771, 0] or int(msg) == win32con.WM_SIZING or int(msg) == win32con.SM_CXBORDER or int(msg) == win32con.SM_CYCURSOR or  int(msg) == win32con.SM_CXCURSOR  or  int(msg) == win32con.SM_CYMENU or int(msg) == win32con.SM_CXDOUBLECLK:
                    # if int(msg) == win32con.WM_SIZE or int(msg) == win32con.SM_SHOWSOUNDS or int(msg) == win32con.SM_CXDOUBLECLK or int(msg) == 131 or int(msg) == 133 or int(msg) == 20:
                        if not self.isWindowBeingResizedByUser and self._lastTime_isWindowBeingResizedByUser_WasFalse != 0:
                        # import mouse
                        # if not mouse.is_pressed() and time.time() - self._startupTime > 1:
                            # print("early return")
                            # win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONDOWN, win32con.HTRIGHT, 0)
                            # win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONUP, win32con.HTRIGHT, 0)
                            # win32gui.SendMessage(hwndInt, win32con.WM_EXITSIZEMOVE, 0, 0)
                            # self.main_window._impl.native.OnResizeEnd()
                            pass
                            # size = self.main_window._impl.native.get_Size()
                            # print(size.__dir__())
                            # self.main_window._impl.native.set_MaximumSize(size)
                            # self.main_window._impl.native.set_MinimumSize(size)
                            # return 0
                        else:
                            pass
                            # print(f"Not early return: msg {msg} wParam {wParam} lParam {lParam}")
                    
                    if not int(msg) == 49771:
                        import keyboard
                        if keyboard.is_pressed('q'):
                            win32gui.ReleaseCapture();
                            # if int(msg) == 528:
                            # if int(msg) == win32con.WM_LBUTTONDOWN:
                                # win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONDOWN, 2, 0)
                            print(f"msg {msg} wParam {wParam} lParam {lParam}")
                        # win32gui.InvalidateRect(hwndInt, win32gui.GetClientRect(hwndInt), True)
                        
                    # if msg == win32con.WM_NCLBUTTONUP or win32con.SM_CXDOUBLECLK:
                    #     win32gui.SendMessage(hwndInt, win32con.WM_EXITSIZEMOVE, 0, 0)


                    msgObj2 = WinForms.Form.WndProc(self.main_window._impl.native, msgObj)
                    # result = msgObj2.Result
                    # result =  win32gui.DefWindowProc(hwndInt, msg, wParam, lParam)
                    result =  win32gui.DefWindowProc(hwndInt, msgObj2.Msg, msgObj2.WParam.ToInt64(), msgObj2.LParam.ToInt64())

                    # if win32con.WM_NCHITTEST == int(msg):
                    #     if win32con.HTCLIENT == int(result):

                    # result =  win32gui.DefWindowProc(hwndInt, msg, wParam, lParam)



                    # if wParam  and msg == win32con.WM_SIZE:
                    # hasTimePassed = wndInitTime < time.time()-10
                    if int(wParam)==1  and int(msg) == win32con.WM_NCCALCSIZE :
                    # if wParam  == 12 and msg == win32con.WM_SIZE:
                        # print(f"wParam: {wParam}")
                        # sz = user32.NCCALCSIZE_PARAMS.from_address(lParam)
                        # class RECT(ctypes.Structure):
                        #     _fields_ = [("left", ctypes.c_long),
                        #                 ("top", ctypes.c_long),
                        #                 ("right", ctypes.c_long),
                        #                 ("bottom", ctypes.c_long)]

                        class WINDOWPOS(ctypes.Structure):
                            _fields_ = [("hwnd", wintypes.HWND),
                                        ("hWndInsertAfter", wintypes.HWND),
                                        ("x", ctypes.c_int),
                                        ("y", ctypes.c_int),
                                        ("cx", ctypes.c_int),
                                        ("cy", ctypes.c_int),
                                        ("flags", ctypes.c_uint)]
                            
                        # Define the structs
                        class RECT(ctypes.Structure):
                            _fields_ = [("left", ctypes.c_long),
                                        ("top", ctypes.c_long),
                                        ("right", ctypes.c_long),
                                        ("bottom", ctypes.c_long)]


                        # define the NCCALCSIZE_PARAMS struct as a ctypes.Structure
                        class NCCALCSIZE_PARAMS(ctypes.Structure):
                            _fields_ = [
                                # ("rgrc", ctypes.POINTER(wintypes.RECT)),  # pointer to RECT struct
                                # ("lppos", ctypes.POINTER(WINDOWPOS)),  # pointer to WINDOWPOS struct
                                ("rgrc", wintypes.RECT),  # pointer to RECT struct
                                ("lppos", WINDOWPOS),  # pointer to WINDOWPOS struct
                            ]
                        # import win32ui
                        # win32ui.ncc
                        # win32gui_struct.
                        
                        # create an instance of the NCCALCSIZE_PARAMS struct from the lParam value
                        # from struct import pack, unpack
                        # unpack()
                        # sz = NCCALCSIZE_PARAMS.from_address(msg)
                        sz = NCCALCSIZE_PARAMS.from_address(msgObj2.LParam.ToInt64())
                        # sz = NCCALCSIZE_PARAMS.from_address(lParam)
                        # sz = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents
                        # sz = lParam
                        try:
                            # print(sz.lppos.__dir__())
                            pass
                            if sz and sz.rgrc:
                                pass
                                # if hasattr(sz.rgrc[0], 'top:'):
                                # print(f"rgrc0: {sz.rgrc[0]._objects.__dir__()}") # remove 6px top border!
                                # print(f"rgrc1: {sz.rgrc[0].__dir__()}") # remove 6px top border!
                                # print(f"rgrc2: {sz.rgrc.contents.__dir__()}") # remove 6px top border!
                                sz.rgrc.top -= 3+10+48
                                sz.rgrc.bottom += 2+5+1        
                                sz.rgrc.left -= 2+5+1    
                                sz.rgrc.right += 2+5+1         
                                # if sz.rgrc[0]._b_needsfree_:
                                # sz.rgrc[0]._objects.top -= 20
                                # print(f"rgrc: {sz.rgrc[0].__dir__()}") # remove 6px top border!
                                # sz.rgrc[0] = sz.rgrc[0]()
                                # top = ctypes.c_long.from_address(ctypes.addressof(sz.rgrc[0]) + ctypes.sizeof(RECT))
                                # top.value = 5
                                # sz.rgrc[0].bottom = 200
                                # sz.rgrc[0].left = 200
                                # sz.rgrc[0].right = 200
                                # lParam = sz
                                # return 0
                                # return win32con.WVR_HREDRAW
                                return 0
                                # sz.rgrc[0].top -= 0 # remove 6px top border!
                        except Exception as exc:
                            print(f"exc caught {exc}")
                            return 0
                        else:
                            print("SUCCEEESS")
                        # return res
                    return result



                    # msgObj.set_LParam(IntPtr(lParam))
                    # msgObj2 = WinForms.Form.WndProc(self.main_window._impl.native, msgObj)
                    # result =  win32gui.DefWindowProc(hwndInt, msgObj2.Msg, msgObj2.WParam.ToInt64(), msgObj2.LParam.ToInt64())
                    # msgObj2 = WinForms.Form.WndProc(self.main_window._impl.native, msgObj)
                    # result =  win32gui.DefWindowProc(hwndInt, msg, wParam, lParam)


                win32gui.SetWindowLong(hwndInt,win32con.GWL_WNDPROC,wndProc) 

                
                
                # print(f"formBorderStyle: {self.main_window._impl.native.get_FormBorderStyle()}")


                # self.main_window._impl.native.DefWndProc = lambda m: print("wndproc")
                # self.main_window._impl.native.SizeFromClientSize1 = True
                # title = ctypes.create_unicode_buffer(1024)
                # user32.GetWindowTextW(hwnd, title, ctypes.sizeof(title))
                # time.sleep(4)
                style = 0x00040000  # Adds rounded corners & resize controls at the egdes (The win11 look). When used alone it will give an odd looking titlebar at the top. Resizing the window removes this titlebar
                style |= win32con.WS_CAPTION

                style |= win32con.WS_MINIMIZEBOX|win32con.WS_MAXIMIZEBOX|win32con.WS_SYSMENU
                # style = 0xC00000
                # extStyle = win32con.GWL_EXSTYLE
                extStyle = user32.GetWindowLongPtrW(hwnd, -20)
                # extStyle |= win32con.WS_EX_COMPOSITED
                extStyle |= 0x00080000 # win32con.WS_EX_LAYERED @note This combined with setting a color style removes an artifact when
                # expanding the window where the edge being expanded has a small transparent area on the inside
                # extStyle |= win32con.SSTF_BORDER
                # extStyle |= win32con.WS_SIZEBOX
                # flags = win32con.SWP_FRAMECHANGED|win32con.SWP_NOMOVE|win32con.SWP_NOSIZE|win32con.SWP_NOZORDER|win32con.SWP_NOOWNERZORDER
                # if msg == win32con.WM_NCCALCSIZE:
                #         # res = CallWindowProc(
                #         #     wndProc, hwnd, msg, wParam, lParam
                #         # )
                #         sz = NCCALCSIZE_PARAMS.from_address(lParam)
                #         sz.rgrc[0].top -= 6 # remove 6px top border!
                #         return res
                # extStyle |= win32con.SM_CXSCREEN 
                # extStyle |= win32con.WS_POPUP 
                # extStyle |= win32con.WS_VISIBLE
                # extStyle = win32con.WS_EX_CLIENTEDGE  
                # extStyle = user32.GetWindowLongPtrW(hwnd, win32con.GWL_EXSTYLE)
                # extStyle |= 0x00080000 # Transparent background - works, but the window breaks after a bit. This is WS_EX_LAYERED 
 
                # extStyle = 0x02000000   # Failed Transparent background
                # extStyle = 0x00000020 # Failed Transparent background
                # Steal begin
                # hwndSteal = 65696 # Discord
                # hwndSteal = wintypes.HWND(int(str(hwndSteal)))
                # style = user32.GetWindowLongPtrA(hwndSteal, -16)
                # style |= 0x00040000
                # extStyle = user32.GetWindowLongPtrA(hwndSteal, -20)
                # Steal end
                # user32.SetWindowLongA(hwnd, -16, style)
                from ctypes import windll

                # windll = windll.LoadLibrary("DwmExtendFrameIntoClientArea")
                # windll.DwmExtendFrameIntoClientArea(hwnd, (0,0,0,0))
                # win32gui.draw(hwndInt, None,200,0,0,0,flags)
                
                # @note remove titlebar/ apply styling
                # style = 0x00080000|0x00040000
                # user32.SetWindowLongPtrA(hwnd, -16, style)
                # extStyle = 0x00080000
                # user32.SetWindowLongPtrW(hwnd, -20, extStyle)
                # win32gui.SetLayeredWindowAttributes(hwndInt, win32api.RGB(0,0,0), 255, win32con.LWA_COLORKEY)
                # win32gui.SetLayeredWindowAttributes(hwndInt, win32api.RGB(0,0,0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
                # from toga_winforms.libs import Color
                from toga_winforms.widgets import webview
                # @note Transparency attempt
                from toga_winforms.libs import WinForms, Color
                self.main_window._impl.native.SetStyle(WinForms.ControlStyles.SupportsTransparentBackColor, True)
                # win32gui.GetTextColor
                # bgColorRgb = [int(((x/255.0)**2.2)*255) for x in bgColorRgb]
                bgColorRgb = color.hexToRgb(colors.colors.pageBackground)
                bgColorWin32 = Color.FromArgb(bgColorRgb[0],bgColorRgb[1],bgColorRgb[2])
                self.main_window._impl.native.set_BackColor(bgColorWin32)
                # self.main_window._impl.native.set_BackColor(Color.FromArgb(255,0,0,0))
                # print(f"color-> {Color.__dir__(Color)} <-")
                # self.main_window._impl.native.set_BackColor(Color.Transparent)
                # for control in self.main_window._impl.native.get_Controls():
                #     control.SetStyle(WinForms.ControlStyles.SupportsTransparentBackColor, True)
                #     control.set_BackColor(bgColorWin32)
                #     # print(f"ctrl: {control}")
                #     control.DefaultBackgroundColor = bgColorWin32
                    # control.set_BackColor(Color.Transparent)
                # async def runAsync321():
                #     await asyncio.sleep(4)
                #     print("excellence")
                    
                # asyncronous.runSync(runAsync321(), dontWait=True)


                # HBRUSH brush = win32gui.CreateSolidBrush(win32api.RGB(0, 0, 255))
                # win32gui.SetClassLongPtr(hwnd, win32.GCLP_HBRBACKGROUND, (LONG_PTR)brush);
                # self.main_window._impl.native.set_FormBorderStyle(self.main_window._impl.native.get_FormBorderStyle().SizableToolWindow)

                # from ctypes import windll
                # windll.uxtheme.SetWindowTheme(hwnd, "DarkMode_Explorer", None)
                # set the background color to dark gray
                self.main_window.size = (self.main_window.size[0], self.main_window.size[1]+1) # Refreshes the window, removing glitched artifact described above
                # time.sleep(2)
                
                # self._impl.width = self.main_window._impl.width + 1000
                # user32.UpdateWindow(hwnd)
                # self.main_window.position = (self.main_window.position[0], self.main_window.position[1]+1)
        self._impl.create_menus = lambda *x, **y: None  # Removes the app menubar
        self.main_window._impl.create_toolbar = lambda: None  # Removes the app menubar
        # print(self.main_window._impl.native.__dir__())
        # self.main_window._impl.native.remove_MenuStart()
        
        # for control in self.main_window._impl.native.Controls:
        #         # if control != main_box:
        #         self.main_window._impl.native.Controls.Remove(control)
        # self.main_window._impl.native.Controls.Add(main_box._impl.native) # @note This was an experiment to check if the white bar at the top was some kind of control that could be removed, turns out it was not.
                
        self.icon = data.appIcon
        # self._impl.set_title("")
        # self._impl.interface.main_window._impl.set_title(self.formal_name)
        self._impl.interface.main_window._impl.native.Load.__iadd__(
            removeTitlebar)
        # asyncronous.runAsync(removeTitlebar)
        self.main_window.show()
        if self.hideNativeTitlebar:
            pass
            # print("dir", self._impl.interface.main_window._impl.native.Load.__dir__())
            # asyncronous.runAsync(removeTitlebar)

        # self._impl.native.onClosing = lambda:print("Enter")


# def mainLoop(url, ):
#     # print(f"args: {args}")
#     # url = f"{adress}:{port}"
#     # print("mainLoop")  # ?
#     # print(f"url: {url}")
#     togaApp = TogaApp(data.appName, string.PascalCaseTo_snake_case(
#         f"org.{data.publishers[0]}.{data.appName}".replace(' ', '')))
#     # togaApp.on_exit

#     togaApp.url = url
#     togaApp.main_loop()


def applyNiceguiDesktopSpecificStyling(window: Window):
    from nicegui import ui
    import nicegui

    # nicegui.app.add_static_files('/fastAssetsLogo', data.appIcon[:data.appIcon.rfind('/')])

    # with ui.header(fixed=True)as header:
    # header.style(add="background-color: transparent; pointer-events: none;")
    # with ui.row() as fadeoutGradient:
    #     fadeoutGradient.""
    
    # with ui.card() as topFadeout:
        # topFadeout._classes.clear()
        # topFadeout.style(add="overflow: overlay; position:fixed; top:-3px; left:-3px;right:-3px; box-shadow: 0 0 0; background-color: transparent; backdrop-filter: blur(10px); ") #background-image: linear-gradient(white, white, transparent);

    with el.boxes.Card() as titlebar:
        
        titlebar.style(add="top:14px; left:8.3px;right:8.3px; overflow: overlay;  position:fixed;   ") #background-image: linear-gradient(white, transparent);
        # titlebar.style(add="top:14px; left:10px;right:10px; overflow: overlay; padding: 14px; align-items: center; position:fixed; border-radius: 9px; background-color: transparent; backdrop-filter: blur(10px); ") #background-image: linear-gradient(white, transparent);
        # titlebar.style(add="overflow: overlay; position:fixed; top:-3px; left:-3px;right:-3px; background-color: transparent; backdrop-filter: blur(10px); background-image: linear-gradient(white, transparent);")
        # titlebar.on("mousedown", lambda: print("Down"))
        # async def asyncBegin():
        #     print("AsyncBegin")
        # titlebar.on("mousedown", asyncBegin)
        titlebar.on("mousedown", window.follow_mouse_begin)
        # titlebar.on("mouseup", lambda: print("Up"))
        titlebar.on("mouseup", lambda: window.follow_mouse_end())
        # background-image: linear-gradient(direction, color-stop1, color-stop2, ...);
        with ui.row() as titlebarRow:
            titlebarRow._classes.clear()
            titlebarRow._style.clear()
            titlebarRow.style(add="display: flex; align-items: center; justify-content: space-between; align-self:stretch; ")

            # ui.card((data.appName)
            with ui.row() as leftTitlebarRow:
                leftTitlebarRow._classes.clear()
                leftTitlebarRow._style.clear()
                # leftTitlebarRow.style(add="align-items: center; display: flex; width: 100%;")
                leftTitlebarRow.style(add="align-items: center; display: flex;")
                ui.image(serveFiles.serveFile(data.appIcon)).style(add="width: 32px;")
                ui.label(data.appName)
            # ui.html('background-color:red;"></div>')
            ui.element("div").style(add="display: flex; flex-grow: 1;")
            with ui.row() as rightTitlebarRow:
                rightTitlebarRow._classes.clear()
                rightTitlebarRow._style.clear()
                # rightTitlebarRow.style(add="align-items: center; display: flex; justify-content: flex-end; background-color: red;")
                rightTitlebarRow.style(add="align-items: center; display: flex; gap: 12px;")
                # def windowDragTest():
                #     import win32gui
                #     import win32con
                #     # from toga_winforms.libs import winforms
                #     import ctypes.wintypes
                #     hwnd = window.togaApp.main_window._impl.native.Handle
                #     hwndInt = int(str(hwnd))
                #     # hwnd = ctypes.wintypes.HWND(int(str(hwnd)))
                #     win32gui.ReleaseCapture()
                #     HT_CAPTION = 2
                #     win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONDOWN, HT_CAPTION, 0)
                def show():
                    pass
                    # dropDown.classes(add="rotate180" )
                def hide():
                    pass
                    # print("hide")
                    # dropDown._classes.clear()
                    # dropDown.update()
                def createPopup():
                    with el.popups.Popup() as popup:
                    # with el.popups.Popup(onShow=lambda: (dropDown._style.pop("rotate180"), dropDown.update())if dropDown._style.__contains__("rotate180") else dropDown.style(add="rotate180" )) as popup:
                        pass
                        el.popups.PopupButton("Resize Window", lambda: print("Popup"))
                        el.popups.PopupButton("Resize Window", lambda: print("Popup"))
                        el.popups.PopupButton("Resize Window", lambda: print("Popup"))
                        client=nicegui.globals.get_client()
                        async def hiThere(a=None):
                            await client.connected()
                            print(asyncronous.runSync(client.run_javascript('[cursorX, cursorY]')))
                        el.popups.PopupButton("hi", hiThere)
                        def cb(a, b=None):
                            colors.colors.toggleDarkMode(client=client)
                        el.popups.PopupButton("Toggle darkmode", cb)
                def spinDropDown():
                    dropDown.style(add="transform: rotate(180); transition: 1s;")
                dropDown = ui.icon('expand_more').on("click", (lambda: (spinDropDown(),createPopup()))).style(add="cursor:pointer;").classes(add="backgroundHover")
                # el.titlebar.button(lambda: (print("hi"),popup.show()), "expand_more", transparentBackground=True)
                ui.image(serveFiles.serveFile(pathlib.Path(__file__).parent/'assets'/'minimize_208px.png')).style(add="width: 24px;").on("click", lambda: window.set_minimized(not window.get_minimized())).style(add="cursor:pointer;").classes(add="scaleHover")
                ui.image(serveFiles.serveFile(pathlib.Path(__file__).parent/'assets'/'maximize_208px.png')).style(add="width: 24px;").on("click", lambda: window.set_maximized(not window.get_maximized())).style(add="cursor:pointer;").classes(add="scaleHover")
                ui.image(serveFiles.serveFile(pathlib.Path(__file__).parent/'assets'/'close_208px.png')).style(add=   "width: 24px;").on("click", lambda: asyncronous.killProcess())                       .style(add="cursor:pointer;").classes(add="scaleHover")
                # el.titlebar.button(lambda: window.set_minimized(not window.get_minimized()), "horizontal_rule")
                # el.titlebar.button(lambda: window.set_maximized(not window.get_maximized()), "check_box_outline_blank")
                # el.titlebar.button(lambda: asyncronous.killProcess(), "close")

    nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<div style="height: 32px;"></div>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<p>film</p>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<p>film</p>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<p>film</p>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<p>film</p>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<p>film</p>'))  # It looks like Im having some weird syntax error here
    # nicegui.globals.get_client().content.default_slot.parent.style(add="padding-top: 48px;")
    # for child in nicegui.globals.get_client().content.default_slot.children:
    #     child.style(add="overflow: overlay; ")
    # nicegui.globals.get_client().content.default_slot.children[0].default_slot.children[0].style(add="overflow: none; ")
    # nicegui.globals.get_client().content.default_slot.children[0].style(add="overflow-x: hidden; overflow-y: hidden;")
    # nicegui.globals.get_client().content.default_slot.parent.style(add="overflow-x: hidden; overflow-y: hidden;")
    # nicegui.globals.get_client().content.default_slot.parent.style(add="width: 100%; height: calc(100vh - 100px); display: flex; flex-direction: row; flex-wrap: nowrap;")
    # nicegui.globals.get_client().content.default_slot.parent.parent_slot.parent.style(add="overflow-x: overlay; overflow-y: overlay; ")
    # nicegui.globals.get_client().content.default_slot.parent.parent_slot.parent.parent_slot.parent.style(add="overflow-x: hidden; overflow-y: hidden;")
    # nicegui.globals.get_client().content.default_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.style(add="overflow-x: hidden; overflow-y: hidden;")
    ui.add_head_html('<style>body {overflow: hidden;}</style>')
    # nicegui.globals.get_client().content.default_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.style(add="overflow: none; ")
    # nicegui.globals.get_client().content.default_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.parent_slot.parent.style(add="overflow: none; ")
    
    
    #app > nicegui-layout > q-page-container > q-page
    if window.enable_scrolling: # @note Set styling for whether the page should be scrollable or not.
        ui.html('''<style>
    .desktop { overflow: overlay;}

    </style''' # @note the desktop class is assigned to the body, which is where scrolling happens.
        )
    else:
        pass
        nicegui.globals.get_client().content.default_slot.parent.style(add='width: 100%; height: calc(100vh - 21px); display: flex; flex-direction: row; flex-wrap: nowrap; overflow-x: hidden; overflow-y: hidden; flex-flow: column; align-items: flex-start; align-content: flex-start;')
        # nicegui.globals.get_client().content.default_slot.parent.style(add='width: 100vw; height: 100vh; overflow-x: overlay; overflow-y: overlay; flex-flow: column; align-items: flex-start; align-content: flex-start;')
        # nicegui.globals.get_client().content.default_slot.parent._classes.clear()
        
        # nicegui.globals.get_client().content.default_slot.parent.style(add='background-color: cyan;')
        # nicegui.globals.get_client().content.default_slot.parent.style(replace='overflow: hide; display: flex; padding: 0; margin: 0; max-height: 100vh; max-width: 100vw;')
        # nicegui.globals.get_client().content.default_slot.parent._classes.clear()
        # for element in ['nicegui-layout', 'q-page-container', 'q-page', 'desktop']:
        #     ui.html(f'''<style>
        # .{element} {{ overflow: hidden; max-height: 100vh; max-width: 100vw; display: flex; flex-direction: column; align-items:start;}}
            

        # </style''' # @note the desktop class is assigned to the body, which is where scrolling happens.
        # ) # Other rules that proved unnecessary height: 100vh; width: 100vw; display: flex;


    # nicegui.globals.get_client().content.default_slot.children.insert(0, ui.html('<a> class="anchor"></a>'))  # It looks like Im having some weird syntax error here
    # but interestingly, its the extra > bracket that allows the page content offset to adapt to the height of position: fixed elements.
    # nicegui.globals.get_client().content.default_slot.parent._style.clear()
    # ##nicegui.globals.get_client().content.default_slot.parent.style(add="display: block; overflow: hidden; height:100vh;")
    # nicegui.globals.get_client().content.default_slot.parent.style(add="align-items: start; justify-content: start; display: block; overflow: hidden; height:100vh;")

    # nicegui.globals.get_client().content.default_slot.parent.style(replace="""display: flex;flex-direction: column;overflow: hidden;""")  # /*height:100vh;*/
    # nicegui.globals.get_client().content.default_slot.parent.style(add="""overflow: hidden; overflow-wrap: break-word; overscroll-behavior-block: none; height:100vh; display:block;""")  # /*height:100vh;*/

    # nicegui.globals.get_client().content.default_slot.children.insert(0, titlebar)


def applyNiceguiUniversalStyling():
    from nicegui import ui
    ui.card().style(add='background-color:var(--neutral); top:0; left:0; right:0; bottom:0; position:fixed; z-index:-1000;')
    js = '''
//js
    function calcRectArea(width, height) {
    return width * height;
    }

    console.log(calcRectArea(5, 6));
;//
    '''



    
    ui.add_body_html(r'''
<!-- 
<script src="https://cdnjs.cloudflare.com/ajax/libs/darkreader/4.9.58/darkreader.js"
    integrity="sha512-SVegqt9Q4E2cRDZ5alp9NLqLLJEAh6Ske9I/iU37Jiq0fHSFbkIsIbaIGYPcadf1JBLzdxPrkqfH1cpTuBQJvw=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<div onclick="toggleDarkReader()" style="position:fixed; bottom:0; right:0; z-index: 10000;">ToggleDarkReader</div>
<script> // @note DARK READER
    let _darkReaderEnabled = false;
    function toggleDarkReader() {
        _darkReaderEnabled = !_darkReaderEnabled
        if (_darkReaderEnabled) {
            // DarkReader.enable({
            //     brightness: 250,
            //     contrast:  120,
            //     sepia: 5
            // });
            // DarkReader.enable({
            //     brightness: 430,
            //     contrast:  570,
            //     sepia: 95
            // });
            // DarkReader.enable({
            //     brightness: 80,
            //     contrast: 90,
            //     sepia: 0
            // });
            // DarkReader.enable({
            //     brightness: 150,
            //     contrast: 90,
            //     sepia: -30
            // });
            DarkReader.enable({
                brightness: 190,
                contrast: 90,
                sepia: -40
            });
        } else {
            DarkReader.disable();
        }
    }
    // DarkReader.disable();

    // Enable when the system color scheme is dark.
    // DarkReader.auto({
    //     brightness: 100,
    //     contrast: 90,
    //     sepia: 10
    // });

    // Stop watching for the system color scheme.
    // DarkReader.auto(false);

    // Get the generated CSS of Dark Reader returned as a string.
    // const CSS = await DarkReader.exportGeneratedCSS();

    // Check if Dark Reader is enabled.

    const isEnabled = DarkReader.isEnabled();
    console.log(`darkReader: ${isEnabled}`)
// @note DARK READER END</script>


-->







    <!-- <div onclick="toggleDarkMode()" style="position:fixed; bottom:0; right:0; z-index: 10000;">ToggleDarkMode</div> -->
<!-- 
<script>
    function colorToRgb(color, asArray = true) {
        _colorFetchHelperElement = document.createElement("div")
        _colorFetchHelperElement.style.width = "0px"
        _colorFetchHelperElement.style.height = "0px"
        document.body.appendChild(_colorFetchHelperElement)


        _colorFetchHelperElement.style.backgroundColor = color;
        const computedStyle = window.getComputedStyle(_colorFetchHelperElement)
        const colorAsRgb = color.includes("rgb") ? color : computedStyle.backgroundColor
        _colorFetchHelperElement.remove()
        if(asArray){
            let array = colorAsRgb.match(/[\d\.]+/g).map(Number)
            // if (array[3] == undefined) {
            // array[3] = computedStyle.opacity ? computedStyle.opacity : 0;
            // array[3] = computedStyle.opacity;
            // }
            return array
        }
        return colorAsRgb
        // return asArray ? colorAsRgb.match(/\d+/g).map(Number) : colorAsRgb
    }
    let _darkModeEnabled = false;
    function toggleDarkMode() {
        _darkModeEnabled = !_darkModeEnabled;
        const elements = document.getElementsByTagName("*");

        for (let i = 0; i < elements.length; i++) {
            const element = elements[i]
            let originalOpacity = element.style.opacity
            const colorStyles = ["color", "backgroundColor"]
            for (let colI = 0; colI < colorStyles.length; colI++) {
                const colorStyle = colorStyles[colI]
                const useRgba = element.style[colorStyle].includes('rgba')
                const setColor = element.style[colorStyle].includes('rgb')

                // const originalColorAsRgb = element.style[colorStyle].match(/[\d\.]+/g).map(Number)
                const originalColorAsRgb = colorToRgb(element.style[colorStyle])
                // console.log(`id: ${element.id} colorStyle: ${colorStyle} originalColorAsRgb: ${originalColorAsRgb} tran: ${originalColorAsRgb[3]}`)
                const originalColorAsRgb0to1 = [originalColorAsRgb[0] / 255, originalColorAsRgb[1] / 255, originalColorAsRgb[2] / 255]

                const saturation = (Math.max(Math.max(Math.abs(originalColorAsRgb[0] - originalColorAsRgb[1]), Math.abs(originalColorAsRgb[0] - originalColorAsRgb[2])), Math.abs(originalColorAsRgb[1] - originalColorAsRgb[2]))) / 255
                const lowestValue = Math.min(originalColorAsRgb[0], originalColorAsRgb[1], originalColorAsRgb[2])
                const average = arr => arr.reduce((p, c) => p + c, 0) / arr.length;
                const averageValue = average([Math.max(originalColorAsRgb0to1[0],originalColorAsRgb0to1[1], originalColorAsRgb0to1[2]), lowestValue/255])
                if (true) {
                    // if (saturation < 0.1) {
                    // @note Reduce by amount
                    // let darkMode = true
                    // let maxColorReductionAmount = 0.3 // 0-1 range
                    // let lowestPossibleValue = 0.08    // 0-1 range
                    // let reductionAmountFinal = min(lowestValue, maxColorReductionAmount)-lowestPossibleValue

                    // let colorFinal = [originalColorAsRgb[0]-reductionAmountFinal, originalColorAsRgb[1]-reductionAmountFinal, originalColorAsRgb[2]-reductionAmountFinal]

                    // element.style[colorStyle] = colorFinal;
                    const originalColor0to1Inverted = [originalColorAsRgb0to1[0] * -1 + 1, originalColorAsRgb0to1[1] * -1 + 1, originalColorAsRgb0to1[2] * -1 + 1]
                    const averageValueInverted = averageValue * -1 + 1

                    let colorFinal = [(originalColor0to1Inverted[0] - averageValueInverted) * -1 + averageValueInverted, (originalColor0to1Inverted[1] - averageValueInverted) * -1 + averageValueInverted, (originalColor0to1Inverted[2] - averageValueInverted) * -1 + averageValueInverted]
                    let colorFinalAsStr = undefined
                    if (useRgba) {
                        const rgbaString = element.style[colorStyle]; // Example RGBA string
                        const numbersArray = rgbaString.match(/[\d\.]+/g);
                        const lastDigit = numbersArray.pop();
                        colorFinalAsStr = `rgba(${colorFinal[0] * 255}, ${colorFinal[1] * 255}, ${colorFinal[2] * 255}, ${lastDigit})`

                    } else{
                        colorFinalAsStr = `rgb(${colorFinal[0] * 255}, ${colorFinal[1] * 255}, ${colorFinal[2] * 255})`
                    }
                    // let colorFinalAsStr = element.opacity === undefined ? `rgb(${colorFinal[0] * 255}, ${colorFinal[1] * 255}, ${colorFinal[2] * 255})` : `rgba(${colorFinal[0] * 255}, ${colorFinal[1] * 255}, ${colorFinal[2] * 255}, ${element.opacity})`
                    console.log(`id: ${element.id} colorStyle ${colorStyle} colorFinalAsStr: ${colorFinalAsStr} originalOpacity ${originalOpacity} setColor ${setColor} original: ${element.style[colorStyle]}`)
                    if (setColor) {
                        element.style[colorStyle] = colorFinalAsStr
                    }
                    // element.style[colorStyle] = originalColorAsRgb

                    element.style.cssText = element.style.cssText.replaceAll(_darkModeEnabled ?'white' : 'black', _darkModeEnabled ?'black' : 'white');
                }
                // eval(`element.style.${colorStyle} = "red";`)
                // element.style.backgroundColor = "red";
                // element.style.color = "red";
            // element.style.opacity = originalOpacity;
            }
        }
    }
</script>

-->




<script>
var cursorX = 0;
var cursorY = 0;
var mouseDown = false;
document.body.onmousedown = function() { 
    mouseDown = true;
}
document.body.onmouseup = function() {
    mouseDown = false;
}


document.addEventListener('mousemove', onMouseMove, false)

function onMouseMove(e){
    cursorX = e.clientX;
    document.documentElement.style.setProperty('--cursorX', cursorX);
    cursorY = e.clientY;
    document.documentElement.style.setProperty('--cursorY', cursorY);
}

function getMouseX() {
    return cursorX;
}

function getMouseY() {
    return cursorY;
}
</script>
''')
# .nicegui-content {width: 100%; height: calc(100vh - 100px); display: flex; flex-direction: row; flex-wrap: nowrap;}
    ui.html('''
<!-- html-->
<style> 



/*Scrollbar customization*/

/*
* {
 overflow: overlay; 
}
*/ 
::-webkit-scrollbar-corner {
  background-color: transparent;
}


/* total width */
::-webkit-scrollbar {
  width: 11px;
  height: 11px;
  background-color: transparent;
}

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 14px 14px transparent;
  border: solid 4px transparent;
}

::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 14px 14px #bbbbbe;
  border: solid 4px transparent;
  border-radius: 14px;
  background-color: transparent;
}

::-webkit-scrollbar-thumb:hover {
  background-color: transparent;
}

/* set button(top and bottom of the scrollbar) */
::-webkit-scrollbar-button {
  display: none;
}
</style>
<!--!html-->
''')
#     ui.html('''
# <!- -html-->
# <style> /*Scrollbar customization*/

# /* total width */
# ::-webkit-scrollbar {
#   width: 11px;
#   height: 11px;
#   background-color: transparent;
# }

# ::-webkit-scrollbar-track {
#   box-shadow: inset 0 0 14px 14px transparent;
#   border: solid 4px transparent;
# }

# ::-webkit-scrollbar-thumb {
#   box-shadow: inset 0 0 14px 14px #bbbbbe;
#   border: solid 4px transparent;
#   border-radius: 14px;
# }S

# /* set button(top and bottom of the scrollbar) */
# ::-webkit-scrollbar-button {
#   display: none;
# }
# </style>
# <!--!html-->
# ''')

serveFiles.addJsToDom(pathlib.Path(__file__).parent/'fastJs'/'index.js')

window: Window = None
"Instanciating Window sets this variable to the window."
class Window():  # Base class outlining API interface
    """Wishlist: Make this runnable without blocking the main thread. Feels a little ridiculous to be blocking it just to let the OS host the window.
    Currently thinking that I might be able to use fifo pipes instead of sockets to implement this, I would want to build an abstraction layer for fifo first then."""
    def __init__(self, adress: str = "0.0.0.0", port: int = 80, title: str = None, iconPath=None,
                 show_title_bar: bool = False, height= 500, width= 1000, commsPort=0, reloadOnChange=True, reloadOnChangePath: str = sys.argv[0], reloadOnChangeRestartWindow=True, hideNativeTitlebar=True, enableScrolling = False, darkMode=True):
       
        
        global window
        window = self
        # def bgFixCb():
        #     window = self
            
        #     from toga_winforms.libs import Drawing2D, Color
        #     from toga_winforms.libs import winforms
        #     bgColorRgb = color.hexToRgb(colors.colors.pageBackground)
        #     bgColorWin32 = Color.FromArgb(bgColorRgb[0],bgColorRgb[1],bgColorRgb[2])
            # print(window.togaWindow._impl.native.get_Controls()[0].__dir__())
            # window.togaWindow._impl.native.get_Controls()[0].set_DefaultBackgroundColor(window.togaWindow._impl.native.get_Controls()[0].DefaultBackgroundColor.Red)
            # window.togaWindow._impl.native.get_Controls()[0].DefaultBackgroundColor = bgColorWin32
        #     window.togaWindow._impl.native.get_Controls()[0].set_BackColor(Color.Red)
        #     window.togaWindow._impl.native.get_Controls()[0].set_ForeColor(Color.Red)
        
        # ui.button("BgFix", on_click=bgFixCb)
        
        
        
        
        
        
        
        
        self.enable_scrolling = enableScrolling
        if not title:
            title = data.appName
        if not iconPath:
            iconPath = data.appIcon
        # adress = adress.replace('http://', '').replace('https://', '')
        iconPath = str(iconPath)
        self.adress = adress
        self.port = port
        self.title = title
        self.show_title_bar = show_title_bar
        # print("window")
        adressFormatted = f"http://{adress}:{port}"
        # mainLoop(adressFormatted)

        import nicegui
        applyNiceguiUniversalStyling()
        applyNiceguiDesktopSpecificStyling(self)
        def startNiceguiServer():
            asyncronous.runAsync(lambda: nicegui.ui.run(reload=False, port=port,
                                host=adress, show=False), useThreading=True) 
            from . import colors
            colors.colors.setDarkMode(darkMode)
        portOccupied = True
        tries = 0
        while portOccupied and tries < 30:
            if not networking.isPortOpen(adress, port):
                startNiceguiServer()  
                portOccupied=False
            else:
                time.sleep(0.1)            
                   
            tries += 1  
                  
    


        startWindow = not "reload" in sys.argv[1:] or reloadOnChangeRestartWindow
        # print("startWindow", startWindow)
        togaApp = TogaApp(title, string.PascalCaseTo_snake_case(
            f"org.{data.publishers[0]}.{title}".replace(' ', '')), icon=iconPath)
        togaApp.hideNativeTitlebar = hideNativeTitlebar
        togaApp.url = adressFormatted.replace("0.0.0.0", "localhost")
        # togaApp.icon = iconPath
        # devTools.reloadOnChange(
        #     watchDir=True, cb=[nicegui.app.shutdown],
        #     blocking=not startWindow, paths=reloadOnChangePath)
        # print("foo")

        # import pickle
        # import tempfile
        def restartWindow():
            try:
                self.togaApp.exit()
            except:
                pass
        if reloadOnChange:
            devTools.reloadOnChange(
                watchDir=True, cb=[nicegui.app.shutdown, restartWindow if reloadOnChangeRestartWindow else lambda: None],
                blocking=False, parametersCb=lambda: f'windowDimensions=[{self.get_width()}, {self.get_height()}]')   
        # print("bar")
        # f = tempfile.NamedTemporaryFile()
        # windowRefFile = pathlib.Path((tempfile.gettempdir().replace('\\', '/')+'/'+"fastWindowRef.pickle").replace('//', '/')).open("w+")
        # globals()['window'] = self
        if startWindow:
            self.togaApp = togaApp
            def setWidthHeight():
                time.sleep(2)
                print("run!")
                self.set_height(height)
                self.set_width(width)
            # togaApp._impl.interface.main_window._impl.native.Load.__iadd__(setWidthHeight)
            # asyncronous.runAsync(setWidthHeight)
            # dump = pickle.dump(togaApp, windowRefFile)
            togaApp.main_loop()

        else:
            # windowRefFile
            # self.togaApp = pickle.load(windowRefFile.read())
            while True:
                time.sleep(100000)
        # print("yo")

        # else:
        # multiprocessing.Process(target=mainLoop, args=(adressFormatted,), daemon=True).start()
        # asyncronous.runAsync(lambda: self._togaApp.main_loop())

    @property
    def togaWindow(self) -> toga.Window:
        return self.togaApp.main_window

    def close(self):
        pass

    def open(self, ):
        pass

    def get_maximized(self):
        return True if self.togaApp.main_window._impl.native.WindowState == self.togaApp.main_window._impl.native.WindowState.Maximized else False

    def set_maximized(self, value=True):
        self.togaApp.main_window._impl.native.set_WindowState(self.togaApp.main_window._impl.native.WindowState.Maximized if value else self.togaApp.main_window._impl.native.WindowState.Normal)
        return self.get_maximized()
    # @property
    # def maximize(self, value=None):
    #     if value != None:
    #         self.togaApp.main_window._impl.native.WindowState = self.togaApp.main_window._impl.native.WindowState.Maximized if value else self.togaApp.main_window._impl.native.WindowState.Normal
    #     return True if self.togaApp.main_window._impl.native.WindowState == self.togaApp.main_window._impl.native.WindowState.Maximized else False

    # def unmaximize(self):
    #     from toga_winforms.libs import WinForms
    #     self.togaApp.main_window._impl.native.WindowState = self.togaApp.main_window._impl.native.WindowState.Maximized

    # @property
    # def minimize(self, value=None):
    #     # window: toga.Window = self.togaApp.main_window
    #     # window.hide()
    #     if value != None:
    #         self.togaApp.main_window._impl.native.WindowState = self.togaApp.main_window._impl.native.WindowState.Minimized if value else self.togaApp.main_window._impl.native.WindowState.Normal
    #     return True if self.togaApp.main_window._impl.native.WindowState == self.togaApp.main_window._impl.native.WindowState.Minimized else False

    def set_minimized(self, value=True):
        self.togaApp.main_window._impl.native.set_WindowState(self.togaApp.main_window._impl.native.WindowState.Minimized if value else self.togaApp.main_window._impl.native.WindowState.Normal)
        return self.get_minimized

    def get_minimized(self, value=None):
        return True if self.togaApp.main_window._impl.native.WindowState == self.togaApp.main_window._impl.native.WindowState.Minimized else False


    # def unminimize(self, ):
    #     pass

    def expand(self, ):
        "Fit screen"

    def unexpand(self, ):
        pass

    def refresh(self, ):
        "Kind of like hitting the reload btn in a real webbrowser"

    def move(self, x, y):
        pos = self.get_position()
        newPos = [pos[0]+x, pos[1]+y]
        # print(newPos)
        self.set_position(*newPos)

    is_following_mouse = False

    # async def test(self):
    #     print("AsyncHelloWorld")
    #     return "AsyncHelloWorld"
    async def get_lmb(self) -> bool:
        """Get mouse position in pixels where bottom left is [0,0] and top right is [windowWidth, windowHeight]

        @todo invert the y value according to this description."""
        returnVal = await nicegui.globals.get_client().run_javascript('mouseDown')
        return returnVal

    async def get_mouse_pos(self) -> list[int]:
        """Get mouse position in pixels where bottom left is [0,0] and top right is [windowWidth, windowHeight]

        @todo invert the y value according to this description."""
        returnVal = await nicegui.globals.get_client().run_javascript('[cursorX, cursorY]')
        return returnVal
    nicegui.ui.label
    __disable_user_select_html_element__ = None
    is_following_mouse = False
    async def follow_mouse_begin(self, foo=None):
        # import ctypes
        # import win32gui
        # user32=ctypes.WinDLL("user32.dll")
        # hwnd = self.togaApp.main_window._impl.native.Handle
        # hwndInt = int(str(hwnd))
        # # win32gui.ReleaseCapture()
        # import win32con
        # HT_CAPTION  = 0x2
        # win32gui.ReleaseCapture()
        # import inspect

        # print(f"argspec: {self.togaApp.main_window._impl.native.RaiseDragEvent.__dir__()}")
        # inspect.getargspec(f"argspec: {self.togaApp.main_window._impl.native.RaiseDragEvent}")
        # self.togaApp.main_window._impl.native.RaiseDragEvent.__code__
        # win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONDOWN, HT_CAPTION, 0)
        # win32gui.SendMessage(hwndInt, win32con.WM_NCLBUTTONDOWN, 2, 30934655)
        # while self.is_following_mouse:
        #     win32gui.SendMessage(hwndInt, 534, 9, 0)
        # win32gui.SendMessage(hwndInt, 0x112, 0xf012, 0)
        # print("bgn")
        
        # return
        async def follow_mouse_begin_inner(foo=None):
            # print("follow_mouse_begin")
            try:
                import win32api
                useWin32api = True
            except:
                useWin32api = False

            async def getMousePos():
                import win32api
                x, y = win32api.GetCursorPos()
                if useWin32api:
                    return [x,y]
                else:
                    return await self.get_mouse_pos()
            self.__disable_user_select_html_element__ = ui.html("<style>* {user-select: none; }</style")

            from nicegui import events
            if not self.is_following_mouse:
                self.is_following_mouse = True

                # def update_pos():
                mousePosPrevious = await getMousePos()
                mousePosOriginal = mousePosPrevious
                windowPosOriginal = self.get_position()
                # mousePosOriginalRelationToWindowPos
                mouseOffsetFromOriginalPrevious = [[0, 0]]
                while (self.is_following_mouse):
                    if not await self.get_lmb():
                        break
                    await asyncio.sleep(1/240)
                    mousePos = await getMousePos()
                    windowPos = self.get_position()
                    if useWin32api:
                        self.set_position(int(windowPosOriginal[0]-mousePosOriginal[0]+mousePos[0]),
                                        int(windowPosOriginal[1]-mousePosOriginal[1]+mousePos[1]))
                        continue
                    else:
                        # print(f"mousePos: {mousePos}    windowPos: {windowPos}")
                        # # print(mousePos)
                        # mouseDelta = [mousePos[0]-mousePosPrevious[0], mousePos[1]-mousePosPrevious[1]]
                        # self.move(mouseDelta[0], mouseDelta[1])

                        mouseOffsetFromOriginal = [mousePos[0]-mousePosOriginal[0], mousePos[1]-mousePosOriginal[1]]
                        if mouseOffsetFromOriginalPrevious[-1] == mouseOffsetFromOriginal:
                            continue
                        else:
                            mouseOffsetFromOriginalPrevious.append(mouseOffsetFromOriginal)
                            while mouseOffsetFromOriginalPrevious.__len__() > 2:
                                mouseOffsetFromOriginalPrevious.pop(0)
                            xyAvg = [0, 0]
                            i = 0
                            for xy in mouseOffsetFromOriginalPrevious:
                                i += 1
                                # print(type(xy))
                                xyAvg[0] = xyAvg[0]+xy[0]
                                xyAvg[1] = xyAvg[1]+xy[1]
                            xyAvg[0] = round(xy[0]/i)
                            xyAvg[1] = round(xy[1]/i)

                            # self.set_position(-windowPosOriginal[0]-mousePosOriginal[0]+mousePos[0]+windowPos[0], -windowPosOriginal[1]-mousePosOriginal[1]+mousePos[1]+windowPos[1])
                        self.set_position(int(xyAvg[0]+windowPos[0]),
                                        int(xyAvg[1]+windowPos[1]))

                    # mouseOffsetFromOriginalPrevious = mouseOffsetFromOriginal.copy()
                    # self.set_position(windowPosOriginal[0]+mousePos[0]-mousePosOriginal[0], windowPosOriginal[1]+mousePos[1]-mousePosOriginal[1])

                    # mousePosPrevious = await self.get_mouse_pos()

                    # print(mouse_event_argument)
                    # nicegui.globals.get_client().content.default_slot.parent._event_listeners.remove(update_pos)
                # nicegui.globals.get_client().content.default_slot.parent.on("mousemove", update_pos, throttle=0.5)
            # print(f"currentMouseX {asyncronous.runSync(self.test())}")
            # print(await self.get_mouse_pos())
            # print(f"""js return: {await nicegui.globals.get_client().run_javascript('cursorX', timeout=1.5)}""")
            # print(f"""js return: {await nicegui.globals.get_client().run_javascript('cursorY', timeout=1.5)}""")
            # print(f"""currentMouseX {asyncronous.runSync(nicegui.globals.get_client().run_javascript('alert("Hello!")', timeout=5))}""")
        try:
            await follow_mouse_begin_inner()
        except Exception as exc:
            print(f"exc {exc}")
        # self.togaApp.add_background_task(follow_mouse_begin_inner)

    def follow_mouse_end(self):
        self.is_following_mouse = False
        self.__disable_user_select_html_element__.content = ""

    def set_position(self, x, y, in_pixels=True):
        # print(f"newPos: {[x,y]}")
        self.togaWindow.position = [x, y]

    def get_position(self, in_pixels=True) -> list[float, float]:
        returnVal = self.togaWindow.position
        # returnVal = [int(returnVal[0]), int(returnVal[1])]
        return returnVal

    def set_width(self, x, in_pixels=True):
        self.togaWindow.size = [self.togaWindow.size[0]+x, self.togaWindow.size[1]]

    def get_width(self, in_pixels=True) -> float:
        self.togaWindow.size[0]

    def set_height(self, y, in_pixels=True):
        self.togaWindow.size = [self.togaWindow.size[0], self.togaWindow.size[1]+y]

    def get_height(self, in_pixels=True) -> float:
        self.togaWindow.size[1]

    def go_to_previous_page(self, ) -> bool:
        pass

    def go_to_next_page(self, ) -> bool:
        pass
