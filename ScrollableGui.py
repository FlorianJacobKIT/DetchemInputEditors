import math
import os
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.scrolledtext import ScrolledText

import Config
import EditorGui
import ReactionEditorGui
import global_vars
from CenterGui import CenterRootWindow
from Reaction_Class import Reaction
from adjustclass import AdjustClass


class ListGui(CenterRootWindow):

    listbox: ScrolledText = None
    reaction_mapper : dict[str,tuple[str,int, dict[str,Widget]]] = {}
    reverse_mapper: dict[Reaction|str, str] = {}
    placeholder = 'Search'
    save_content = "non"
    hidden_categorys :list[str] = list()
    search_var: tkinter.StringVar = None

    def __init__(self, adjust: AdjustClass):
        super().__init__()

        self.adjust_obj = adjust
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        width = 30
        search_var = tkinter.StringVar()
        self.search_var = search_var
        search_var.set("Search")
        search_bar = tkinter.Entry(self, textvariable=search_var, fg="gray", width=width)
        search_bar.grid(column=0, row=0, pady = (5,0), padx = 5, sticky="w")
        search_var.trace("w", lambda name,index,mode: self.update_search())

        help_label = tkinter.Label(self, text="\'*:\' Fuzzy Search" + "\n"  + "\'e:\' Search in Educts" + "\n"  + "\'p:\' Search in Products", anchor=tkinter.W, justify=tkinter.LEFT)
        help_label.grid(column=0, row=1, columnspan=2, sticky="w")

        def update_adjust(adjust_object: AdjustClass) -> None:
            adjust_data = adjust_object.adjust_data
            EditorGui.UniversalEditorGui(adjust_data).show()
            adjust_object.adjust_data = adjust_data
            adjust_config = os.path.join(global_vars.parent, "adjust.json")
            target = open(adjust_config, "w")
            target.write(adjust_data.toJSON(pretty=True))
            target.close()


        new_btn = tkinter.Button(self,text="Edit Adjust Data (use careful)",command=lambda :update_adjust(adjust), width=width)
        new_btn.grid(column=1, row=0, pady = (5,0), padx = 5, sticky="ew")

        # Secures the placement of all other elements
        space_frame = tkinter.Frame(self)
        space_frame.grid(column=3, row=0, sticky="ew")

        new_btn = tkinter.Button(self,text="New Reaction",command=self.add_reaction, width=width, font=("Arial", 16))
        new_btn.grid(column=4, row=0, pady = (5,0), padx = 5, rowspan = 2, sticky="nwse")


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

        self.container = Frame(self, relief=tkinter.RIDGE, borderwidth=3)
        self.container.grid(row=2, column=0, columnspan = 5, sticky='nsew')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.listbox = ScrolledText(self.container, state=DISABLED, relief=FLAT, bg= self.container["background"], cursor = "arrow")

        self.listbox.grid(row=0, column=0, pady = 5, sticky='nsew')
        self.listbox.bind_all('<MouseWheel>', self.scroll)

        self.container = Frame(self.listbox)
        self.listbox.window_create('1.0', window=self.container, padx=5, pady=5, stretch=1)

        #for x in range(100):
        #    listNodes.insert(END, str(x))

        i = 0
        for reaction_category in global_vars.reactions:
            header_label = tkinter.Label(self.container, name="header:" + reaction_category, text=str(reaction_category).ljust(160,"-"), fg="gray", font=("Arial", (Config.text_size * 5)//4, "bold"),anchor=tkinter.W)
            self.reaction_mapper[str(header_label)] = (reaction_category, -1, dict())
            self.reverse_mapper[reaction_category] = str(header_label)
            header_label.grid(row=i, column=0, columnspan=3, sticky='nsew')
            i -=- 1
            for j in range(len(global_vars.reactions[reaction_category])):
                reaction_frame = tkinter.Frame(self.container, name="frame:" + reaction_category+ ":" + str(j))
                widgets = self.add_reaction_to_frame(global_vars.reactions[reaction_category][j], reaction_frame, Config.text_size)
                self.reaction_mapper[str(reaction_frame)] = (reaction_category, j, widgets)
                self.reverse_mapper[global_vars.reactions[reaction_category][j]] = str(reaction_frame)
                reaction_frame.grid(row=i, column=0, sticky='nsew')
                i -=- 1

        save_btn = tkinter.Button(self, text="Save as copy", command=lambda: self.save("copy"), width=width)
        save_btn.grid(row=3, column=0, padx = 5, pady = 5, sticky='nsw')

        overwrite_btn = tkinter.Button(self, text="Overwrite", command=lambda:self.save("overwrite"), width=width)
        overwrite_btn.grid(row=3, column=1, padx = 5, pady = 5, sticky='nsw')

        def run_adjust():
            self.adjust_obj.adjust()
            for reaction_category in global_vars.reactions:
                for j in range(len(global_vars.reactions[reaction_category])):
                    self.update_reaction_frame(global_vars.reactions[reaction_category][j])

        adjust_btn = tkinter.Button(self, text="Adjust", command=lambda: run_adjust(), width=width)
        adjust_btn.grid(row=3, column=2, padx = 5, pady = 5, sticky='nsw')

        close_btn = tkinter.Button(self, text="Close (Don't Save)", command=lambda: self.ask_destroy(), width=width)
        close_btn.grid(row=3, column=4, padx = 5, pady = 5, sticky='nse')

    def scroll(self, event):
        current_view = self.listbox.yview()
        self.listbox.yview_moveto(current_view[0] + event.delta/120 * (-1) * 0.01)




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
        if filter_txtstr == "":
            filter_txtstr = "*:"
        for child in self.container.winfo_children():
            child.grid_forget()
        entry_nr = 0
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


        for category in global_vars.reactions:
            header_label_name = self.reverse_mapper[category]
            header_label = self.container.nametowidget(header_label_name)
            header_label.grid(row=i, column=0, columnspan=3, sticky='nsew')
            i -=- 1
            if category not in self.hidden_categorys:
                for index in range(len(global_vars.reactions[category])):
                    text = str(global_vars.reactions[category][index])
                    reaction_frame_name = self.reverse_mapper[global_vars.reactions[category][index]]
                    reaction_frame = self.container.nametowidget(reaction_frame_name)
                    if mode == "e":
                        for educt in global_vars.reactions[category][index].educts:
                            if filter_txtstr == educt.strip().upper():
                                reaction_frame.grid(row=i, column=0, sticky='nsew')
                                i -=- 1
                                break
                    elif mode == "p":
                        for product in global_vars.reactions[category][index].products:
                            if filter_txtstr == product.strip().upper():
                                reaction_frame.grid(row=i, column=0, sticky='nsew')
                                i -=- 1
                                break
                    elif mode == "*":
                        if filter_txtstr in text.upper():
                            reaction_frame.grid(row=i, column=0, sticky='nsew')
                            i -=- 1
                    else:
                        flag = True
                        for educt in global_vars.reactions[category][index].educts:
                            if filter_txtstr.strip().upper() == educt.strip().upper():
                                reaction_frame.grid(row=i, column=0, sticky='nsew')
                                i -=- 1
                                flag = False
                                break
                        if flag:
                            for product in global_vars.reactions[category][index].products:
                                if filter_txtstr.strip().upper() == product.strip().upper():
                                    reaction_frame.grid(row=i, column=0, sticky='nsew')
                                    i -=- 1
                                    break

    def update_data(self):
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

    def show(self):
        self.wm_deiconify()
        self.wait_window()

    def add_reaction(self):
        firstKey = list(global_vars.reactions.keys())[0]
        reaction = Reaction(category=firstKey, is_reversible=True)
        global_vars.reactions[firstKey].append(reaction)

        j = global_vars.reactions[firstKey].index(reaction)
        reaction_frame = tkinter.Frame(self.container, name="frame:" + firstKey + ":" + str(j))
        widgets = self.add_reaction_to_frame(reaction, reaction_frame, 16)
        self.reaction_mapper[str(reaction_frame)] = (firstKey, j, widgets)
        self.reverse_mapper[reaction] = str(reaction_frame)

        EditorGui.UniversalEditorGui(reaction).show()
        self.update_data()
        self.update_search()

    no_garbage_collector = list()

    def add_reaction_to_frame(self, reaction, frame, text_size):
        widgets = dict()
        i = 0
        label = tkinter.Label(frame, text=reaction.name, anchor=tkinter.E, width=4)
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        i -= - 1
        adjustable = tkinter.IntVar()
        adjustable.set(reaction.is_adjustable)
        self.no_garbage_collector.append(adjustable)
        box = tkinter.Checkbutton(frame, variable=adjustable)
        adjustable.trace('w', lambda name, index, v, parent,r= reaction: r.set_adjustable(v))
        box.grid(row = 0, column = i, sticky=tkinter.NSEW)
        i -=- 1
        weight = tkinter.DoubleVar()
        weight.set(reaction.weight)
        self.no_garbage_collector.append(weight)
        weight_entry = tkinter.Entry(frame, font=('Arial', text_size), width=5, textvariable=weight)
        weight.trace('w', lambda name, index, v, parent, r= reaction: r.set_weight(v))
        weight_entry.grid(row = 0, column = i, sticky=tkinter.NSEW)
        i -=- 1
        self.add_species_label(reaction, frame, reaction.educts, i, text_size)
        i -= - 1
        if reaction.is_reversible:
            text = "<->"
        else:
            text = "->"
        label = tkinter.Label(frame, text=text, width=3,anchor=tkinter.E, font=("Arial", text_size), cursor = "pencil")
        label.bind("<Button-1>", lambda event, r = reaction: self.edit_reaction(r))
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        i -= - 1
        self.add_species_label(reaction, frame, reaction.products, i, text_size)
        i -= - 1
        label = tkinter.Frame(frame, width=10)
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        i -= - 1
        label = tkinter.Frame(frame, width=1, bg="black")
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        i -= - 1
        label = tkinter.Frame(frame, width=10)
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        i -= - 1
        title = ""
        if reaction.is_stick:
            title = "S=" + "{:10.3E}".format(reaction.sticking_coefficient)
        else:
            title = "A=" + "{:10.3E}".format(reaction.A_k)
        label = tkinter.Label(frame, text=title, width=12,anchor=tkinter.E, font=("Arial", text_size), borderwidth=1, cursor = "bottom_left_corner",activebackground="gray")
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        widgets["A_k_label"] = label
        i -= - 1
        value = 0
        if reaction.old_A_k != 0:
            value = math.log10(reaction.A_k/reaction.old_A_k)
        if reaction.is_stick:
            value = math.log(reaction.A_k/reaction.old_A_k) / math.log(2.)
        status = StatusBarWidget(frame, text_size*1.5,value)
        status.grid(row=0, column=i, sticky=tkinter.NS)
        widgets["A_k_status"] = status
        i -= - 1
        label = tkinter.Label(frame, text="{:g}".format(reaction._beta_k), width=10, anchor=tkinter.E, font=("Arial", text_size), cursor ="bottom_left_corner", activebackground="gray")
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        widgets["beta_k_label"] = label
        i -= - 1
        status = StatusBarWidget(frame, text_size * 1.5, reaction._beta_k - reaction.old_beta_k)
        status.grid(row=0, column=i, sticky=tkinter.NS)
        widgets["beta_k_status"] = status
        i -= - 1
        label = tkinter.Label(frame, text="{:g}".format(reaction.E_k*1e-3), width=10,anchor=tkinter.E, font=("Arial", text_size), cursor = "bottom_left_corner",activebackground="gray")
        label.grid(row=0, column=i, sticky=tkinter.NSEW)
        widgets["E_k_label"] = label
        i -= - 1
        status = StatusBarWidget(frame, text_size*1.5,(reaction.E_k-reaction.old_E_k)/5.)
        status.grid(row=0, column=i, sticky=tkinter.NS)
        widgets["E_k_status"] = status
        i -= - 1
        return widgets

    def add_species_label(self, reaction, frame, species, i, text_size):
        text = ""
        for key, value in species.items():
            text += str(value) + str(key) + " + "
        text = text[:-3]
        label = tkinter.Label(frame, text=text, width=20, anchor=tkinter.W, font=("Arial", text_size), cursor = "pencil")
        label.bind("<Button-1>", lambda event,r= reaction: self.edit_reaction(r))
        label.grid(row=0, column=i, sticky=tkinter.NSEW)

    def edit_reaction(self, reaction):
        ReactionEditorGui.UniversalEditorGui(reaction).show()
        self.update_reaction_frame(reaction)
        self.update_search()

    def update_reaction_frame(self, reverse):
        reaction_frame_name = self.reverse_mapper.pop(reverse)
        frame = self.container.nametowidget(reaction_frame_name)
        (reaction_category, j, widgets) = self.reaction_mapper.pop(reaction_frame_name)
        for child in frame.winfo_children():
            child.destroy()
        widgets = self.add_reaction_to_frame(reverse, frame,
                                             Config.text_size)
        self.reaction_mapper[str(frame)] = (reaction_category, j, widgets)
        self.reverse_mapper[reverse] = str(frame)


class StatusBarWidget(tkinter.Frame):
    def __init__(self, master, height, size=0.):
        tkinter.Frame.__init__(self, master)
        self.height = height - 3
        self.canvas = tkinter.Canvas(self, height=height, width=13)
        self.canvas.grid(sticky=tkinter.NSEW)
        self.set_size(size)

    def set_size(self, size):
        for ID in self.canvas.find_all():
            self.canvas.delete(ID)
        self.canvas.create_rectangle(2, 2, 14, self.height + 2,
                                     outline="black")
        if size > 1.: size = 1.
        if size < -1.: size = -1.
        if size != 0.:
            w = self.canvas.create_rectangle(3, self.height//2 + 3, 14, self.height//2 + int(self.height/2 * size) + 3,
                                             fill=self.color(size), width=0)
        self.canvas.create_line(1, self.height//2 + 2, 14, self.height//2 + 2, width=1, fill="black")


    def color(self, size):
        size = abs(size)
        r = min((255, int(500 * size)))
        g = max((0, min((255, int(400 * (1 - size))))))
        return "#%2.2x%2.2x%2.2x" % (r, g, 0)

