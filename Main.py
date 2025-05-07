from subprocess import call

from MechanismEditorPackage import SelectionDialog

keys = ["MechanismEditor","ThermalDataCompare"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                     keys).center().show()
if mode == "":
    exit(0)

call(["python", mode + "Package/" + mode + ".py"])