import collections
import datetime

from ChemDataManager.ChemDataFormat import ChemData
from ChemDataManager.SourceFormat import Source


def readChemData() -> dict[str, tuple[list[ChemData],list[ChemData]]]:
    try:
        chemDataFile = open("ChemData.csv","r")
    except FileNotFoundError:
        chemDataFile = open("ChemDataManager/ChemData.csv","r")
    lines = chemDataFile.readlines()
    chemDataFile.close()
    storage: dict[str, tuple[list[ChemData],list[ChemData]]] = dict()
    for line in lines[1:]:
        content = line.split(";")
        ID = int(content[0])
        data = ChemData(ID)
        data.species = content[1]
        if data.species not in storage:
            storage[data.species] = ([],[])

        data.source = int(content[2])
        data.data_type = content[3]
        if content[3] == "MolData":
            storage[data.species][0].append(data)
            data.geometry = int(content[4])
            data.molar_mass = float(content[5])
            data.lennard_jones_potential = float(content[6])
            data.lennard_jones_collision = float(content[7])
            data.dipole_moment = float(content[8])
            data.polarizability = float(content[9])
            data.rotational_relaxation_collision_number = float(content[10])
            data.comment_chem = content[11]
            data.approx_molar_mass()

        if content[3] == "ThermData":
            storage[data.species][1].append(data)
            # ID;Spezies;Source;DataType;11;Atom1;Count;Atom2;Count;Atom3;Count;Atom4;Count;Type;Comment;Low temperature;High temperature ;Jump temperature ;Coef1;Coef2;Coef3;Coef4;Coef5;Coef6;Coef7;Coef8;Coef9;Coef10;Coef11;Coef12;Coef13;Coef14
            #print(line)
            for i in range(4):
                spec = content[12+2*i]
                count = content[12+2*i+1]
                if spec == "":
                    continue
                data.atoms[spec] = int(count)
            data.state = content[20]
            data.comment_therm = content[21]
            data.low_temperature = float(content[22])
            data.high_temperature = float(content[23])
            data.jump_temperature = float(content[24])
            data.molar_mass = -1
            data.approx_molar_mass()
            for i in range(14):
                data.coefficients.append(float(content[25+i]))
    od = dict(sorted(storage.items(), key=lambda item: item[0]))
    return od

def writeChemData(storage: dict[str, tuple[list[ChemData],list[ChemData]]]) -> None:
    try:
        open("ChemData.csv","r")
        chemDataFile = open("ChemData.csv","w")
    except FileNotFoundError:
        open("ChemDataManager/ChemData.csv","r")
        chemDataFile = open("ChemDataManager/ChemData.csv","w")

    header = "ID;Spezies;Source;DataType;Geometry;Molar_Mass;Lennard_Jones_potential;Lennard_Jones_collision;Dipole_moment;Polarizability;Rotational_relaxation_collision_number;Comment;Atom1;Count;Atom2;Count;Atom3;Count;Atom4;Count;Type;Comment;Low temperature;High temperature ;Jump temperature ;Coef1;Coef2;Coef3;Coef4;Coef5;Coef6;Coef7;Coef8;Coef9;Coef10;Coef11;Coef12;Coef13;Coef14\n"
    chemDataFile.write(header)

    line_id = 0
    for key, data_tuple in storage.items():
        chem_list = data_tuple[0]
        for species in chem_list:
            chemDataFile.write(str(line_id) + ";")
            chemDataFile.write(species.species + ";")
            chemDataFile.write(str(species.source) + ";")
            chemDataFile.write(species.data_type + ";")
            chemDataFile.write(str(species.geometry) + ";")
            if species.mass_approx:
                chemDataFile.write(str(-1) + ";")
            else:
                chemDataFile.write(str(species.molar_mass) + ";")
            chemDataFile.write(str(species.lennard_jones_potential) + ";")
            chemDataFile.write(str(species.lennard_jones_collision) + ";")
            chemDataFile.write(str(species.dipole_moment) + ";")
            chemDataFile.write(str(species.polarizability) + ";")
            chemDataFile.write(str(species.rotational_relaxation_collision_number) + ";")
            chemDataFile.write(species.comment_chem + ";")
            chemDataFile.write("\n")
            line_id += 1

        therm_list = data_tuple[1]
        for species in therm_list:
            chemDataFile.write(str(line_id) + ";")
            chemDataFile.write(species.species + ";")
            chemDataFile.write(str(species.source) + ";")
            chemDataFile.write("ThermData;;;;;;;;;")
            atoms = species.atoms
            elements = list(atoms.items())
            for i in range(4):
                try:
                    element = elements[i]
                    chemDataFile.write(str(element[0]) + ";")
                    chemDataFile.write(str(element[1]) + ";")
                except IndexError:
                    chemDataFile.write(";")
                    chemDataFile.write(";")
            chemDataFile.write(species.state + ";")
            chemDataFile.write(species.comment_therm + ";")
            chemDataFile.write(str(species.low_temperature) + ";")
            chemDataFile.write(str(species.high_temperature) + ";")
            chemDataFile.write(str(species.jump_temperature) + ";")
            text = ""
            for coef in species.coefficients:
                text += str(coef) + ";"
            text = text[:-1]
            chemDataFile.write(text)
            chemDataFile.write("\n")
            line_id += 1



def readLibData() -> dict[int, Source]:
    try:
        chemDataFile = open("Sources.csv","r")
    except FileNotFoundError:
        chemDataFile = open("ChemDataManager/Sources.csv","r")

    lines = chemDataFile.readlines()
    chemDataFile.close()
    storage: dict[int, Source] = dict()
    # ID;Author;Title;Creation_Data;Publisher;Source_Type;Link
    for line in lines[1:]:
        content = line.split(";")
        source = Source(int(content[0]))
        storage[source.ID] = source
        source.author = content[1]
        source.title = content[2]
        if content[3] != "":
            source.creation_date = datetime.datetime.strptime(content[3],"%d.%m.%Y").date()
        source.publisher = content[4]
        source.source_type = content[5]
        source.link = content[6]
        source.comment = content[7][:-1]

    od = dict(sorted(storage.items(), key=lambda item: item[1].creation_date))
    return od


def writeLibData(storage: dict[int, Source]) -> None:
    try:
        open("Sources.csv","r")
        chemDataFile = open("Sources.csv","w")
    except FileNotFoundError:
        open("ChemDataManager/Sources.csv", "r")
        chemDataFile = open("ChemDataManager/Sources.csv","w")

    header = "ID;Author;Title;Creation_Data;Publisher;Source_Type;Link;Comment\n"
    chemDataFile.write(header)
    # ID;Author;Title;Creation_Data;Publisher;Source_Type;Link
    for id, source in storage.items():
        chemDataFile.write(str(id) + ";")
        chemDataFile.write(str(source.author) + ";")
        chemDataFile.write(str(source.title) + ";")
        chemDataFile.write(datetime.datetime.strftime(source.creation_date, "%d.%m.%Y") + ";")
        chemDataFile.write(str(source.publisher) + ";")
        chemDataFile.write(str(source.source_type) + ";")
        chemDataFile.write(str(source.link) + ";")
        chemDataFile.write(str(source.comment))
        chemDataFile.write("\n")









