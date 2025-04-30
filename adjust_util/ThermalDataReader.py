import os.path

import periodictable

import global_vars
from adjust_util.AdjustData import AdjustDataHolder
from adjust_util.MaterialData import Species, State, convert_state

issuetracker = dict()
issuetracker["missing value"] = []
issuetracker["formation error"] = []
issuetracker["chem. error"] = []

lineCounter = 0
def read_all_file(file_name: str, ad_data:AdjustDataHolder):
    global lineCounter
    global_vars.thermalDataMap = dict()
    if not os.path.isfile(file_name):
        raise FileNotFoundError("Could not find file " + file_name)
    file = open(file_name, "r")

    surfaces: dict[str, tuple[str, int]] = dict()
    for key,surface in ad_data.surface_side_value.items():
        surfaces[key] = (key , 1)
        for special in surface.special_surface_species:
            surfaces[special] = (key, surface.special_surface_species[special])


    lines = file.readlines()
    while 1 == 1:
        line = lines[lineCounter]
        lineCounter += 1
        if line.startswith("THERMO ALL"):
            file.readline()
            lineCounter += 1
            break
        if lineCounter>= len(lines):
            lineCounter = 0
            break

    table = periodictable.core.default_table(None)
    while 1 == 1:
        header = lines[lineCounter]
        if header.startswith("END"):
            break
        lineCounter += 1
        if header is None:
            break
        if len(header) == 0:
            break
        name = header[0:8].strip()
        species = Species(name, convert_state(header[44]))
        temp_list = header[45:].split()
        try:
            species.set_temp_min(float(temp_list[0]))
            species.set_temp_max(float(temp_list[1]))
            species.set_temp_switch(float(temp_list[2]))
        except ValueError:
            issuetracker["formation error"].append(lineCounter)
            print("Could not read temperature for " + name + " Received \"" + header[45:] + "\"")

        for i in range(24, 44, 5):
            data = header[i:i + 5].split()
            try:
                atom = data[0]  # atom name
                if atom == "0.":            # no more atoms listed
                    break
                n = int(float(data[1]))  # sometimes numbers are floats
            except IndexError:
                continue
            except Exception as error:
                issuetracker["chem. error"].append(lineCounter)
                print("Exception occurred for " + name + ":", error)
                continue
            atom = atom.capitalize()
            if atom == "E": # ignore electrons
                continue
            try:
                if n: species.add_atom(table.isotope(atom), n)
            except:
                print("Could not convert \"" + atom + "\" from " + name)

        for section in range(3):
            line = lines[lineCounter]
            lineCounter += 1
            for i in range(5):
                try:
                    value = float(line[15 * i:15 * (i + 1)])
                    species.add_coefficient(value)
                except ValueError:
                    # Catch Double Values for example 0.10431658D+02
                    try:
                        value = float(line[15 * i:15 * (i + 1)].replace("D", "E"))
                        species.add_coefficient(value)
                    except ValueError:
                        if not(i==4 and section==2):
                            print("Error in data for " + name + " - Received at line " + str(lineCounter) + " for value " + str(i + 1) + ": " + line[15 * i:15 * (
                                    i + 1)].replace("D", "E"))
                        issuetracker["missing value"].append(lineCounter)
                        species.add_coefficient(None)

        species.check_adsorpt(surfaces, ad_data)
        global_vars.thermalDataMap[name] = species
    file.close()




def find_species(species:str) -> Species:
    values: Species
    error = NameError("Species not found")
    values = global_vars.thermalDataMap.get(species, Species("", State.Unknown))
    if str(values) == "":
        if species in global_vars.defaultMapping:
            return global_vars.thermalDataMap[str(global_vars.defaultMapping[species])]
        alternativ = [x for x in global_vars.thermalDataMap.keys() if x.upper().startswith(species.upper())]
        if len(alternativ) > 0:
            print("Did not find:", species,"\nDid you mean: ")
            for chem in range(len(alternativ)):
                print(chem,":",alternativ[chem])
            answer = input("Enter number of wanted chemical:")
            if answer == "": answer = "0"
            if answer.isdecimal():
                try:
                    global_vars.defaultMapping[species] = alternativ[int(answer)]
                    species = str(alternativ[int(answer)])
                except:
                    raise error
            else:
                raise error
        else:
            raise error
    return  global_vars.thermalDataMap[species]






