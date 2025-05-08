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

read1 = ThermalDataReader.read_thermdata_file(dir_name_1)

dir_name_2 = filedialog.askopenfilename(title="Second Thermal Data File")
if dir_name_2 == "":
    exit(0)
read2 = ThermalDataReader.read_thermdata_file(dir_name_2)

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

    ThermalDataReader.write_thermdata_file(dir_name_1.split(".")[0] + "_combined.txt", read1)