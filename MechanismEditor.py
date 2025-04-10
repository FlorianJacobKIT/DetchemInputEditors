from tkinter import filedialog

import Reaction_Class
import ScrollableGui
import global_vars

### IMPORTANT ###
# Lines starting with one start (*) will be seen as disabled reactions
# Lines starting with two or more stars (**) will be seen as comments, the last one as the category
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
        chem_start = i + 1
category = ""
for i in range(chem_start, len(lines)):
    if lines[i].startswith("**"):
        category = lines[i]
        chem_start = i + 1
    else:
        break
category = category.replace("*", "")
category = category.replace("\n", "")
category = category.strip()
i = chem_start
if category == "":
    category = "Reactions"
else:
    chem_start -= 1


reactions = global_vars.reactions
reactions[category] = list()
while i < len(lines):
    text = lines[i]
    if lines[i].startswith("END"):
        break
    if lines[i].startswith("**"):
        category = lines[i]
        category = category.replace("*", "")
        category = category.replace("\n", "")
        category = category.strip()
        reactions[category] = list()
        i -=- 1
        continue
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
    reactions[category].append(Reaction_Class.Reaction(input_spec, output_spec, A_k, beta_k, E_k, category,is_sticky,reversible, disabled==1))
    i -=- 1

gui = ScrollableGui.ListGui()
gui.focus_set()
gui.title("Reaction Gui")
gui.lift()
gui.attributes('-topmost', True)
gui.attributes('-topmost', False)
gui.center()
gui.show()
if gui.save_content == "copy" or gui.save_content == "overwrite":
    lines = lines[:chem_start]
    for category in reactions:
        lines.append("**** " + category + "\n")
        for reaction in reactions[category]:
            line = ""
            if reaction.is_sticky:
                lines.append("STICK\n")
            if reaction.is_disabled:
                line += "*"
            for educt in reaction.educts:
                for i in range(reaction.educts[educt]):
                    line += str(educt).ljust(8)
                    line += "+"
            line = line[:-1]
            if reaction.is_reversible:
                line += "="
            else:
                line += ">"
            for product in reaction.products:
                for i in range(reaction.products[product]):
                    line += str(product).ljust(8)
                    line += "+"
            line = line[:-1]
            line = line.ljust(45)
            line += "{:10.3E}".format(reaction.A_k)
            line += "{:7G}".format(reaction.beta_k)
            line += "{:10G}".format(reaction.E_k)
            line += "\n"
            lines.append(line)
    lines.append("END\n")
    lines.append("-"*72)

    filename = dir_name
    if gui.save_content == "copy":
        split = dir_name.split(".")
        filename = split[0] + "_edit." + split[1]
    file = open(filename, 'w')
    file.writelines(lines)
    file.close()
