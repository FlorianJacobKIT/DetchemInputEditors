from subprocess import call

from MechanismEditorPackage import SelectionDialog

keys = ["MechanismEditor","ThermalDataCompare"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                     keys).center().show()
if mode == "":
    exit(0)

if mode == "MechanismEditor":
    import MechanismEditorPackage.MechanismEditor
if mode == "ThermalDataCompare":
    import ThermalDataComparePackage.ThermalDataCompare