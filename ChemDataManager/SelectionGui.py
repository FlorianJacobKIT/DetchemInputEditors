import math
import tkinter as tk
from tkinter import messagebox

from ChemDataManager import global_vars, ReadData
from ChemDataManager.SpeciesDataDisplayer import SpeciesDisplay
from GeneralUtil.CenterGui import CenterRootWindow


class ListGui(CenterRootWindow):

    def __init__(self, parent):
        super().__init__(parent)
        title = tk.Label(self, text="Chemical Data Manager", font=("Arial", 20))
        title.grid(row=0, column=0, columnspan = 4, sticky=tk.NSEW, padx=5, pady=5)
        data = ReadData.readChemData()
        lib_data = ReadData.readLibData()
        global_vars.chemData = data
        global_vars.libData = lib_data
        dist = int(math.floor(math.sqrt(len(data))))
        dataFrame = tk.Frame(self)
        i: int = 0
        for spec, info in data.items():
            spec_frame = tk.Frame(dataFrame)
            spec_frame.grid_columnconfigure(1, weight=1)
            check = tk.Checkbutton(spec_frame)
            check.grid(row=0, column=0)
            label = tk.Button(spec_frame, text=spec, command=lambda s=spec: self.open_data(s))
            label.grid(row=0, column=1, sticky=tk.NSEW)
            spec_frame.grid(column=i//dist, row=i%dist, sticky=tk.NSEW, padx=1, pady=1)
            i -=- 1
        dataFrame.grid(row=1, column=0, columnspan = 4,sticky=tk.NSEW, padx=10)

        export_button = tk.Button(self,text="Export Simulation Files", command=lambda :messagebox.showinfo("WIP", "This feature is not implemented yet."))
        export_button.grid(row=2, column=0, sticky=tk.NSEW, padx=5, pady=5)
        upload_button = tk.Button(self,text="Upload Changes", command=lambda :messagebox.showinfo("WIP", "This feature is not implemented yet."))
        upload_button.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

        close_button = tk.Button(self,text="Close", command=lambda :messagebox.showinfo("WIP", "This feature is not implemented yet."))
        close_button.grid(row=2, column=3, sticky=tk.NSEW, padx=5, pady=5)

    def open_data(self, speciesName):
        displayer = SpeciesDisplay(self, speciesName)
        displayer.show()


    def show(self):
        self.wm_deiconify()
        self.wait_window()



gui = ListGui(None)
gui.focus_set()
gui.title("Reaction Gui")
gui.lift()
gui.attributes('-topmost', True)
gui.attributes('-topmost', False)
gui.center()
gui.show()
