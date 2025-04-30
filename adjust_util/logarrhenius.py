import math

import adjust_util.algebra as algebra
from adjust_util.Nat_Constants import R


class logArrheniusTerm(object):  # term of form a + b*ln(T) + c/T
    def __init__(self,a=0.0,b=0.0,c=0.0):
        self.a=a
        self.b=b
        self.c=c
    def __repr__(self):
        return "logArrheniusTerm("+str(self.a)+","+str(self.b)+","+str(self.c)+")"
    def __call__(self,T):
        return self.a+self.b*math.log(T)+self.c/T
    def __add__(self,other):
        if isinstance(other,logArrheniusTerm):
            return logArrheniusTerm(self.a+other.a, self.b+other.b,
                                    self.c+other.c)
        elif isinstance(other,algebra.LinearCombination):
            return other+self
        else:
            return logArrheniusTerm(self.a+float(other),self.b,self.c)
    def __radd__(self,other):
        return logArrheniusTerm(self.a+float(other),self.b,self.c)
    def __neg__(self):
        return logArrheniusTerm(-self.a,-self.b,-self.c)
    def __sub__(self,other):
        return self+(-other)
    def __rsub__(self,other):
        return (-self)+other
    def __mul__(self,r):
        try:
            r1=float(r)
            return logArrheniusTerm(r1*self.a,r1*self.b,r1*self.c)
        except TypeError:
            return r*self
    def __rmul__(self,r):
        r=float(r)
        return logArrheniusTerm(r*self.a,r*self.b,r*self.c)
    def __div__(self,r):
        r=float(r)
        return logArrheniusTerm(self.a/r,self.b/r,self.c/r)
    def __truediv__(self,r):
        r=float(r)
        return logArrheniusTerm(self.a/r,self.b/r,self.c/r)
    def norm2(self,T1,T2):
        """integral from T1 to T2 over (a+b*ln(T)+c/T)**2 dT"""
        a,b,c = self.a,self.b,self.c
        I = lambda T,lnT : (a*a*T + b*b*T*(lnT*lnT-2*lnT+2) - c*c/T +
                            2*a*b*T*(lnT-1) + 2*a*c*lnT + b*c*lnT*lnT)
        return I(T2,math.log(T2)) - I(T1,math.log(T1))
    
def Arrhenius2log(A,beta,Ea):
    return logArrheniusTerm(math.log(A),beta,-Ea/R)
def log2Arrhenius(LAT):
    if LAT==0 : return (0,0,0)
    return (math.exp(LAT.a),LAT.b,-LAT.c*R)
def log2therm(LAT):
    # (cp/R,H0/R,S0/R)
    if LAT==0 : return (0,0,0)
    return (-LAT.b,LAT.c,-LAT.b-LAT.a)

def logArrheniusFit(log_k):
    a=algebra.EquationVariable("a")
    b=algebra.EquationVariable("b")
    c=algebra.EquationVariable("c")
    LES=algebra.LinearEquationSystem()
    for T in log_k:
        LES.add(log_k[T] , a+b*math.log(T)+c/T)
    assert(len(LES)>=3)
    x=LES.linreg()
    return logArrheniusTerm(x["a"],x["b"],x["c"])

