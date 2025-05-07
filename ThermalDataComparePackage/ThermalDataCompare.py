import array
import os.path
from tkinter import filedialog, messagebox

import numpy
from numpy import character

from GeneralUtil.MaterialData import Species, State, reconvert_state

from GeneralUtil import ThermalDataReader

# Warning: Electrons get ignored, might cause issues when charged species are involved

dir_name_1 = filedialog.askopenfilename(title="First Thermal Data File")
if dir_name_1 == "":
    exit(0)

read1 = ThermalDataReader.read_all_file(dir_name_1)

dir_name_2 = filedialog.askopenfilename(title="Second Thermal Data File")
if dir_name_2 == "":
    exit(0)
read2 = ThermalDataReader.read_all_file(dir_name_2)

keyset1 = set(read1.keys())
keyset2 = set(read2.keys())
keyset = keyset1.intersection(keyset2)


no_diff = True
for key in keyset:
    print(key)
    spec1 = read1[key]
    spec2 = read2[key]
    coef1 = spec1.get_coefficients()
    coef2 = spec2.get_coefficients()
    for i in range(len(coef1)):
        if coef1[i] != coef2[i]:
            print("{} != {}".format(coef1[i], coef2[i]))
            no_diff = False

combine = messagebox.askyesno(title="Combine", message="Do you want to combine the data?")
if combine:
    for key in read2.keys():
        if key in keyset:
            continue
        else:
            read1[key] = read2[key]

    file = open(dir_name_1.split(".")[0] + "_combined.txt", "w")
    lines = list()
    for key,spec in read1.items():
        line = list("".ljust(80))
        line[0:8] = list(str(spec).ljust(8))
        line[8:24] = spec.comment

        for i in range(24, 44, 5):
            line[i+4] = str(0)
        i = 24
        for atom in spec.get_atoms().keys():
            name = str(atom)
            nr = str(spec.get_atoms()[atom])
            content = name.ljust(5-len(nr))
            content += nr
            line[i:i + 5] = content
            i += 5
        line[48:58] = "{:10.2F}".format(spec.get_temp_min()).rjust(10)
        line[58:68] = "{:10.2F}".format(spec.get_temp_max()).rjust(10)
        line[68:76] = "{:8.2F}".format(spec.get_temp_switch()).rjust(8)
        line[44] = reconvert_state(spec.state)
        line[79] = "1"
        lines.append("".join(line))

        line = ""
        i = 0
        nr = 2
        for coef in spec.get_coefficients():
            if coef is not None:
                line += "{:15.8E}".format(coef)
            else:
                line += " "*15
            i+=1
            if i >= 5:
                line = line.ljust(79)
                line = line + str(nr)
                lines.append(line)
                line = ""
                i = 0
                nr += 1
        if line != "":
            lines.append(line)

    file.write("\n".join(lines))
    file.close()



