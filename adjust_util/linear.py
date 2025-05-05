# purpose: check if a given list of vectors contains vectors that are no
#          linear combination of others, identify the linear idependent vectors

# The vectors shall be stored as dictionaries with integer values.

# idea : A vector can be written as a linear combination iff it belongs to
#        a circuit. Use Gauss elimination to identify circuits.

def gcd(a,b):
    while b:
        a,b = b,a%b
    return a

def VDICT(*vector,**d):
    for i in range(len(vector)):
        if vector[i] : d[str(i)]=vector[i]
    return d
        
class ddict(object):
    def __init__(self,left={},right={}):
        self.left=left.copy()
        self.right=right.copy()

def lincomb(r1,d1,r2,d2):
    d=ddict()
    t=0
    for i in set(d1.left.keys()) | set(d2.left.keys()):
        s=r1*d1.left.get(i,0) + r2*d2.left.get(i,0)
        if s:
            d.left[i]=s
            t=gcd(t,s)
    for i in set(d1.right.keys()) | set(d2.right.keys()):
        s=r1*d1.right.get(i,0) + r2*d2.right.get(i,0)
        if s:
            d.right[i]=s
            t=gcd(t,s)
    if abs(t)>1:
        for i in d.left : d.left[i]//=t
        for i in d.right: d.right[i]//=t       
    return d


def find_independents(list_of_vdicts):
    independent=[True]*len(list_of_vdicts)

    # set up scheme A*x=I*y
    v=[]
    for i in range(len(list_of_vdicts)):
        d=ddict(list_of_vdicts[i],{i:1})
        v.append(d)
    
    # use Gaussian algorithm to eiliminate columns
    while len(v):
        row=v.pop()
        if len(row.left):
            # non-zero row : use it for elimination
            col=list(row.left.keys())[0]
            for i in range(len(v)):
                if col in v[i].left:
                    v[i]=lincomb(row.left[col],v[i],-v[i].left[col],row)
        else:
            # row of zeros indicates a circuit
            for i in row.right:
                independent[i]=False
    return independent

def find_dependents(base,vectors): # base and vectors are lists of vdicts
    # fill all vdicts in one list of ddicts
    v=[ddict(i) for i in base] + [ddict(i) for i in vectors]
    # use Gaussian elimination
    for i in range(len(base)):
        row=v.pop(0)
        if len(row.left):
            # do an elimination
            col=list(row.left.keys())[0]
            for j in range(len(v)):
                if col in v[j].left:
                    v[j]=lincomb(row.left[col],v[j],-v[j].left[col],row)
        else:
            pass # no action necessary
    return [len(i.left)==0 for i in v]
    

def _test_linear_(size=10):
    from random import random
    L=[]
    for i in range(size):
        L.append(VDICT(*[int(random()+5./size) for j in range(size)]))
    for d,r in zip(L,find_independents(L)):
        print(r,d)
                    
# _test_linear_(200)    
    
