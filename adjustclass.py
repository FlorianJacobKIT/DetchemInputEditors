
import math
import adjust_util.algebra
from adjust_util import inp
from adjust_util.logarrhenius import *

class AdjustClass(object):


    def __init__(self):
        self.infile=None
        self.outfilename="chem.adjust"
        self.slist=None
        self.mech=None
        self.weight=dict()
        self.adjustable=dict()
        self.Tref=[]
        self.Tmin=self.Tmax=None
        self.cov=dict()
        self.old2new=dict()

    def read_mechanism(self,infilename,flagweight=1):
        # read input file (CHEMINP format)
        try:
            self.infile=inp.inpfile(infilename)
            self.slist=adjust_util.species.SpeciesList(self.infile["SPECIES"])
            self.mech=mechanism.SurfaceMechanism(self.infile["MECHANISM"]["SURFACE"],self.slist)
        except AssertionError:
            print("ERROR reading file",infilename)
            print("file must be in CHEMINP format")
            raise RuntimeError
        # default weights
        self.weight=dict()
        self.adjustable=dict()
        for reac in self.mech.reactions():
            w=1
            self.adjustable[reac]=True
            if reac.cflag=="*" :
                if flagweight>0:
                    w=flagweight
                else:
                    self.adjustable[reac]=False
            if isinstance(reac,mechanism.StickSReaction): w*=4
            self.weight[reac]=w

    def read_Tref(self,adjust_inp):
        Tref_inp=adjust_inp["TREF"]
        if Tref_inp:
            self.Tref=[float(i) for i in Tref_inp.word_iterator()]
        else:
            self.Tref=[]
        if len(self.Tref)<2 :
            print("WARNING: No reference temperatures found. Using 300 - 1000 K")
            self.Tref=[float(i) for i in range(300,1001,50)]
        self.Tmin=min(self.Tref)
        self.Tmax=max(self.Tref)
        if len(self.Tref)==2 :
            self.Tref=[self.Tmin+(self.Tmax-self.Tmin)*i/20.
                       for i in range(21)]

    def read_cov(self,adjust_inp):
        self.cov=dict()
        cov_inp=adjust_inp["COV"]
        if cov_inp:
            spec=""
            dep=""
            for i in cov_inp.word_iterator():
                if i[0]=="$":
                    dep=i[1:]
                else:
                    spec=i
                    dep=i
                if spec!="":
                    try:
                        self.cov[dep].add(spec)
                    except:
                        self.cov[dep] = set([spec])
                else:
                    print("ERROR in section <COV> of adjust.inp")
                    print("section must start with a species name, not with a dependency ($)")
                    raise RuntimeError


    def adjust_rates(self):
        # for each pair of reversible reactions set up an equation like
        # log(kf)+xf -log(kr)-xr = log(Kc/Kp) - deltaG(T)/RT
        # deltaG(T)/RT = sum_gas(nu_i * g_i(T)/RT) + sum_surf(nu_i * y_i)
        # xf,xr,y_i are terms of type logArrheniusTerm
        # all given functions are fitted by a logArrheniusTerm
    
        LES=algebra.LinearEquationSystem()
        for freac,rreac in self.mech.reversibles():
            if rreac==None : continue
            lterm=algebra.LinearCombination()
            lterm += freac.get_logkf() - rreac.get_logkf()
            if self.adjustable[freac] : lterm += algebra.EquationVariable(freac)
            if self.adjustable[rreac] : lterm -= algebra.EquationVariable(rreac)
            rterm=algebra.LinearCombination()
            rconst=dict()
            for T in self.Tref:
                rconst[T]=( math.log(freac.Kp2Kc(T))
                            - freac.deltaG_const(T)/adjust_util.species.R0/T)
            rterm += logArrheniusFit(rconst)
            rterm -= freac.deltaG_RT_adjustable()
            LES.add(lterm,rterm)

##        print ">>1"
##        print LES

        # eliminate thermodynamic unknowns (y_i)
        LES2=algebra.LinearEquationSystem()
        while True:
            v=LES.variables(adjust_util.species.SurfaceSpecies)
            if len(v)==0 : break
            LES2.add(LES.eliminate(v[0],return_pivot=True))

