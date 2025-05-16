from collections.abc import Callable

from ChemDataManager import global_vars
from ChemDataManager.ChemDataFormat import ChemData
from ChemDataManager.GUIs import DataEditor
from GeneralUtil.CenterGui import CenterWindow
import tkinter as tk


class SpeciesDisplay(CenterWindow):

    def __init__(self, parent, species_name):
        super().__init__(parent)
        self.species = global_vars.chemData[species_name]
        row = 0
        column = 0
        title = tk.Label(self, text=species_name, font=("Arial", 20))
        title.grid(row=row, column=0, sticky='nsew')
        row -=- 1


        chemFrame = tk.Frame(self)
        chemFrame.grid(row=row, column=0, sticky='nsew', padx=10, pady=10)
        row -= - 1

        self.load_chem_frame(chemFrame)

        thermFrame = tk.Frame(self)
        thermFrame.grid(row=row, column=0, sticky='nsew', padx=10, pady=10)
        row -= - 1

        chemDataTitle = tk.Label(thermFrame, text="Therm Data", font=("Arial", 16), anchor=tk.W)
        chemDataTitle.grid(row=0, column=0, columnspan = 3, sticky='nsew')

        column = 4
        line = 0
        label = tk.Label(thermFrame, text="State", anchor=tk.W)
        column = self.add_label(column, label, line)
        label = tk.Label(thermFrame, text="Composition", anchor=tk.W)
        column = self.add_label(column, label, line)
        label = tk.Label(thermFrame, text="Graph", anchor=tk.W)
        column = self.add_label(column, label, line)

        divider = tk.Frame(thermFrame, bg="black", height=1)
        divider.grid(row=1, column=0, columnspan=column, sticky='nsew')

        line = 2
        for chemData in self.species[1]:
            column = 0
            source = global_vars.libData[chemData.source]

            checker = tk.Checkbutton(thermFrame)
            column = self.add_label(column, checker, line)

            label = tk.Label(thermFrame, text=str(source.creation_date.year), anchor=tk.W)
            column = self.add_label(column, label, line)
            author = source.author
            if len(source.author) > 20:
                author = source.author[:17] + "..."
            label = tk.Label(thermFrame, text=author, width=16, anchor=tk.W)
            column = self.add_label(column, label, line)

            column -= - 1
            label = tk.Label(thermFrame, text=chemData.state, anchor=tk.W)
            column = self.add_label(column, label, line)
            comp = ""
            for atom,count in chemData.atoms.items():
                comp += atom + ":" + str(count) + ";"
            comp = comp[:-1]
            label = tk.Label(thermFrame, text=comp, anchor=tk.W)
            column = self.add_label(column, label, line)

            show_btn = tk.Button(thermFrame, text="Open Therm Interface")
            show_btn.grid(row=line, column=column, sticky='nsew')


            line -= - 1


        divider = tk.Frame(thermFrame, bg = "black", width=1)
        divider.grid(row=0, column=3, rowspan=line, sticky='nsew')

        self.center()

    def load_chem_frame(self, chemFrame):
        chemDataTitle = tk.Label(chemFrame, text="Chem Data", font=("Arial", 16), anchor=tk.W)
        chemDataTitle.grid(row=0, column=0, columnspan=3, sticky='nsew')
        column = 4
        label = tk.Label(chemFrame, text="geometry", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="molar_mass", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="lj potential", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="lj collision", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="dipole_moment", anchor=tk.E, width=15)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="polarizability", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="rrc number", anchor=tk.E, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="comment_chem", anchor=tk.W)
        column = self.add_label(column, label, 0)
        divider = tk.Frame(chemFrame, bg="black", height=1)
        divider.grid(row=1, column=0, columnspan=column, sticky='nsew')
        line = 2
        def open_editor(chem_data):
            DataEditor.MolDataDisplayer(self,chemData).show()
            for child in chemFrame.winfo_children():
                child.destroy()
            self.load_chem_frame(chemFrame)

        for chemData in self.species[0]:
            column = 0
            source = global_vars.libData[chemData.source]

            checker = tk.Checkbutton(chemFrame)
            column = self.add_label(column, checker, line)

            label = tk.Label(chemFrame, text=str(source.creation_date.year), anchor=tk.W)
            column = self.add_label(column, label, line)
            author = source.author
            if len(source.author) > 20:
                author = source.author[:17] + "..."
            label = tk.Label(chemFrame, text=author, width=16, anchor=tk.W)
            column = self.add_label(column, label, line)

            click_effect = lambda e, c=chemData: open_editor(c)

            column -= - 1
            label = tk.Label(chemFrame, text=chemData.geometry, anchor=tk.E)

            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.molar_mass, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.lennard_jones_potential, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.lennard_jones_collision, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.dipole_moment, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.polarizability, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.rotational_relaxation_collision_number, anchor=tk.E)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=chemData.comment_chem, anchor=tk.W)
            column = self.add_label(column, label, line, click_effect)
            line -= - 1
        divider = tk.Frame(chemFrame, bg="black", width=1)
        divider.grid(row=0, column=3, rowspan=line, sticky='nsew')

    def add_label(self, column, label, line, click_effect:Callable=None):
        label.grid(row=line, column=column, sticky='nsew')
        label.bind("<Button-1>", click_effect)
        column -= - 1
        return column
