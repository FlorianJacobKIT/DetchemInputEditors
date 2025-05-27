import tkinter as tk


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_spec_text(parent, species_name, text_size: int):
    title = tk.Text(parent, width=len(species_name) + 2, height=2, borderwidth=0, font=("Arial", text_size), background=parent.cget("background"))
    title.tag_configure("subscript", offset=int(-10*text_size/20), font=("Arial", text_size-4))
    for letter in species_name:
        if letter.isnumeric():
            title.insert("insert", letter, "subscript")
        else:
            title.insert("insert", letter, "")
    title.insert("insert", "\n ", "")
    title.tag_configure("center", justify='center')
    title.tag_add("center", 1.0, "end")
    title.configure(state="disabled")
    title.configure(height=2)
    title.configure(cursor="arrow")
    return title
