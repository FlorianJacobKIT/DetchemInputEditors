from GeneralUtil import SelectionDialog

keys = ["MechanismEditor","ThermalDataCompare","ChemDataManager"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                     keys).center().show()
if mode == "":
    exit(0)

if mode == "MechanismEditor":
    from MechanismEditorPackage import MechanismEditor
    editor = MechanismEditor
if mode == "ThermalDataCompare":
    from ThermalDataComparePackage import ThermalDataCompare
    editor = ThermalDataCompare
if mode == "ChemDataManager":
    from ChemDataManager.GUIs import SelectionGui
    editor = SelectionGui
