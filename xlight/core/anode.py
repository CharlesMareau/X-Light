

from .. import config

class Anode():
    def __init__(self):
        self.name=None
        self.filename=None
        self.R=1.0
        self.lambda1=0.0
        self.lambda2=0.0
        self.isRead=False
    def Read(self):
        if self.isRead:
            return

        if self.filename is None:
            if self.name is None:
                raise Exception("Anode: Name is not set")
            ll=config.GetAnodeDict()
            if not self.name in ll.keys():
                raise Exception("Anode: File not found for "+self.name)
            self.filename=ll[self.name]

        lines=[]
        try:
            f=open(self.filename,"r")
            lines=f.readlines()
            f.close()
        except:
            raise Exception("Anode: Can not open/read file "+self.filename)

        msg="Anode: file "+self.filename+" is in a bad format"
        if (len(lines)<2):
            raise Exception(msg)
        data=lines[1].split()
        if (len(data)<3) :
            raise Exception(msg)

        try:
            self.lambda1=float(data[0])
            self.lambda2=float(data[1])
            self.R=float(data[2])
        except ValueError:
            raise Exception(msg)

        self.isRead=True

        
    def getLambda(self):
        self.Read()
        return (self.lambda1+self.R*self.lambda2)/(1.0+self.R)
