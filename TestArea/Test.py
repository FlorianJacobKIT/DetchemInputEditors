from ChemDataManager.ChemDataFormat import ChemData

textline = "IC4H8                 2   344.5   5.089   0.5 0.0 1.0 !   WJP"

splited = textline.split(" ")
while "" in splited:
    splited.remove("")

data = ChemData(-1)
data.source = 1
data.species = splited[0]
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

print(data)