from ChemDataManager.ChemDataFormat import ChemData
from ChemDataManager.SourceFormat import Source

chemData: dict[str, tuple[list[ChemData],list[ChemData]]]
libData: dict[int, Source]