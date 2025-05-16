import GeneralUtil.MaterialData
import GeneralUtil.ThermalDataReader

bark_mol = open("berkeley_moldata.txt", "r")
all_data = open("ChemData.csv", "w")
content = bark_mol.read()
header = "ID;Spezies;Source;DataType;Geometry;Molar_Mass;Lennard_Jones_potential;Lennard_Jones_collision;Dipole_moment;Polarizability;Rotational_relaxation_collision_number;Comment;Atom1;Count;Atom2;Count;Atom3;Count;Atom4;Count;Type;Comment;Low temperature;High temperature ;Jump temperature ;Coef1;Coef2;Coef3;Coef4;Coef5;Coef6;Coef7;Coef8;Coef9;Coef10;Coef11;Coef12;Coef13;Coef14\n"
all_data.write(header)
line_id = 0
for line in content.splitlines():
    spec = line[:19].strip()
    Source = "0"
    DataType = "MolData"
    Geometry =int(line[19].strip())
    Molar_Mass = -1
    Lennard_Jones_potential = float(line[20:30].strip())
    Lennard_Jones_collision = float(line[30:40].strip())
    Dipole_moment = float(line[40:50].strip())
    Polarizability = float(line[50:60].strip())
    Rotational_relaxation_collision_number = float(line[60:70].strip())
    Comment = line[70:].strip()
    all_data.write(str(line_id) + ";")
    all_data.write(spec + ";")
    all_data.write(Source + ";")
    all_data.write(DataType + ";")
    all_data.write(str(Geometry) + ";")
    all_data.write(str(Molar_Mass) + ";")
    all_data.write(str(Lennard_Jones_potential) + ";")
    all_data.write(str(Lennard_Jones_collision) + ";")
    all_data.write(str(Dipole_moment) + ";")
    all_data.write(str(Polarizability) + ";")
    all_data.write(str(Rotational_relaxation_collision_number) + ";")
    all_data.write(Comment + ";")
    all_data.write("\n")
    line_id += 1


bark_mol.close()

content = GeneralUtil.ThermalDataReader.read_thermdata_file("berkeley_thermdata.txt")


for spec in content:
    species = content[spec]
    all_data.write(str(line_id) + ";")
    all_data.write(species.name + ";")
    all_data.write("0;ThermData;;;;;;;;;")
    atoms = species.get_atoms()
    elements =list(atoms.items())
    for i in range(4):
        try:
            element = elements[i]
            all_data.write(str(element[0]) + ";")
            all_data.write(str(element[1]) + ";")
        except IndexError:
            all_data.write(";")
            all_data.write(";")
    all_data.write(GeneralUtil.MaterialData.reconvert_state(species.state) + ";")
    all_data.write(species.comment.strip() + ";")
    all_data.write(str(species.get_temp_min()) + ";")
    all_data.write(str(species.get_temp_max()) + ";")
    all_data.write(str(species.get_temp_switch()) + ";")
    text = ""
    for coef in species.get_coefficients():
        text += str(coef) + ";"
    text = text[:-1]
    all_data.write(text)
    all_data.write("\n")
    line_id += 1









