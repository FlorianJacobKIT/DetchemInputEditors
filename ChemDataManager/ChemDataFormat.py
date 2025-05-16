

class ChemData():
    ID: int
    species: str
    source: int
    data_type: str
    geometry: int
    molar_mass: float
    lennard_jones_potential: float
    lennard_jones_collision: float
    dipole_moment: float
    polarizability: float
    rotational_relaxation_collision_number: float
    comment_chem: str
    atoms: dict[str, int]
    state: str
    comment_therm: str
    low_temperature: float
    high_temperature: float
    jump_temperature: float
    coefficients: list[float]

    def __init__(self, ID:int):
        self.ID = ID
        self.atoms = {}
        self.coefficients = []

    def __str__(self):
        content = str(self.ID) + ": {name:" + str(self.species) + ","
        content += "type:" + str(self.data_type) + "}"
        return content






