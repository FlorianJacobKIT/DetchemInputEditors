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
            data.comment = content[21]
            data.low_temperature = float(content[22])
            data.high_temperature = float(content[23])
            data.jump_temperature = float(content[24])
            for i in range(14):
                data.coefficients.append(float(content[25+i]))
    od = dict(sorted(storage.items(), key=lambda item: item[0]))
    return od

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
        source.package = content[4]
        source.source_type = content[5]
        source.link = content[6]
        source.comment = content[7]

    od = dict(sorted(storage.items(), key=lambda item: item[1].creation_date))
    return od








