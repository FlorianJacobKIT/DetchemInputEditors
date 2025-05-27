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

    box: tk.Listbox

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

        self.center()

    def info(self,event: tk.Event):
        print(event.state)
        print(event.type)
        print(event.widget)
        print(event.num)

    def move_selection(self, event: tk.Event, delta: int):
        cur = self.box.curselection()[0] + delta
        cur = max(0, cur)
        if 0 <= cur < self.box.size():
            event.widget.selection_clear(0, tk.END)
            event.widget.select_set(cur)

    def focus_selection(self, event: tk.Event):
        if not self.box.curselection():
            event.widget.select_set(0)


    def load_element_display(self):
        self.box = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 16))
        self.box.bind('<Up>', lambda e:self.move_selection(e,-1))
        self.box.bind('<Down>',lambda e: self.move_selection(e,1))
        self.box.bind('<Return>', lambda event: self.open_data())
        self.box.bind('<Double-1>', lambda event: self.open_data())
        self.box.bind('<FocusIn>', self.focus_selection)
        self.box.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW, padx=10)
        self.update_selection()


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

    def open_data(self):
        selected = self.box.curselection()[0]
        selected_str: str = self.box.get(selected)
        displayer = SpeciesDisplay(self, selected_str.split("\t")[1])
        displayer.show()
        if len(self.children) != 0:
            self.update_selection()
        self.box.selection_clear(0, tk.END)
        self.box.select_set(selected)
        self.box.activate(selected)
        self.box.see(selected)

    def update_selection(self):
        data = global_vars.chemData
        selection = global_vars.selected_data
        self.box.delete(0, tk.END)
        for spec, info in data.items():
            color = "black"
            if spec not in selection:
                spec_string = "□\t"
            else:
                select = selection[spec]
                if select == (None, None):
                    spec_string = "☐\t"
                elif select[0] is None:
                    spec_string = "🌡\t"
                    color = "red"
                elif select[1] is None:
                    spec_string = "〰\t"
                    color = "blue"
                else:
                    spec_string = "✓\t"
                    color = "green"
            self.box.insert(tk.END, spec_string + spec)
            self.box.itemconfig(tk.END, foreground=color)




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
