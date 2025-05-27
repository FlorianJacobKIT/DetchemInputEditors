import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        l = tk.Text(self, width=5, height=2, borderwidth=0,
                    background=self.cget("background"))
        l.tag_configure("subscript", offset=-4)
        l.insert("insert", "H", "", "2", "subscript", "O", "", "3", "subscript")
        l.configure(state="disabled")
        l.pack(side="top")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()