##        print ">>2"
##        print LES

        # minimize Phi=sum(w_i * ||x_i||^2) with x_i fulfilling equations in LES
        # x_i = a_i + b_i * ln(T) + c_i / T
        # ||x_i||^2 = Integral_Tmin^Tmax x_i(T)^2 dT

        MES=algebra.LinearEquationSystem()
        variables=LES.variables() # these are the adjustable reactions
        I = lambda func : func(self.Tmax)-func(self.Tmin)
        Iaa = I(lambda T : T) # Integral 1 dT
        Ibb = I(lambda T : T*math.log(T)**2 - 2*T*math.log(T) + 2*T) # Integral ln^2(T) dT
        Icc = I(lambda T : -1./T) # Integral 1/T^2 dT
        Iab = 2*I(lambda T : T*math.log(T)-T) # Integral ln(T) dT
        Iac = 2*I(lambda T : math.log(T)) # Integral 1/T dT
        Ibc = 2*I(lambda T : math.log(T)**2/2) # Integral ln(T)/T dT

        Lagrange=lambda v,name: sum([LES[i].coefficient(v) *
                                     algebra.EquationVariable(name+str(i))
                                     for i in range(len(LES))])
        Adict=dict()
        Bdict=dict()
        Cdict=dict()
        for v in variables:
            a=algebra.EquationVariable("a"+str(v))
            b=algebra.EquationVariable("b"+str(v))
            c=algebra.EquationVariable("c"+str(v))
            Adict[v]=a
            Bdict[v]=b
            Cdict[v]=c
            # d Phi/d a_i = 0
            MES.add(self.weight[v] * (2*a*Iaa + b*Iab + c*Iac) + Lagrange(v,"A"))
            # d Phi/d b_i = 0
            MES.add(self.weight[v] * (2*b*Ibb + a*Iab + c*Ibc) + Lagrange(v,"B"))
            # d Phi/d c_i = 0
            MES.add(self.weight[v] * (2*c*Icc + a*Iac + b*Ibc) + Lagrange(v,"C"))
        # split original equations by equating coefficients
        for eq in LES:
            eqa=eq.copy()
            eqa.c=eqa.c.a  # constant must be of type logArrheniusTerm
            eqa.replace(Adict,True)
            MES.add(eqa)
            eqb=eq.copy()
            eqb.c=eqb.c.b  # constant must be of type logArrheniusTerm
            eqb.replace(Bdict,True)
            MES.add(eqb)
            eqc=eq.copy()
            eqc.c=eqc.c.c  # constant must be of type logArrheniusTerm
            eqc.replace(Cdict,True)
            MES.add(eqc)
           
##        print ">>3"
##        print MES

        x=MES.solve()

##        print ">>4"
##        for i in x: print i,"\t",x[i]
##        print ">>5"
##        print LES2
    
        # new mechanism , linear equations for thermdata
        OK=True
        for reac in variables:
            nreac=self.old2new[reac]
            X = logArrheniusTerm(x["a"+str(reac)],x["b"+str(reac)],x["c"+str(reac)])
            LES2.replace({reac:X},True)
            logkf = X + reac.get_logkf() 
            A,beta,Ea = log2Arrhenius(logkf)
            nreac.set_Ea(Ea)
            nreac.set_beta(beta)
            try:
                nreac.set_A(A)
            except ValueError:
                OK=False
                self.weight[reac]*=2
                print("Incrementing weight for reaction <", end=' ')
                print(reac.text(),"> to",self.weight[reac])

        # solve equations for thermdata
        
##        print ">>6"
##        print LES2

        y=LES2.solve()

##        print ">>7"
##        for i in y: print i,"\t",y[i]

        # use species with lowest cp as reference
        while True:
            done=True
            cp0=0
            for s,term in list(y.items()):
                try:
                    cp=-term.coefficient().b
                except AttributeError:
                    continue
                if cp<cp0 :
                    done=False
                    s0,term0,cp0=s,term,cp
            if done : break
            s1=term0.variables()[0]
            c1=term0.coefficient(s1)
            term0=term0-c1*algebra.EquationVariable(s1)
            term1=(algebra.EquationVariable(s0)-term0)
            if c1!=1:
                term1/=float(c1)
            for s in y:
                y[s].replace({s1:term1},True)
                    
