import math
from enum import Enum

import periodictable

from adjust_util import Errors
from adjust_util.Nat_Constants import R


class State(Enum):
   Gas = 1
   Liquid = 2
   Solid = 3
   Crystal = 4
   Unknown = 10

def convert_state(letter:str):
    if letter == "G":
        return State.Gas
    if letter == "L":
        return  State.Liquid
    if letter == "S":
        return State.Solid
    if letter == "C":
        return State.Crystal
    return State.Unknown
    #raise NameError("Value \"" + letter + "\" not convertable")




class Species:
    __coefficient: list
    __atoms: dict[periodictable.core.Isotope,float]
    __name:str
    __T_min:float
    __T_max:float
    __T_switch:float
    __error = NameError("Value not defined")

    def __hash__(self):
        return hash(self.__name)

    def __gt__(self, other):
        return self.__name > other.__name

    def __ge__(self, other):
        return self.__name >= other.__name

    def __le__(self, other):
        return self.__name <= other.__name

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__name == other.__name
        return False

    def __ne__(self, other):
        return self.__name != other.__name


    def __init__(self, name: str, state:State):
        self.__name = name
        self.state = state
        self.__coefficient = []
        self.__atoms = dict()

    def __str__(self):
        return self.__name

    def add_atom(self, isotop:periodictable.core.Isotope,number:int):
        self.__atoms[isotop] = number

    def get_atoms(self):
        return self.__atoms

    def get_weight(self):
        total_weight = 0
        isotop: periodictable.core.Isotope
        for isotop in self.__atoms.keys():
            total_weight += isotop.mass * self.__atoms[isotop]
        return total_weight

    def get_temp_coefficients(self, T: float):
        if T>self.__T_max:
            raise Errors.OutOfBoundError("temperature",T,self.__T_min,self.__T_max)
        if T<self.__T_min:
            raise Errors.OutOfBoundError("temperature",T,self.__T_min,self.__T_max)
        a = self.__coefficient[7:14]
        if T > self.get_temp_switch():
            a = self.__coefficient[:7]
        return a

    def get_cp(self, T: float):
        a = self.get_temp_coefficients(T)
        c_p = (a[0] + a[1] * T + a[2] * T ** 2 + a[3] * T ** 3 + a[4] * T ** 4) * R
        return c_p


    def get_h(self, T: float):
        a = self.get_temp_coefficients(T)
        h = (a[5] + a[0] * T + a[1] / 2 * T ** 2 + a[2] / 3 * T ** 3 + a[3] / 4 * T ** 4 + a[4] / 5 * T ** 5) * R
        return h

    def get_s(self, T: float):
        a = self.get_temp_coefficients(T)
        s = (a[6] + a[0] * math.log(T) + a[1] * T + a[2] / 2 * T ** 2 + a[3] / 3 * T ** 3 + a[4] / 4 * T ** 4) * R
        return s


    def add_coefficient(self, value):
        self.__coefficient.append(value)

    def get_coefficients(self):
        return self.__coefficient

    def set_temp_min(self, T_min:float):
        self.__T_min = T_min

    def set_temp_max(self, T_max:float):
        self.__T_max = T_max

    def set_temp_switch(self, T_switch:float):
        self.__T_switch = T_switch

    def get_temp_min(self):
        if self.__T_min is None:
            raise self.__error
        return self.__T_min

    def get_temp_max(self):
        if self.__T_max is None:
            raise self.__error
        return self.__T_max

    def get_temp_switch(self):
        if self.__T_switch is None:
            raise self.__error
        return self.__T_switch



    # def get_atomic_equation(self):
    #     atoms = self.get_atoms()
    #     atomMap = LDict()
    #     for atom in atoms:
    #         atomMap[str(atom)] = atoms[atom]
    #     return LEquation({self.get_name():1},atomMap)


