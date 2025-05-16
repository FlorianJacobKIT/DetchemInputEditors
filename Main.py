from subprocess import call

from MechanismEditorPackage import SelectionDialog

keys = ["MechanismEditor","ThermalDataCompare","ChemDataManager"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                     keys, None).center().show()
if mode == "":
    exit(0)

if mode == "MechanismEditor":
    import MechanismEditorPackage.MechanismEditor
if mode == "ThermalDataCompare":
    import ThermalDataComparePackage.ThermalDataCompare
if mode == "ChemDataManager":
    import  ChemDataManager.SelectionGui