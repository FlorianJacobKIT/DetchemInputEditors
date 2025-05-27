import datetime
import math
import tkinter as tk

import numpy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ChemDataManager import global_vars, Omega_Table, SourceFormat
from ChemDataManager.ChemDataFormat import ChemData
from GeneralUtil import Nat_Constants, MaterialData
from GeneralUtil.CenterGui import CenterWindow


class SourceDataDisplayer(CenterWindow):

    variables: list = []

    self_diff: tuple[list[float],list[float]]
    viscosity: tuple[list[float],list[float]]
    heat_conductivity: tuple[list[float],list[float]]
    plot: Axes
    source: SourceFormat.Source


    def __init__(self, master, source):
        super().__init__(master)
        self.source = source
        row = 0
        label = tk.Label(self, text="Source Information", font=("Arial", 20))
        label.grid(row=row, column=0, columnspan=2)
        row -=- 1
        label = tk.Label(self, text="ID", anchor=tk.W)
        label.grid(row=row, column=0, sticky=tk.EW)
        var = tk.IntVar()
        var.set(self.source.ID)
        edit = tk.Entry(self, textvariable=var, justify=tk.RIGHT, fg="gray",state=tk.DISABLED)
        edit.grid(row=row, column=1, sticky=tk.EW)
        row -=- 1

        self.max_width = 0
        for value in self.source.__dict__.values():
            if type(value) == str:
                self.max_width = max(self.max_width, len(value))

        self.add_property(row,"author")
        row -=- 1
        self.add_property(row,"title")
        row -=- 1
        self.add_date_property(row,"creation_date")
        row -=- 1
        self.add_property(row,"publisher")
        row -=- 1
        self.add_property(row,"source_type")
        row -=- 1
        self.add_property(row,"link")
        row -=- 1
        self.add_property(row,"comment")
        row -=- 1


        x:list[float] = []
        self_diff:list[float] = []
        viscosity:list[float] = []

        self.self_diff = (x, self_diff)
        self.viscosity = (x, viscosity)

        self.grid_columnconfigure(1, weight=1)

        self.center()


    def add_property(self, row, text, color = "black", var: tk.Variable = None):
        state = tk.NORMAL
        if self.source.ID < 0:
            state = tk.DISABLED
        title = text.split("_")
        for i in range(len(title)):
            title[i] = title[i].capitalize()
        title = " ".join(title)
        title += ": "
        label = tk.Label(self, text=title, anchor=tk.W)
        label.grid(row=row, column=0, sticky=tk.EW)
        dict_version = self.source.__dict__
        if var is None:
            var = tk.StringVar()
        var.set(dict_version[text])
        edit = tk.Entry(self, textvariable=var, width=self.max_width, justify=tk.LEFT, fg=color, state=state)
        edit.grid(row=row, column=1, sticky=tk.EW)
        def set_value(var,text,e):
            dict_version = self.source.__dict__
            dict_version[text] = var.get()

        var.trace_add("write", lambda a,b,c,v=var,t=text, e=edit: set_value(var,t,e))


    def add_date_property(self, row, text):
        state = tk.NORMAL
        if self.source.ID < 0:
            state = tk.DISABLED
        title = text.split("_")
        for i in range(len(title)):
            title[i] = title[i].capitalize()
        title = " ".join(title)
        title += ": "
        label = tk.Label(self, text=title, anchor=tk.W)
        label.grid(row=row, column=0, sticky=tk.EW)
        var = tk.StringVar()
        var.set(datetime.datetime.strftime(self.source.creation_date, "%d.%m.%Y"))
        edit = tk.Entry(self, textvariable=var, width=self.max_width, justify=tk.LEFT, state=state)
        edit.grid(row=row, column=1, sticky=tk.EW)
        def set_value(var,e:tk.Entry):
            try:
                self.source.creation_date = datetime.datetime.strptime(var.get(), "%d.%m.%Y").date()
                e.config(fg = "black")
            except ValueError:
                e.config(fg = "red")

        var.trace_add("write", lambda a,b,c,v=var, e=edit: set_value(var,e))


    def clear_plot(self):
        self.plot.clear()
        self.plot.ticklabel_format(axis='y', scilimits=[-3, 3])
        self.plot.grid(True)




