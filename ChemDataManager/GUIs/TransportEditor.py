import math

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import array

from ChemDataManager import global_vars
from ChemDataManager.ChemDataFormat import ChemData
from GeneralUtil import Nat_Constants
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
        label = tk.Label(self, text="Transport Data", font=("Arial", 20))
        label.grid(row=row, column=0, columnspan=4)
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
        spacer = tk.Frame(self, width=30)
        spacer.grid(row=1, column=2)

        plotFrame = tk.Frame(self)
        x = list(range(10))
        # list of squares
        y = [i ** 2 for i in x]
        data =  [x,y]
        self.plot(plotFrame, data)
        plotFrame.grid(row=1, column=3, rowspan=row-1, sticky=tk.NSEW)



    def plot_diff(self):
        T = 300
        M = self.chem_data.molar_mass
        p = 101325.0 #Pa
        col = self.chem_data.lennard_jones_collision * 1e-10
        omega11 = 1
        x = 3 / 8 * math.sqrt(math.pi * Nat_Constants.N_A * (Nat_Constants.k_b * T) ** 3 / M) / (p * math.pi * col ** 2 * omega11)


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

    def plot(self, parent, data):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                     dpi=50)


        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(data[0], data[1])

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master=parent)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        #toolbar = NavigationToolbar2Tk(canvas,
        #                               parent)
        #toolbar.update()

        # placing the toolbar on the Tkinter window
        #canvas.get_tk_widget().pack()



class ThermDataDisplayer(CenterWindow):
    def __init__(self, master, chem_data: ChemData):
        super().__init__(master)
        self.chem_data = chem_data
        source = global_vars.libData[self.chem_data.source]
        self.source = source
        label = tk.Label(self.master, text="ThermData")
        label.grid(row=0, column=0)


