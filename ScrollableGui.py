import ctypes
import tkinter
import tkinter.messagebox
from tkinter import *

from CenterGui import CenterGui
import EditorGui
import global_vars


class ListGui(tkinter.Tk,CenterGui):

    listbox: Listbox = None
    reaction_mapper = {}
    placeholder = 'Search'
    save_content = False

    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)



        search_var = tkinter.StringVar()
        search_var.set("Search")
        search_bar = tkinter.Entry(self, textvariable=search_var, fg="gray")
        search_bar.grid(column=0, row=0, sticky="ew")
        search_var.trace("w", lambda name,index,mode: self.update_search(search_var.get()))


        def erase(event=None):
            if search_bar.get() == self.placeholder:
                search_bar.delete(0, 'end')
                search_bar.config(fg="black")
        def add(event=None):
            if search_bar.get() == '':
                search_bar.insert(0, self.placeholder)
                search_bar.config(fg="gray")

        search_bar.bind('<FocusIn>', erase)
        search_bar.bind('<FocusOut>', add)

        frame = Frame(self, bg="blue")
        frame.grid(row=1, column=0, columnspan = 2, sticky='nsew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.listbox = Listbox(frame, font=("FixedSys", 12))
        self.listbox.grid(row=0, column=0, sticky='nsew')

        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<Double-Button>', self.update_reaction)
        self.listbox.bind('<Return>', self.update_reaction)

        #for x in range(100):
        #    listNodes.insert(END, str(x))

        for reaction in global_vars.reactions:
            self.listbox.insert(END, str(reaction))
        self.listbox.config(width=0)

        self.reaction_mapper = {}
        for i in range(len(global_vars.reactions)):
            self.reaction_mapper[i] = i

        save_btn = tkinter.Button(self, text="Save", command=self.save)
        save_btn.grid(row=2, column=0, sticky='nsew')

        close_btn = tkinter.Button(self, text="Close (Don't Save)", command=lambda: self.ask_destroy())
        close_btn.grid(row=2, column=1, sticky='nsew')

    def update_reaction(self, event):
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return
        reaction_idx = self.reaction_mapper[index]
        reaction = global_vars.reactions[reaction_idx]
        EditorGui.UniversalEditorGui(reaction).show()
        self.update_data()

    def ask_destroy(self):
        answer = tkinter.messagebox.askokcancel("Don't save", "Are you sure you don't want to save?")
        if answer:
            self.destroy()

    def save(self):
        self.save_content = True
        self.destroy()

    def update_search(self, filter_txtstr):
        if filter_txtstr == self.placeholder:
            filter_txtstr = ""
        self.listbox.delete(0, END)
        entry_nr = 0
        self.reaction_mapper = {}
        for i in range(len(global_vars.reactions)):
            text = str(global_vars.reactions[i])
            if filter_txtstr.upper() in text.upper():
                self.listbox.insert(END, text)
                self.reaction_mapper[entry_nr] = i
                entry_nr += 1
        self.listbox.update()

    def update_data(self):
        self.listbox.delete(0, END)
        entry_nr = 0
        self.reaction_mapper = {}
        for i in range(len(global_vars.reactions)):
            text = str(global_vars.reactions[i])
            self.listbox.insert(END, text)
            self.reaction_mapper[entry_nr] = i
            entry_nr += 1
        self.listbox.update()

    def show(self):
        self.wm_deiconify()
        self.wait_window()

