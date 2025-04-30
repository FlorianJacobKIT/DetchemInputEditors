from subprocess import call

import SelectionDialog

keys = ["MechanismEditor"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                   keys).center().show()
if mode == "":
    exit(0)

call(["python", mode + ".py"])