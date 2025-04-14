from Interfaces import Checkable, SelfFixing
import tkinter.messagebox

class Reaction(Checkable, SelfFixing):

    educts: dict[str,int]
    products: dict[str,int]
    orders: dict[str,float]
    epsilon: dict[str,float]
    A_k = 0
    beta_k = 0
    E_k = 0
    is_sticky = False
    reversible = False
    is_disabled = False
    category = ""

    def __init__(self, category:str, educts=None, products=None, A_k = 0, beta_k = 0, E_k = 0, is_sticky = False, is_reversible = False, is_disabled = False):
        self.orders = {}
        self.epsilon = {}
        if products is None:
            products = {}
        if educts is None:
            educts = {}
        self.educts = educts
        self.products = products
        self.A_k = A_k
        self.beta_k = beta_k
        self.E_k = E_k
        self.is_sticky = is_sticky
        self.is_reversible = is_reversible
        self.is_disabled = is_disabled
        self.category = category

    def __str__(self):
        text = ""
        for key, value in self.educts.items():
            text += str(value) + str(key) + " + "
        text= text[:-3]
        text = text.ljust(25)
        if self.is_reversible:
            text = text + " <-> "
        else:
            text = text + " -> "
        for key, value in self.products.items():
            text += str(value) + str(key) + " + "
        text= text[:-3]
        text= text.ljust(55)
        text += " | "
        text = text.ljust(60)
        text= text + "{:10.3E}".format(self.A_k).rjust(10) + "   "
        beta_str = "{:g}".format(self.beta_k)
        text= text + beta_str.rjust(7) + "   "
        text= text + "{:g}".format(self.E_k).rjust(10) + "   "
        if self.is_sticky:
            text= text + "stick"
        text = text.ljust(105)
        if self.is_disabled:
            text= text + "disabled"
        text = text.ljust(120)
        return text

    def check(self) -> bool:
        total_spec = 0
        for key, value in self.educts.items():
            total_spec += value
        for key, value in self.products.items():
            total_spec += value
        if total_spec > 5:
            tkinter.messagebox.showinfo(title="Reaction Error", message="Reduce number of educts and products to 5")
            return False
        return True

    def fix(self) -> None:
        self.educts = {k: v for k, v in self.educts.items() if v>0}
        self.products = {k: v for k, v in self.products.items() if v>0}
        self.epsilon = {k: v for k, v in self.epsilon.items() if v!=0}
        self.orders = {k: v for k, v in self.orders.items() if v!=0}


