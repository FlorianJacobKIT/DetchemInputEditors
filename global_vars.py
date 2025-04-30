import Reaction_Class
from adjust_util.MaterialData import Species

reactions: dict[str,list[Reaction_Class.Reaction]] = dict()
species: dict[str,Species|None] = dict()


thermalDataMap: dict[str, Species]
defaultMapping: dict[str,str]
parent: str