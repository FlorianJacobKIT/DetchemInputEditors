import tkinter
from subprocess import call

import SelectionDialog

keys = ["MechanismEditor"]

mode = SelectionDialog.GeneralDialog("Select Input File Editor",
                                   keys).center().show()

call(["python", mode + ".py"])