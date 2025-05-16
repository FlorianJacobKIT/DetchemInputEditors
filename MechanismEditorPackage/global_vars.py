from MechanismEditorPackage import Reaction_Class
from GeneralUtil.MaterialData import Species

reactions: dict[str,list[Reaction_Class.Reaction]] = dict()
species: dict[str,Species|None] = dict()


thermalDataMap: dict[str, Species]
originalDataMap: dict[str, Species]
parent: str

file_prefix: list[str]
dir_name: str