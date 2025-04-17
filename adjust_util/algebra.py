
import math

def gcd(a,b):
    while(b):
        a,b=b,a%b
    return abs(a)

def lcm(a,b):
    return a//gcd(a,b)*b

def isint(x):
    if isinstance(x,int): return True
    if isinstance(x,int): return True
    return False

def integerize(x):
    if isint(x): return x,1
    if x==0.: return 0,1
    fac=1
    while abs(x)<1.e16:
        x,fac=2*x,2*fac
    x=int(x)
    t=gcd(x,fac)
    return x//t,fac//t
    

class LinearCombination(object):
    def __init__(self,c=0):
        self.d=dict()  # key of arbitrary type ("EquationVariable")
        self.c=c       # constant value
    def copy(self):
        C=LinearCombination()
        C.d=self.d.copy()
        C.c=self.c
        return C
    def __str__(self):
        s=""
        for i,a in list(self.d.items()):
            if a!=1 : s=s+str(a)+" "
            s=s+"<"+str(i)+"> + "
        if self.c or len(self.d)==0:
            return s+str(self.c)
        else:
            return s[:-3]
    def __add__(self,other):
        if isinstance(other,LinearCombination):
            result=LinearCombination(self.c+other.c)
            for key in set(self.d.keys())|set(other.d.keys()) :
                val=self.d.get(key,0)+other.d.get(key,0)
                if val : result.d[key]=val
            return result
        else:
            result=LinearCombination(self.c+other)
            result.d=self.d.copy()
            return result
    def __radd__(self,other):
        return self+other
    def __neg__(self):
        result=LinearCombination(-self.c)
        for key in self.d:
            result.d[key]=-self.d[key]
        return result
    def __sub__(self,other):
        return self+(-other)
    def __rsub__(self,other):
        return other+(-self)
    def __mul__(self,other):
        if not other : return LinearCombination()
        if isinstance(other,LinearCombination): raise ValueError
        result=LinearCombination(other*self.c)
        for key in self.d:
            result.d[key]=other*self.d[key]
        return result
    def __rmul__(self,other):
        return self*other
    def __div__(self,other):
        return self*(1./other)
    def __truediv__(self,other):
        return self*(1./other)
    def __floordiv__(self,other):
        result=LinearCombination(self.c//other)
        for key in self.d:
            result.d[key]=self.d[key]//other
        return result
    def __bool__(self):
        return bool(self.c) or len(self.d)>0
    def reduce_factor(self,f):
        for key in self.d:
            if isint(self.d[key]):
                self.d[key]//=f
            else:
                self.d[key]/=f
        if isint(self.c):
            self.c//=f
        else:
            self.c/=f
        
    def variables(self,instanceof=object):
        return [i for i in list(self.d.keys()) if isinstance(i,instanceof)]
    def coefficient(self,variable=None):
        if variable==None : return self.c
        return self.d.get(variable,0)
    def find_best_pivot(self):
        var=None
        c=0
        for var1,c1 in list(self.d.items()):
            if isint(c1):
                c1=abs(c1)
                if c1>c:
                    var,c=var1,c1
        if var!=None : return var
        for var1 in self.d:
            c1=abs(self.d[var1])
            if c1>c:
                var,c=var1,c1
        return var
                
    def simplify_gcd(self):
        t=0
        for i in list(self.d.values())+[self.c]:
            if isint(i) : t=gcd(i,t)
        if t:
            self.reduce_factor(t)
        return self
    
    def normalize(self):
        d1=d2=0
        for value in list(self.d.values()):
            d1=max([d1,abs(value)])
            d2+=value*value
        if d2>0:
            try:
                t=math.sqrt(d2)
            except:
                t=d1
            self.c/=t
            for key,value in list(self.d.items()):
                self.d[key] = value/t
        return self

    def integerize(self):
        fac=1
        for value in list(self.d.values())+[self.c]:
            try:
                x,f=integerize(value)
                fac=lcm(fac,f)
            except TypeError:
                return
        for key,value in list(self.d.items()):
            x,f=integerize(value)
            self.d[key] = x*fac//f
        x,f=integerize(self.c)
        self.c = x*fac//f 

    def replace(self,vdict,deep=False):
        for key,value in list(vdict.items()):
            if key in self.d:
                coeff=self.d[key]
                del self.d[key]
                if deep:
                    result = self + coeff * value
                    self.c = result.c
                    self.d = result.d
                else:
                    self.c += coeff * value
        return self

    def solve(self):
        assert(len(self.d)==1)
        key=list(self.d.keys())[0]
        return key , -self.c/self.d[key]

    def solve2(self):
        assert(len(self.d)>0)
        result=dict()
        c=self.c
        keys=list(self.d.keys())
        for key in keys[1:]:
            result[key]=EquationVariable(key)
            c+=self.d[key]*result[key]
        key=keys[0]
        result[key]=-c/self.d[key]
        return result
        
def EquationVariable(anyobject):
    v=LinearCombination()
    v.d[anyobject]=1
    return v

class LinearEquationSystem(list):
    def __str__(self):
        s=""
        for eq in self:
            s=s+str(eq)+'\n'
        return s
    def add(self,left,right=0):
        eq=left-right
        if eq : self.append(eq)
    def variables(self,instanceof=object):
        V=set()
        for eq in self:
            V=V | set(eq.variables(instanceof))
        return list(V)
    def replace(self,vdict,deep=False):
        for eq in self:
            eq.replace(vdict,deep)
    def eliminate(self,variable,return_pivot=False):
        L=[]
        pivot=None
        while len(self):
            eq=self.pop(0)
            c=eq.coefficient(variable)
            if c :
                if not pivot :
                    pivot=eq
                    cpivot=c
                else:
                    eq=cpivot*eq - c*pivot
                    if len(eq.variables()):
                        if isint(cpivot*c):
                            eq.simplify_gcd()
                        else:
                            eq.normalize()
                        L.append(eq)
            else:
                L.append(eq)
        self.extend(L)
        if return_pivot : return pivot
    def solve(self):
        # use integer arithmetics
        for eq in self:
            eq.integerize()
        L=[]
        while len(self):  # forward elimination
            eq=self[0]
            var=eq.find_best_pivot()
            L.append(eq)
            self.eliminate(var)
        vdict=dict()
        while len(L): # backward elimination
            eq = L.pop()
            # change back to floating point arithmetics
            eq.normalize()
            eq.replace(vdict)
            try:
                var,val=eq.solve()
                vdict[var]=val
            except AssertionError:
                result=eq.solve2()
                vdict.update(result)
            self.append(eq)
        return vdict
    def get_ATA(self): # calculate A^T . A
        ATA=LinearEquationSystem()
        for var in self.variables():
            eqsum=LinearCombination()
            for eq in self:
                eqsum += eq.coefficient(var) * eq
            ATA.append(eqsum)
        return ATA
    def linreg(self):
        return self.get_ATA().solve()
    def minimize_sum_of_squares(self,weight=dict()):
        MES=LinearEquationSystem()
        for eq in self:
            MES.append(eq.copy())
        variables=self.variables()
        for var in variables:
            me=weight.get(var,1) * EquationVariable(var)
            for i in range(len(self)):
                me += self[i].coefficient(var) * EquationVariable("lambda"+str(i))
            MES.append(me)            
        solution=MES.solve()
        return dict([(var,solution[var]) for var in variables])
        
