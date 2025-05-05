import tkinter


class StatusBarWidget(tkinter.Frame):
    def __init__(self, master, width, size=0.):
        tkinter.Frame.__init__(self, master)
        self.width = width - 3
        self.canvas = tkinter.Canvas(self, height=13, width=width)
        self.canvas.grid(sticky=tkinter.NSEW)
        self.set_size(size)

    def set_size(self, size):
        for ID in self.canvas.find_all():
            self.canvas.delete(ID)
        self.canvas.create_rectangle(2, 2, self.width + 2, 14,
                                     outline="black")
        if size > 1.: size = 1.
        if size < -1.: size = -1.
        if size != 0.:
            w = self.canvas.create_rectangle(self.width//2 + 3, 3, self.width//2 + int(self.width/2 * size) + 3, 14,
                                             fill=self.color(size), width=0)
        self.canvas.create_line(self.width//2 + 2, 1, self.width//2 + 2, 14, width=1, fill="black")


    def color(self, size):
        size = abs(size)
        r = min((255, int(500 * size)))
        g = max((0, min((255, int(400 * (1 - size))))))
        return "#%2.2x%2.2x%2.2x" % (r, g, 0)