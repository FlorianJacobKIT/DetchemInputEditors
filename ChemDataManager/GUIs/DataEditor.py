from ChemDataManager import global_vars
from ChemDataManager.ChemDataFormat import ChemData
from GeneralUtil.CenterGui import CenterWindow
import tkinter as tk


class MolDataDisplayer(CenterWindow):

    variables: list = []

    def __init__(self, master, chem_data: ChemData):
        super().__init__(master)
        self.chem_data = chem_data
        source = global_vars.libData[self.chem_data.source]
        self.source = source
        row = 0
        label = tk.Label(self, text="MolData", font=("Arial", 20))
        label.grid(row=row, column=0, columnspan=2)
        row -=- 1
        label = tk.Label(self, text="Source:", anchor=tk.W)
        label.grid(row=row, column=0, sticky=tk.NSEW)
        edit = tk.Button(self, text="Select source", command=lambda:print("Select source"))
        edit.grid(row=row, column=1, sticky=tk.NSEW)
        row -=- 1
        self.add_property(row,"geometry")
        row -= - 1
        self.add_property(row,"molar_mass")
        row -= - 1
        self.add_property(row,"lennard_jones_potential")
        row -= - 1
        self.add_property(row,"lennard_jones_collision")
        row -= - 1
        self.add_property(row,"dipole_moment")
        row -= - 1
        self.add_property(row,"polarizability")
        row -= - 1
        self.add_property(row,"rotational_relaxation_collision_number")
        row -= - 1


    def add_property(self, row, text):
        title = text.split("_")
        for i in range(len(title)):
            title[i] = title[i].capitalize()
        title = " ".join(title)
        title += ": "
        label = tk.Label(self, text=title, anchor=tk.W)
        label.grid(row=row, column=0, sticky=tk.NSEW)
        dict_version = self.chem_data.__dict__
        var = tk.DoubleVar()
        var.set(dict_version[text])
        edit = tk.Entry(self, textvariable=var)
        edit.grid(row=row, column=1, sticky=tk.NSEW)
        def set_value(var,text):
            dict_version = self.chem_data.__dict__
            dict_version[text] = var.get()

        var.trace_add("write", lambda a,b,c,v=var,t=text: set_value(var,t))



class ThermDataDisplayer(CenterWindow):
    def __init__(self, master, chem_data: ChemData):
        super().__init__(master)
        self.chem_data = chem_data
        source = global_vars.libData[self.chem_data.source]
        self.source = source
        label = tk.Label(self.master, text="ThermData")
        label.grid(row=0, column=0)


