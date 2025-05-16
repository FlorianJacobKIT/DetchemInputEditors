from ChemDataManager import global_vars
from ChemDataManager.ChemDataFormat import ChemData
from GeneralUtil.CenterGui import CenterWindow
import tkinter as tk


class SpeciesDisplay(CenterWindow):

    def __init__(self, parent, species_name):
        super().__init__(parent)
        self.species = global_vars.chemData[species_name]
        row = 0
        title = tk.Label(self, text=species_name, font=("Arial", 20))
        title.grid(row=row, column=0, sticky='nsew')
        row -=- 1

        chemDataTitle = tk.Label(self, text="Chem Data", font=("Arial", 16), anchor=tk.W)
        chemDataTitle.grid(row=row, column=0, sticky='nsew')
        row -= - 1

        chemFrame = tk.Frame(self)
        chemFrame.grid(row=row, column=0, sticky='nsew', padx=10, pady=10)
        row -= - 1

        label = tk.Label(chemFrame, text="geometry", anchor='w', width=10)
        label.grid(row=0, column=3, sticky='nsew')
        label = tk.Label(chemFrame, text="molar_mass", anchor='w', width=10)
        label.grid(row=0, column=4, sticky='nsew')
        label = tk.Label(chemFrame, text="lj potential", anchor='w', width=10)
        label.grid(row=0, column=5, sticky='nsew')
        label = tk.Label(chemFrame, text="lj collision", anchor='w', width=10)
        label.grid(row=0, column=6, sticky='nsew')
        label = tk.Label(chemFrame, text="dipole_moment", anchor='w', width=15)
        label.grid(row=0, column=7, sticky='nsew')
        label = tk.Label(chemFrame, text="polarizability", anchor='w', width=10)
        label.grid(row=0, column=8, sticky='nsew')
        label = tk.Label(chemFrame, text="rrc number", anchor='w', width=10)
        label.grid(row=0, column=9, sticky='nsew')
        label = tk.Label(chemFrame, text="comment_chem", anchor='w')
        label.grid(row=0, column=10, sticky='nsew')

        divider = tk.Frame(chemFrame, bg = "black", height=1)
        divider.grid(row=1, column=0, columnspan = 11, sticky='nsew')

        line = 2
        for chemData in self.species[0]:
            source = global_vars.libData[chemData.source]
            label = tk.Label(chemFrame, text=str(source.creation_date.strftime("%d.%m.%Y")), anchor='w')
            label.grid(row=line, column=0, sticky='nsew')
            author = source.author
            if len(source.author)> 20:
                author = source.author[:17] + "..."
            label = tk.Label(chemFrame, text=author, width=16, anchor='w')
            label.grid(row=line, column=1, sticky='nsew')


            label = tk.Label(chemFrame, text=chemData.geometry, anchor='w')
            label.grid(row=line, column=3, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.molar_mass, anchor='w')
            label.grid(row=line, column=4, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.lennard_jones_potential,anchor='w')
            label.grid(row=line, column=5, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.lennard_jones_collision,anchor='w')
            label.grid(row=line, column=6, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.dipole_moment,anchor='w')
            label.grid(row=line, column=7, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.polarizability,anchor='w')
            label.grid(row=line, column=8, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.rotational_relaxation_collision_number,anchor='w')
            label.grid(row=line, column=9, sticky='nsew')
            label = tk.Label(chemFrame, text=chemData.comment_chem, anchor='w')
            label.grid(row=line, column=10, sticky='nsew')
            line -=- 1

        divider = tk.Frame(chemFrame, bg = "black", width=1)
        divider.grid(row=0, column=2, rowspan=line, sticky='nsew')


        chemDataTitle = tk.Label(self, text="Therm Data", font=("Arial", 16), anchor=tk.W)
        chemDataTitle.grid(row=row, column=0, sticky='nsew')
        row -= - 1

        thermFrame = tk.Frame(self)
        thermFrame.grid(row=row, column=0, sticky='nsew', padx=10, pady=10)
        row -= - 1
        for chemData in self.species[1]:
            label = tk.Label(thermFrame, text=str(chemData))
            label.pack(side='left')

        self.center()

    def show(self):
        self.wm_deiconify()
        self.wait_window()