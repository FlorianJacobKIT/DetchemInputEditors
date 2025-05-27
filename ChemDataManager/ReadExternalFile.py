import copy
import traceback
from tkinter import messagebox

import GeneralUtil.MaterialData
import GeneralUtil.ThermalDataReader
from ChemDataManager import global_vars
from ChemDataManager.ChemDataFormat import ChemData


def read_moldata(filename:str, source_id:int):
    bark_mol = open(filename, "r")
    content = bark_mol.readlines()
    bark_mol.close()
    backup = copy.deepcopy(global_vars.chemData)
    line = ""
    line_nr = -1
    try:
        for line_nr in range(len(content)):
            line = content[line_nr].strip("\n")
            if len(line) == 0:
                continue
            if line[0] == "!":
                continue
            if line.lower().startswith("end"):
                break
            data = ChemData(-1)
            data.source = source_id
            data.species = line[:19].strip()
            data.source = source_id
            data.dataType = "MolData"
            data.geometry =int(line[19].strip())
            data.molar_mass = -1
            data.lennard_jones_potential = float(line[20:30].strip())
            data.lennard_jones_collision = float(line[30:40].strip())
            data.dipole_moment = float(line[40:50].strip())
            data.polarizability = float(line[50:60].strip())
            data.rotational_relaxation_collision_number = float(line[60:70].strip())
            data.comment_chem = line[70:].strip()

            if data.species in global_vars.chemData:
                global_vars.chemData[data.species][0].append(data)
            else:
                global_vars.chemData[data.species] = ([data],[])
    except Exception:
        global_vars.chemData = copy.deepcopy(backup)
        print("Error in line " + str(line_nr) + " with content:\n" + line)
        traceback.print_exc()
        answer = messagebox.askokcancel("Failed Import", "Moldata doesn't follow positioning convention.\n \n Retry with flexible import?")
        if not answer:
            return -1
        line = ""
        line_nr = -1
        try:
            for line_nr in range(len(content)):
                line = content[line_nr].strip("\n")
                if len(line) == 0:
                    continue
                if line[0] == "!":
                    continue
                if line.lower().startswith("end"):
                    break
                splited = line.split(" ")
                while "" in splited:
                    splited.remove("")

                data = ChemData(-1)
                data.source = source_id
                data.species = splited[0]
                data.source = source_id
                data.dataType = "MolData"
                data.geometry = int(splited[1])
                data.molar_mass = -1
                data.lennard_jones_potential = float(splited[2])
                data.lennard_jones_collision = float(splited[3])
                data.dipole_moment = float(splited[4])
                data.polarizability = float(splited[5])
                data.rotational_relaxation_collision_number = float(splited[6])
                if len(splited) > 7:
                    comment = " ".join(splited[7:])
                    data.comment_chem = comment

                if data.species in global_vars.chemData:
                    global_vars.chemData[data.species][0].append(data)
                else:
                    global_vars.chemData[data.species] = ([data], [])
        except Exception:
            print("Error in line " + str(line_nr) + " with content:\n" + line)
            traceback.print_exc()
            global_vars.chemData = copy.deepcopy(backup)
            messagebox.showerror("Failed Import",
                                   "Moldata import failed with flexible import.  \n Line with error:\n\n" + line)
            return -1
        return 0


def read_thermdata(filename:str, source_id:int):
    content = GeneralUtil.ThermalDataReader.read_thermdata_file(filename)

    for spec in content:
        data = ChemData(-1)
        data.source = source_id
        species = content[spec]
        data.species = species.name
        for atom in species.get_atoms():
            data.atoms[str(atom)] = species.get_atoms()[atom]
        data.state = GeneralUtil.MaterialData.reconvert_state(species.state)
        data.comment_therm = species.comment.strip()
        data.high_temperature = species.get_temp_max()
        data.low_temperature = species.get_temp_min()
        data.jump_temperature = species.get_temp_switch()

        data.coefficients = species.get_coefficients()
        if spec in global_vars.chemData:
            global_vars.chemData[spec][1].append(data)
        else:
            global_vars.chemData[spec] = ([], [data])

    return 0



