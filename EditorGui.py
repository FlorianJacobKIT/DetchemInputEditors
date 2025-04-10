import ctypes
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import copy

from CenterGui import CenterGui
from Interfaces import Checkable,SelfFixing
from Reaction_Class import Reaction


#setattr(self, key, value)

class UniversalEditorGui(CenterGui):

    entry_vars: dict[tkinter.Variable] = {}
    reaction = None

    def __init__(self, reaction):
        super().__init__()
        self.reaction = reaction
        self.focus_set()
        self.generate_fields()

    def generate_fields(self):
        dict_version = self.reaction.__dict__
        self.grid_columnconfigure(1, weight=1)
        i = 0
        for key, value in dict_version.items():
            if type(value) == dict:
                frame = tkinter.Frame(self, name=key, borderwidth=2, relief=tkinter.RIDGE)
                frame.grid(column=0, row=i, columnspan=2, sticky="nsew", pady=2)
                sub_dict: dict
                sub_dict = dict_version[key]
                label = tkinter.Label(frame, text=key, font=("FixedSys", 12, "bold"), anchor=tkinter.W)
                label.grid(column=0, row=0, columnspan=1, sticky="w")
                add_btn = tkinter.Button(frame, text="+", command=lambda d=value: self.add(d))
                add_btn.grid(column=1, row=0, sticky="ew")
                j = 1
                for dict_key, dict_value in sub_dict.items():
                    sub_element = sub_dict[dict_key]
                    label = tkinter.Label(frame, text="  " + dict_key, font=("FixedSys", 12), width=20, anchor=tkinter.W)
                    label.grid(column=0, row=j, sticky="nsew")
                    self.entry_vars[key + ":" + dict_key] = getVar(sub_element)
                    self.entry_vars[key + ":" + dict_key].set(sub_element)
                    entry = tkinter.Entry(frame, textvariable=self.entry_vars[key + ":" + dict_key])
                    entry.grid(column=1, row=j, sticky="nsew")
                    rem_btn = tkinter.Button(frame, text="-", command=lambda d=value: self.remove_entry(d, dict_key))
                    rem_btn.grid(column=2, row=j, sticky="nsew")
                    j -= - 1


            elif type(value) == list:
                sub_list = dict_version[key]
                print("List: ", key)
            elif type(value) == bool:
                sub_bool = dict_version[key]
                text = key
                if text.startswith("is_"):
                    text = text[3:]
                label = tkinter.Label(self, text=text, font=("FixedSys", 12), width=20, anchor=tkinter.W)
                label.grid(column=0, row=i, sticky="w")
                self.entry_vars[key] = tkinter.BooleanVar()
                self.entry_vars[key].set(sub_bool)
                entry = tkinter.Button(self, text="On" if self.entry_vars[key].get() else "Off")
                entry.config(command=lambda k=key,btn= entry: self.update_btn(k, btn))
                entry.grid(column=1, row=i, sticky="nsew")
            elif type(value) == float:
                sub_float = dict_version[key]
                label = tkinter.Label(self, text=key + " (float)", font=("FixedSys", 12), width=20, anchor=tkinter.W)
                label.grid(column=0, row=i, sticky="w")
                self.entry_vars[key] = tkinter.DoubleVar()
                self.entry_vars[key].set(sub_float)
                entry = tkinter.Entry(self, textvariable=self.entry_vars[key])
                entry.grid(column=1, row=i, sticky = "nsew")
            elif type(value) == int:
                sub_int = dict_version[key]
                label = tkinter.Label(self, text=key + " (int)", font=("FixedSys", 12), width=20, anchor=tkinter.W)
                label.grid(column=0, row=i, sticky="w")
                self.entry_vars[key] = tkinter.IntVar()
                self.entry_vars[key].set(sub_int)
                entry = tkinter.Entry(self, textvariable=self.entry_vars[key])
                entry.grid(column=1, row=i, sticky = "nsew")
            else:
                sub_element = dict_version[key]
                label = tkinter.Label(self, text=key, font=("FixedSys", 12), width=20, anchor=tkinter.W)
                label.grid(column=0, row=i, sticky="w")
                self.entry_vars[key] = tkinter.StringVar()
                self.entry_vars[key].set(str(sub_element))
                entry = tkinter.Entry(self, textvariable=self.entry_vars[key])
                entry.grid(column=1, row=i, sticky = "nsew")

            i -= - 1
        save_btn = tkinter.Button(self, text="Save", command=self.save)
        save_btn.grid(row=i, column=0, sticky='nsew')
        close_btn = tkinter.Button(self, text="Cancel (Don't Save)", command=lambda: self.ask_destroy())
        close_btn.grid(row=i, column=1, sticky='nsew')

    def ask_destroy(self):
        self.destroy()

    def save(self):
        dupe = copy.deepcopy(self.reaction)
        dict_version = dupe.__dict__
        for key, value in dict_version.items():
            if type(value) == dict:
                value = dict()
                dict_version[key] = value
                sub_key_list = [k for k in self.entry_vars.keys() if k.split(":")[0]== key]
                for combi_key in sub_key_list:
                    sub_key = combi_key.split(":")[1]
                    value[sub_key] = self.entry_vars[combi_key].get()
                continue
            if key in self.entry_vars:
                setattr(dupe, key, self.entry_vars[key].get())

        if isinstance(dupe, SelfFixing):
            dupe.fix()

        if isinstance(dupe, Checkable):
            check: Checkable = dupe
            if check.check():
                dict_version = self.reaction.__dict__
                for key, value in dict_version.items():
                    if type(value) == dict:
                        value = dict()
                        dict_version[key] = value
                        sub_key_list = [k for k in self.entry_vars.keys() if k.split(":")[0] == key]
                        for combi_key in sub_key_list:
                            sub_key = combi_key.split(":")[1]
                            value[sub_key] = self.entry_vars[combi_key].get()
                        continue
                    if key in self.entry_vars:
                        setattr(self.reaction, key, self.entry_vars[key].get())
                if isinstance(self.reaction, SelfFixing):
                    self.reaction.fix()
                self.destroy()
                return
            return
        tkinter.messagebox.showerror("Error", "Data type for Editor not supported")
        self.destroy()


    def show(self):
        self.wm_deiconify()
        self.wait_window()

    def add(self, d):
        name = tkinter.simpledialog.askstring("Set name", "Name", parent=self)
        if len(name) > 8:
            tkinter.messagebox.showerror("Error", "Name too long, max 8 characters")
            return
        else:
            d[name] = 0
        for widget in self.winfo_children():
            widget.destroy()
        self.entry_vars.clear()
        self.generate_fields()

    def remove_entry(self, d, sub_key):
        if sub_key in d:
            d.pop(sub_key)
        for widget in self.winfo_children():
            widget.destroy()
        self.entry_vars.clear()
        self.generate_fields()

    def update_btn(self, key, btn):
        self.entry_vars[key].set(not self.entry_vars[key].get())
        btn.configure(text="On" if self.entry_vars[key].get() else "Off")
        btn.update()

def getVar(fieldElement):
    if type(fieldElement) == dict:
        var = tkinter.StringVar()
        var.set(str(fieldElement))
        return var
    elif type(fieldElement) == list:
        var = tkinter.StringVar()
        var.set(str(fieldElement))
        return var
    elif type(fieldElement) == bool:
        var = tkinter.BooleanVar()
        var.set(fieldElement)
        return var
    elif type(fieldElement) == float:
        var = tkinter.DoubleVar()
        var.set(fieldElement)
        return var
    elif type(fieldElement) == int:
        var = tkinter.IntVar()
        var.set(fieldElement)
        return  var
    else:
        var = tkinter.StringVar()
        var.set(str(fieldElement))
        return var

