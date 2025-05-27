import math
import os
import tkinter as tk
from tkinter import messagebox, filedialog

from ChemDataManager import global_vars, ReadData, SourceFormat, ReadExternalFile
from ChemDataManager.GUIs import SourceEditor
from ChemDataManager.GUIs.SourceDataDisplayer import SourceDisplay
from ChemDataManager.GUIs.SourceEditor import SourceDataDisplayer
from ChemDataManager.GUIs.SpeciesDataDisplayer import SpeciesDisplay
from GeneralUtil import TextModifiers, SelectionDialog
from GeneralUtil.CenterGui import CenterRootWindow


class ListGui(CenterRootWindow):

    check_btn: dict[str,tk.Checkbutton] = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.grid_columnconfigure(4,weight=1)
        title = tk.Label(self, text="Chemical Data Manager", font=("Arial", 20))
        title.grid(row=0, column=0, columnspan = 6, sticky=tk.NSEW, padx=5, pady=5)
        data = ReadData.readChemData()
        lib_data = ReadData.readLibData()
        global_vars.chemData = data
        global_vars.libData = lib_data

        global_vars.selected_data = {}
        for spec, info in data.items():
            global_vars.selected_data[spec] = (None, None)
        self.load_element_display()

        export_button = tk.Button(self,text="Import File", font=("Arial", 12), command=lambda :self.import_file())
        export_button.grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        export_button = tk.Button(self,text="Export Simulation Files", font=("Arial", 12), command=lambda :messagebox.showinfo("WIP", "This feature is not implemented yet."))
        export_button.grid(row=2, column=1, sticky=tk.NW, padx=5, pady=5)
        upload_button = tk.Button(self,text="Save Locally", font=("Arial", 12), command=lambda :self.save_locally())
        upload_button.grid(row=2, column=2, sticky=tk.NW, padx=5, pady=5)
        upload_button = tk.Button(self,text="Upload Changes", font=("Arial", 12), command=lambda :messagebox.showinfo("WIP", "This feature is not implemented yet."))
        upload_button.grid(row=2, column=3, sticky=tk.NW, padx=5, pady=5)

        close_button = tk.Button(self,text="Close", font=("Arial", 12), width=10, command=lambda :self.destroy())
        close_button.grid(row=2, column=5, sticky=tk.NSEW, padx=5, pady=5)

    def load_element_display(self):
        dist = int(math.floor(math.sqrt(len(global_vars.chemData))))
        dataFrame = tk.Frame(self, borderwidth=5, relief=tk.RAISED, padx=5, pady=5)
        i: int = 0
        self.check_btn = dict()
        for spec, info in global_vars.chemData.items():
            spec_frame = tk.Frame(dataFrame)
            spec_frame.grid_columnconfigure(1, weight=1)
            check = tk.Checkbutton(spec_frame, state=tk.DISABLED)
            self.check_btn[spec] = check
            check.grid(row=0, column=0)
            label = tk.Button(spec_frame, text=spec, command=lambda s=spec: self.open_data(s))
            label.grid(row=0, column=1, sticky=tk.NSEW)
            spec_frame.grid(column=i // dist, row=i % dist, sticky=tk.NSEW, padx=1, pady=1)
            i -= - 1
        dataFrame.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW, padx=10)
        self.update_selection()
        self.center()

    def import_file(self):
        answer = SelectionDialog.GeneralDialog("Choose type of import file:", ["thermdata", "moldata"]).center().show()
        if answer == "":
            return

        dir_name = filedialog.askopenfilename()
        if dir_name == "":
            return

        display = SourceDisplay(self)
        display.show()
        id = display.selected_id

        if answer == "thermdata":
            answer = ReadExternalFile.read_thermdata(dir_name,id)
            if answer>=0:
                messagebox.showinfo("Thermal Data Imported", "Thermal Data >" + dir_name + "< successfully Imported")
        if answer == "moldata":
            answer = ReadExternalFile.read_moldata(dir_name,id)
            if answer >= 0:
                messagebox.showinfo("Molecular Data Imported", "Molecular Data >" + dir_name + "< successfully Imported")
        self.load_element_display()


    def save_locally(self):
        ReadData.writeChemData(global_vars.chemData)
        ReadData.writeLibData(global_vars.libData)

    def open_data(self, speciesName):
        displayer = SpeciesDisplay(self, speciesName)
        displayer.show()
        if len(self.children) != 0:
            self.update_selection()

    def update_selection(self):
        data = global_vars.chemData
        selection = global_vars.selected_data
        for spec, info in data.items():
            if spec not in selection:
                self.check_btn[spec].deselect()
                continue
            select = selection[spec]
            if select == (None, None):
                self.check_btn[spec].deselect()
                continue
            if select[0] is None:
                self.check_btn[spec].select()
                self.check_btn[spec].configure(disabledforeground="blue")
                continue
            if select[1] is None:
                self.check_btn[spec].select()
                self.check_btn[spec].configure(disabledforeground="red")
                continue
            self.check_btn[spec].select()
            self.check_btn[spec].configure(disabledforeground="green")




    def show(self):
        self.wm_deiconify()
        self.wait_window()



gui = ListGui(None)
gui.focus_set()
gui.title("Reaction Gui")
gui.lift()
gui.attributes('-topmost', True)
gui.attributes('-topmost', False)
gui.update()
gui.center()
gui.show()