##            print ">>8"
##            for i in y: print i,"\t",y[i]

        # convert to tuples (cp/R,H0/R,S0/R) and change thermdata
        errors=[]
        for i in y:
            try:
                i.set_adjusted(*log2therm(y[i].coefficient()))
            except AttributeError:
                errors.append(i)
        for i in errors:
            del y[i]
                
        for i in y:
            print("%8s   cp=%6.2f   H0=%8.0f   S0=%6.2f" %(str(i),i.cp(298.),i.H(298.),i.S(298.)))
                    
        return OK
        
    def adjust_cov(self):
        # coverage dependencies ....
        for cov,cov_dependent_species in list(self.cov.items()):
            print("adjusting $"+cov)
            # set up linear equations for coverage dependent thermdata (eps_i)
            # epsilon_r-epsilon_f = sum (nu_i * eps_i)
            LES1=algebra.LinearEquationSystem()
            LES2=algebra.LinearEquationSystem()
            for freac,rreac in self.mech.reversibles():
                eq=self.mech.get_cov_equation(freac,rreac,cov,cov_dependent_species)
                if eq!=None :
                    if not self.adjustable[freac] and not self.adjustable[rreac]:
                        LES1.add(eq)
                    else:
                        LES2.add(eq)

            # solve exact equations
            eps1=LES1.solve()
            LES2.replace(eps1,True)

            # solve linear regression
            eps=LES2.linreg()

            # merge exact and approximated solutions
            for s,val in list(eps1.items()) :
                if isinstance(val,algebra.LinearCombination):
                    eps[s]=val.replace(eps,False).coefficient()
                else:
                    eps[s]=val
            for s,val in list(eps.items()) :
                s.therm.set_adjusted_cov(cov,val)
                print("$"+cov+" of "+str(s)+" =",val)
            
            # new coverage dependencies in all reactions:
            for freac,rreac in self.mech.reversibles():
                # get old values of epsilon
                epsilon_f = freac.get_epsilon(cov)
                try:    epsilon_r = rreac.get_epsilon(cov)
                except: epsilon_r = 0
                # calculate new delta_epsilon
                eq=freac.get_covdependency_equation(cov_dependent_species)
                if eq==0:
                    if epsilon_r or epsilon_f:
                        print("WARNING: ")
                        print("Coverage dependency for species "+cov+" defined in equation")
                        print(freac.text()," (or reverse),")
                        print("but no participing species was defined as coverage dependent")
                        print("Coverage dependency will be removed from adjusted mechanism")
                        print()
                    continue
                delta_epsilon=eq.replace(eps).coefficient()
                if not delta_epsilon: continue
                # add difference to the "nicer" side of equation
                if epsilon_f :
                    if not epsilon_r:
                        # forward reaction coverage dependent
                        epsilon_f = epsilon_r - delta_epsilon
                    else:
                        # find larger term
                        if abs(epsilon_f)>=abs(epsilon_r):
                            epsilon_f = epsilon_r - delta_epsilon
                        else:
                            epsilon_r = epsilon_f + delta_epsilon
                else:
                    if epsilon_r:
                        # reverse reaction coverage dependent
                        epsilon_r = epsilon_f + delta_epsilon
                    else:
                        # make epsilon positive
                        if delta_epsilon > 0 :
                            epsilon_r = delta_epsilon
                        else:
                            epsilon_f = -delta_epsilon
                # add coverage dependency to new equations
                if epsilon_f:
                    self.old2new[freac].cov.append(mechanism.CoverageDependency
                                (spec=self.slist[cov],epsilon=epsilon_f))
                if epsilon_r and rreac:
                    self.old2new[rreac].cov.append(mechanism.CoverageDependency
                                (spec=self.slist[cov],epsilon=epsilon_r))

        
    def adjust(self):
        self.old2new=dict([(reac,reac.copy_forward())
                           for reac in self.mech.reactions()])
        OK=False
        for count in range(5) :
            if self.adjust_rates():
                OK=True
                break
        self.adjust_cov()
        return OK

    def write_mechanism(self):
        # write new mechanism
        outfile=open(self.outfilename,"w")
        outfile2=open(self.outfilename+".fixed","w")
        print("SURFACE MECHANISM", file=outfile2)
        print("writing",self.outfilename)
        for it1 in list(self.infile.items()):
            if str(it1)!="<MECHANISM>":
                print(it1.fulltext(), file=outfile)
            else:
                print("<MECHANISM>", file=outfile)
                for it2 in list(it1.items()):
                    if str(it2)!="<SURFACE>":
                        print(it2.fulltext(2), file=outfile)
                    else:
                        print("  <SURFACE "+it2.attr+">", file=outfile)

                        for reac in self.mech.reactions():
                            print(self.old2new[reac].fulltext(4), file=outfile)
                            print(self.old2new[reac].shorttext(), file=outfile2)
                        print("  </SURFACE>", file=outfile)
                print("</MECHANISM>", file=outfile)
        print("END", file=outfile2)
        outfile.close()
        outfile2.close()

    def __str__(self):
        string = ""
        string += "T_ref: " + str(self.Tref) + "\n"
        string += "T_max:" + str(self.Tmax) + "\n"
        string += "Species: \n"
        for species in self.slist:
            string += str(species) + "\n"
        #string += "Reactions: \n"
        #for reac in self.mech.mlist:
        #    string += str(reac) + "\n"
        return string


        

