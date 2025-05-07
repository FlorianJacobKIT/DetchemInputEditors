import tkinter

from MechanismEditorPackage import global_vars, Config
from MechanismEditorPackage.CenterGui import CenterWindow
from MechanismEditorPackage.adjustclass import AdjustClass


class SpeciesDisplayGUI(CenterWindow):

    scale_var: tkinter.DoubleVar
    text_box: tkinter.Message

    def __init__(self, parent, data: AdjustClass):
        super().__init__(master= parent)
        self.scale_var = tkinter.DoubleVar()
        self.scale_var.set(data.T_min)
        scale = tkinter.Scale(self, from_=data.T_min, to=data.T_max, tickinterval=50, variable=self.scale_var, orient=tkinter.HORIZONTAL)
        scale.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.EW)
        self.scale_var.trace_add("write",lambda a,b,c: self.update_text(scale.get()))
        text = ""
        for spec_name in global_vars.thermalDataMap.keys():
            spec = global_vars.thermalDataMap[spec_name]

            text += "{:8s}   cp={:6.2f}   H0={:8.0f}   S0={:6.2f}".format( str(spec),spec.get_cp(data.T_min),spec.get_h(data.T_min),spec.get_s(data.T_min))
            text += "\n"
        self.text_box = tkinter.Message(self,text=text, font=("FixedSys", Config.text_size - 4))
        self.text_box.grid(row=1, column=0, padx=10, pady=10)

    def update_text(self, temp):
        text = ""
        for spec_name in global_vars.thermalDataMap.keys():
            spec = global_vars.thermalDataMap[spec_name]
            text += "{:8s}   cp={:6.2f}   H0={:8.0f}   S0={:6.2f}".format( str(spec),spec.get_cp(temp),spec.get_h(temp),spec.get_s(temp))
            text += "\n"
        self.text_box.config(text=text)


    def show(self):
        self.wm_deiconify()
        self.wait_window()
