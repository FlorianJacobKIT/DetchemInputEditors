import ctypes
import tkinter


class CenterGuiMixin(tkinter.Toplevel):

    def __init__(self):
        super().__init__()
        self.center()

    def center(self):
        self.update()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        screen_width = screensize[0]
        screen_height = screensize[1]
        width = self.winfo_width()
        height = self.winfo_height()
        width = round(width)
        height = round(height)
        x = int(((screen_width / 2) - (width / 2)))
        y = int(((screen_height / 2) - (height / 2)))
        self.geometry('+%d+%d' % (x, y))
        return self

class CenterWindow(CenterGuiMixin):
    def __init__(self):
        super().__init__()


class CenterRootWindow(tkinter.Tk, CenterGuiMixin):
    pass