import tkinter
import tkinter.messagebox
from tkinter import *

from CenterGui import CenterRootWindow
import EditorGui
import global_vars


class ListGui(CenterRootWindow):

    listbox: Listbox = None
    reaction_mapper : dict[int,tuple[str,int]] = {}
    placeholder = 'Search'
    save_content = "non"
    hidden_categorys :list[str] = list()
    search_var: tkinter.StringVar = None


    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        search_var = tkinter.StringVar()
        self.search_var = search_var
        search_var.set("Search")
        search_bar = tkinter.Entry(self, textvariable=search_var, fg="gray")
        search_bar.grid(column=0, row=0, sticky="ew")
        search_var.trace("w", lambda name,index,mode: self.update_search())

        help_label = tkinter.Label(self, text="\'*:\' Fuzzy Search" + " "*5  + "\'e:\' Search in Educts" + " "*5  + "\'p:\' Search in Products")
        help_label.grid(column=1, row=0, columnspan = 2, sticky="ew")


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
        frame.grid(row=1, column=0, columnspan = 3, sticky='nsew')
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

        i = 0
        self.reaction_mapper = {}
        for reaction_category in global_vars.reactions:
            self.listbox.insert(END, str(reaction_category).ljust(120,"-"))
            self.reaction_mapper[i] = (reaction_category, -1)
            i -=- 1
            for j in range(len(global_vars.reactions[reaction_category])):
                self.listbox.insert(END, str(global_vars.reactions[reaction_category][j]))
                self.reaction_mapper[i] = (reaction_category, j)
                i -=- 1
        self.listbox.config(width=0)

        save_btn = tkinter.Button(self, text="Save as copy", command=lambda: self.save("copy"))
        save_btn.grid(row=2, column=0, sticky='nsew')

        save_btn = tkinter.Button(self, text="Overwrite", command=lambda:self.save("overwrite"))
        save_btn.grid(row=2, column=1, sticky='nsew')

        close_btn = tkinter.Button(self, text="Close (Don't Save)", command=lambda: self.ask_destroy())
        close_btn.grid(row=2, column=2, sticky='nsew')

    def update_reaction(self, event):
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return

        reaction_idx = self.reaction_mapper[index]
        if reaction_idx[1] == -1:
            if reaction_idx[0] in self.hidden_categorys:
                self.hidden_categorys.remove(reaction_idx[0])
            else:
                self.hidden_categorys.append(reaction_idx[0])
        else:
            reaction = global_vars.reactions[reaction_idx[0]][reaction_idx[1]]
            EditorGui.UniversalEditorGui(reaction).show()
        self.update_data()
        self.update_search()

    def ask_destroy(self):
        answer = tkinter.messagebox.askokcancel("Don't save", "Are you sure you don't want to save?")
        if answer:
            self.destroy()

    def save(self, type) -> None:
        self.save_content = type
        self.destroy()

    def update_search(self):
        filter_txtstr = self.search_var.get()
        if filter_txtstr == self.placeholder:
            filter_txtstr = "*:"
        self.listbox.delete(0, END)
        entry_nr = 0
        self.reaction_mapper = {}
        i = 0
        mode = ""
        if filter_txtstr.startswith("e:"):
            mode = "e"
            filter_txtstr = filter_txtstr.replace("e:", "", 1).strip().upper()
        elif filter_txtstr.startswith("p:"):
            mode = "p"
            filter_txtstr = filter_txtstr.replace("p:", "", 1).strip().upper()
        elif filter_txtstr.startswith("*:"):
            mode = "*"
            filter_txtstr = filter_txtstr.replace("*:", "", 1).strip().upper()


        for category in global_vars.reactions.keys():
            self.listbox.insert(END, str(category).ljust(120,"-"))
            self.reaction_mapper[entry_nr] = (category, -1)
            entry_nr += 1
            if category not in self.hidden_categorys:
                for index in range(len(global_vars.reactions[category])):
                    text = str(global_vars.reactions[category][index])
                    if mode == "e":
                        for educt in global_vars.reactions[category][index].educts:
                            if filter_txtstr == educt.strip().upper():
                                self.listbox.insert(END, text)
                                self.reaction_mapper[entry_nr] = (category, index)
                                entry_nr += 1
                                break
                    elif mode == "p":
                        for product in global_vars.reactions[category][index].products:
                            if filter_txtstr == product.strip().upper():
                                self.listbox.insert(END, text)
                                self.reaction_mapper[entry_nr] = (category, index)
                                entry_nr += 1
                                break
                    elif mode == "*":
                        if filter_txtstr in text.upper():
                            self.listbox.insert(END, text)
                            self.reaction_mapper[entry_nr] = (category, index)
                            entry_nr += 1
                    else:
                        flag = True
                        for educt in global_vars.reactions[category][index].educts:
                            if filter_txtstr.strip().upper() == educt.strip().upper():
                                self.listbox.insert(END, text)
                                self.reaction_mapper[entry_nr] = (category, index)
                                entry_nr += 1
                                flag = False
                                break
                        if flag:
                            for product in global_vars.reactions[category][index].products:
                                if filter_txtstr.strip().upper() == product.strip().upper():
                                    self.listbox.insert(END, text)
                                    self.reaction_mapper[entry_nr] = (category, index)
                                    entry_nr += 1
                                    break
        self.listbox.update()

    def update_data(self):
        self.listbox.delete(0, END)
        entry_nr = 0
        self.reaction_mapper = {}
        mover = list()
        for category in global_vars.reactions.keys():
            for i in range(len(global_vars.reactions[category])):
                if global_vars.reactions[category][i].category != category:
                    mover.append((category, global_vars.reactions[category][i].category, global_vars.reactions[category][i]))
        for move in mover:
            if move[1] not in global_vars.reactions.keys():
                global_vars.reactions[move[1]] = list()
            global_vars.reactions[move[1]].append(move[2])
            global_vars.reactions[move[0]].remove(move[2])
        for category in global_vars.reactions.keys():
            self.listbox.insert(END, str(category).ljust(120,"-"))
            self.reaction_mapper[entry_nr] = (category, -1)
            entry_nr += 1
            if category not in self.hidden_categorys:
                for i in range(len(global_vars.reactions[category])):
                    text = str(global_vars.reactions[category][i])
                    self.listbox.insert(END, text)
                    self.reaction_mapper[entry_nr] = (category, i)
                    entry_nr += 1
        self.listbox.update()

    def show(self):
        self.wm_deiconify()
        self.wait_window()

