import math
import tkinter as tk

from GeneralUtil.CenterGui import CenterRootWindow


class GeneralDialog(CenterRootWindow):
    result: str
    buttons: list

    def __init__(self, prompt, answers):
        super().__init__()
        self.result = ""
        self.buttons = list()
        label = tk.Label(self, text=prompt, font=('Arial', 20))
        label.grid(column=0, row=0, columnspan=len(answers), sticky=tk.NSEW)

        height = round(math.sqrt(len(answers)))
        for i in range(len(answers)):
            btn = tk.Button(self, text=answers[i], font=('Arial', 15), command=lambda r=answers[i]: self.on_ok(r))
            self.buttons.append(btn)
            btn.grid(column=i // height, row=i % height + 1, padx=5, pady=5, sticky=tk.NSEW)


    def on_ok(self, answer):
        self.result = answer
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.result
