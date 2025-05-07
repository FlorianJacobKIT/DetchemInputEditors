
class inptag(list):
    def __init__(self, name, parent=None):
        super().__init__()
        self.parent=parent
        self.name=name.upper()
        self.attr=""
    def __repr__(self):
        return '<'+self.name+'>'
    def items(self):
        return [i for linenr,i in self]
    def word_iterator(self):
        for i in list(self.items()):
            if not isinstance(i,inptag):
                for j in i.replace("="," ").split():
                    yield j
    def get_tag(self,name):
        name=name.upper()
        for i in list(self.items()):
            if isinstance(i,inptag):
                if i.name==name: return i
        return None
    def get_option(self,name):
        def _evaluate_text(s):
            found=False
            for i in s.replace("="," ").split():
                if found : return i
                found=(name==i.upper())
            return None
        name=name.upper()
        value= _evaluate_text(self.attr)
        if value != None : return value
        L=[]
        for i in list(self.items()):
            if isinstance(i,str):
                L.append(i)
            else:
                L.append("<>")
        return _evaluate_text(" ".join(L))
##        for i in self.items():
##            if not isinstance(i,inptag):
##                value = _evaluate_text(i)
##                if value : return value
##        return None
    def __getitem__(self,name):
        i=self.get_tag(name)
        if i : return i
        return self.get_option(name)
    def get_float(self,name,default=None):
        try:
            return float(self.get_option(name))
        except:
            return default
    def fulltext(self,indent=0):
        L=[]
        L.append(" "*indent+"<"+self.name)
        if self.attr!="": L.append(" "+self.attr)
        L.append(">\n")
        for i in list(self.items()):
            if isinstance(i,inptag):
                L.append(i.fulltext(indent+2))
            else:
                L.append(" "*(indent+2)+i+'\n')        
        L.append(" "*indent+"</"+self.name+">\n")
        return "".join(L)

def inp_error(linenr,linetext,errortext):
    print("Error in line ",linenr)
    print(linetext)
    print(errortext)
    raise ValueError

class inpfile(inptag):
    def __init__(self,filename):
        inptag.__init__(self,filename)
        self.append_file(filename,self)

    def append_file(self,filename,currlist):
        def parse_error(text):
            inp_error(linenr,line,text)
                
        linenr=0
        print("reading",filename)
        for line in open(filename.strip('"')):
            linenr+=1
            line=line.split("#")[0]
            ## print line.rstrip()

            # check for include statements
            if line.strip()[:8]=="{include" :
                self.append_file(line.strip()[1:-1].split()[1],currlist)
                continue

            # separate tags
            lineitems=[s.strip() for s in line.split('<')]
            if len(lineitems[0]) :
                # text outside of a tag
                currlist.append((linenr,lineitems[0]))
            for item in lineitems[1:]:
                # evaluate tag
                try:
                    i=item.index('>')
                except ValueError:
                    parse_error("Missing '>' at end of tag")
                tag=item[:i].strip()
                value=item[i+1:].strip()
                if tag[0:1]=="/": # closing tag
                    if tag[1:].upper()==currlist.name:
                        currlist=currlist.parent
                    else:
                        parse_error("Wrong closing tag - expecting </"+
                                    currlist.name+">")
                else: # opening tag
                    newlist=inptag(tag.split()[0],currlist)
                    currlist.append((linenr,newlist))
                    currlist=newlist
                    currlist.attr=tag[len(currlist.name):].strip()
                if len(value): # items
                    currlist.append((linenr,value))

