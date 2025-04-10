import tkinter
from tkinter import filedialog
import io

import Reaction_Class
import ScrollableGui
import global_vars
from global_vars import reactions

### IMPORTANT ###
# Lines starting with one start (*) will be seen as disabled reactions
# Lines starting with two or more stars (**) will be seen as comments
# When you add a comment with only one star (*), this code will cause errors and might corrupt your file

dir_name = filedialog.askopenfilename()

if dir_name == "":
    exit(0)

file = open(dir_name, 'r')
lines = file.readlines()
file.close()
chem_start = 0
exit_var = 0
for i in range(len(lines)):
    if lines[i].startswith("SURF"):
        chem_start = i

for i in range(len(lines)):
    if lines[i].startswith("**"):
        chem_start = i + 1
i = chem_start

reactions = global_vars.reactions
while i < len(lines):
    text = lines[i]
    if lines[i].startswith("END"):
        break
    is_sticky = False
    if lines[i].startswith("STICK"):
        i -=- 1
        is_sticky = True
        text = lines[i]
    disabled = 0
    if lines[i].startswith("*"):
        disabled = 1
    input_spec = dict()
    output_spec = dict()
    j = 0 + disabled
    sign = 1
    reversible = False
    while j < 47-8 + disabled:
        spec = text[j:j+8].strip()
        if spec != "":
            if sign == 1:
                input_spec[spec] = input_spec.get(spec, 0) + 1
            else:
                output_spec[spec] = output_spec.get(spec, 0) + 1
        j -=- 8
        symbol = text[j]
        if symbol == ">":
            sign = -1
        if symbol == "=":
            sign = -1
            reversible = True
        j -=- 1
    A_k = float(text[46:56])
    beta_k = float(text[56:63])
    E_k = float(text[63:73])
    reactions.append(Reaction_Class.Reaction(input_spec, output_spec, A_k, beta_k, E_k,is_sticky,reversible, disabled==1))
    i -=- 1

gui = ScrollableGui.ListGui()
gui.focus_set()
gui.title("Reaction Gui")
gui.lift()
gui.attributes('-topmost', True)
gui.attributes('-topmost', False)
gui.center()
gui.mainloop()
