import json

from Interfaces import EditorAdjusted, Checkable


# Relevant Adjust Data:
#   - T_ref -> Temp. range and range of extra importance
#   - Flag Weight -> Default weight for reactions marked
#   - Surface Site Name

class Surface:
    surface_side_density: float

    special_surface_species: dict[str, int]

    def __init__(self, surface_side_density = 0):
        self.surface_side_density = surface_side_density
        self.special_surface_species = {}

    def add_species(self, species, spaces: int = 1):
        self.special_surface_species[species] = spaces

    def __eq__(self, other):
        if self.special_surface_species != other.special_surface_species:
            return False
        return self.surface_side_density == other.surface_side_density

    def toJSON(self, pretty=False):
        if pretty:
            return json.dumps(
                self,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=2)
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True)

    def fromJSON(self, json_text):
        self.__dict__ = json.loads(json_text)



class TemperatureRange:
    T_min: int
    T_max: int
    T_step: int

    def __init__(self, T_min: int = 0, T_max: int = 0, T_step: int = 0):
        self.T_min = T_min
        self.T_max = T_max
        self.T_step = T_step

    def __eq__(self, other):
        if not isinstance(other, TemperatureRange):
            return False
        if self.T_step != other.T_step:
            return False
        if self.T_min != other.T_min:
            return False
        if self.T_max != other.T_max:
            return False
        return True

    def toJSON(self, pretty=False):
        if pretty:
            return json.dumps(
                self,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=2)
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True)

    def fromJSON(self, json_text):
        self.__dict__ = json.loads(json_text)
        if not isinstance(self.T_min, int):
            raise TypeError("T_min needs to be an integer")
        if not isinstance(self.T_max, int):
            raise TypeError("T_max needs to be an integer")
        if not isinstance(self.T_step, int):
            raise TypeError("T_step needs to be an integer")

class AdjustDataHolder(EditorAdjusted, Checkable):
    T_ref_value: list[TemperatureRange]
    flag_weight_value: float
    surface_side_value: dict[str, Surface]


    def __init__(self, T_ref: list[TemperatureRange] = None, flag_weight: float = 1, surface_side: dict[str, Surface] = None):
        if T_ref is not None:
            self.T_ref_value = T_ref
        else:
            self.T_ref_value = list()
        self.flag_weight_value = flag_weight
        if surface_side is not None:
            self.surface_side_value = surface_side
        else:
            self.surface_side_value = dict()
        self.T_ref_comment = "Each temperatur range specifies a area to fit the energy balance. Only one is required, enter more ranges if certain ranges are more important."
        self.flag_weight_comment = "All flagged reactions get this weight"
        self.surface_side_comment = "All Surface sides. The name will given, will be searched in the species to determine the surface species. If a species does not follow that convention or requires more than one side, add it in the special_surface_species dictionary."

    def __eq__(self, other):
        if not isinstance(other, AdjustDataHolder):
            return False
        if self.T_ref_value != other.T_ref_value:
            print("T_ref_value Diff")
            return False
        if self.flag_weight_value != other.flag_weight_value:
            print("flag_weight_value Diff")
            return False
        if self.surface_side_value != other.surface_side_value:
            print("Surface Diff")
            return False
        return True

    def toJSON(self, pretty = False):
        if pretty:
            return json.dumps(
                self,
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=2)
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True)

    def fromJSON(self, json_text):
        self.__dict__ = json.loads(json_text)
        for key in self.surface_side_value:
            surface = Surface()
            surface.fromJSON(json.dumps(self.surface_side_value[key]))
            self.surface_side_value[key] = surface
        for i in range(len(self.T_ref_value)):
            t_range = TemperatureRange()
            t_range.fromJSON(json.dumps(self.T_ref_value[i]))
            self.T_ref_value[i] = t_range

    def check(self) -> bool:
        return True

