from collections.abc import Callable

from ChemDataManager import global_vars, SourceFormat
from ChemDataManager.GUIs import DataEditor, SourceEditor
from GeneralUtil import TextModifiers
from GeneralUtil.CenterGui import CenterWindow
import tkinter as tk
import webbrowser as wb
from tkinter import messagebox


class SourceDisplay(CenterWindow):

    chem_checks: dict[tk.Checkbutton, int]

    def __init__(self, parent, selected_id: int = -1):
        super().__init__(parent)
        self.selected_id = selected_id
        self.chem_checks = dict()
        row = 0
        column = 0
        title = tk.Label(self, text="Available Sources", font=("Arial", 20))

        title.grid(row=row, column=0, sticky='nsew')
        row -=- 1

        chemFrame = tk.Frame(self)
        chemFrame.grid(row=row, column=0, sticky='nsew', padx=10, pady=10)
        row -= - 1

        self.load_source_frame(chemFrame)
        self.update_source_checks()


        self.center()



    def update_source_checks(self, c= None):
        if c is not None:
            source_id = self.chem_checks[c]
            if self.selected_id == source_id:
                self.selected_id = -1
            else:
                self.selected_id = source_id
        for chem in self.chem_checks:
            if self.selected_id == self.chem_checks[chem]:
                chem.select()
            else:
                chem.deselect()


    def create_new_source(self, c):
        from tkinter import messagebox
        answer = messagebox.askokcancel("Create new source", "Do you want to create a new source?", parent=self)
        print(answer)
        if not answer:
            return
        max_id = max(global_vars.libData.keys()) + 1
        source = SourceFormat.Source(max_id)
        SourceEditor.SourceDataDisplayer(self, source).show()
        global_vars.libData[max_id] = source
        for child in c.winfo_children():
            child.destroy()
        self.load_source_frame(c)

    def open_link(self, source):
        answer = messagebox.askokcancel("Open Link", "Do you want to open the link? \n(Links don't get checked and might cause potential harm.)", parent=self)
        if answer:
            wb.open(source.link)

    def load_source_frame(self, chemFrame):
        new_source_button = tk.Button(chemFrame, text="+", command=lambda c=chemFrame: self.create_new_source(c))
        new_source_button.grid(row=0, column=0, sticky='nsew')
        chemDataTitle = tk.Label(chemFrame, text="Source", font=("Arial", 16), anchor=tk.W)
        chemDataTitle.grid(row=0, column=1, columnspan=2, sticky='nsew')
        column = 4
        label = tk.Label(chemFrame, text="Title", anchor=tk.W, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="Publisher", anchor=tk.W, width=15)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="Source Type", anchor=tk.W, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="Link", anchor=tk.W, width=10)
        column = self.add_label(column, label, 0)
        label = tk.Label(chemFrame, text="Comment", anchor=tk.W)
        column = self.add_label(column, label, 0)
        divider = tk.Frame(chemFrame, bg="black", height=1)
        divider.grid(row=1, column=0, columnspan=column, sticky='nsew')
        line = 2

        def open_editor(source):
            SourceEditor.SourceDataDisplayer(self, source).show()
            for child in chemFrame.winfo_children():
                child.destroy()
            self.chem_checks = dict()
            self.load_source_frame(chemFrame)
            self.update_source_checks()



        for source_id,source in global_vars.libData.items():
            column = 0

            checker = tk.Checkbutton(chemFrame)
            checker.config(command=lambda c=checker: self.update_source_checks(c))
            self.chem_checks[checker] = source_id
            column = self.add_label(column, checker, line)

            label = tk.Label(chemFrame, text=str(source.creation_date.year), anchor=tk.W)
            column = self.add_label(column, label, line)
            author = source.author
            if len(source.author) > 20:
                author = source.author[:17] + "..."
            label = tk.Label(chemFrame, text=author, width=16, anchor=tk.W)
            column = self.add_label(column, label, line)

            click_effect = lambda e, c=source: open_editor(c)

            open_link = lambda e, c=source: self.open_link(c)

            column -= - 1
            label = tk.Label(chemFrame, text=source.title, anchor=tk.W)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=source.publisher, anchor=tk.W)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=source.source_type, anchor=tk.W)
            column = self.add_label(column, label, line, click_effect)
            label = tk.Label(chemFrame, text=source.link, anchor=tk.W)
            column = self.add_label(column, label, line, open_link, cursor="hand2")
            label = tk.Label(chemFrame, text=source.comment, anchor=tk.W)
            column = self.add_label(column, label, line, click_effect)
            line -= - 1
        divider = tk.Frame(chemFrame, bg="black", width=1)
        divider.grid(row=0, column=3, rowspan=line, sticky='nsew')


    def add_label(self, column, label, line, click_effect:Callable= None, cursor:str = "pencil"):
        if click_effect is not None:
            label.config(cursor = cursor)
        label.grid(row=line, column=column, sticky='nsew')
        label.bind("<Button-1>", click_effect)
        column -= - 1
        return column
