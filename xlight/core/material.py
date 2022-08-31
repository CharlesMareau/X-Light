
import numpy as np
from ..config import *

class Material():
        def __init__(self):
                self.filename=None
                self.NPLANES=0
                self.System=None
                self.a=1.0
                self.b=1.0
                self.c=1.0
                self.alpha=0.0
                self.beta=0.0
                self.gamma=0.0
                self.h=[]
                self.k=[]
                self.l=[]
                self.E=[]
                self.nu=[]
                self.q=None
        def ImportName(self,typename:str):
                materials=GetMaterialDict()
                self.ImportFile(materials[typename])
        def ImportFile(self,filename:str):
                self.q=None
                self.filename=filename
                f = open(self.filename, "r")
                lines=f.readlines()
                f.close()
                lines = [line.rstrip() for line in lines]
                if len(lines)<7:
                        raise Exception("Material: filename "+filename+" is in a bad format")
                self.System=lines[2]
                latice=lines[4].split()
                if (len(latice)!=6):
                        raise Exception("Material: filename "+filename+" is in a bad format")
                self.a=float(latice[0])
                self.b=float(latice[0])
                self.c=float(latice[0])
                self.alpha=float(latice[0])*np.pi/180.0
                self.beta=float(latice[0])*np.pi/180.0
                self.gamma=float(latice[0])*np.pi/180.0
                self.NPLANES=len(lines)-6
                if self.NPLANES<1:
                        raise Exception("Material: filename "+filename+" is in a bad format")
                self.h=np.zeros(self.NPLANES,dtype=float)
                self.k=np.zeros(self.NPLANES,dtype=float)
                self.l=np.zeros(self.NPLANES,dtype=float)
                self.E=np.zeros(self.NPLANES,dtype=float)
                self.nu=np.zeros(self.NPLANES,dtype=float)
                for i in range(self.NPLANES):
                        plan=lines[6+i].split()
                        if len(plan)!=5:
                                self.NPLANES=0
                                raise Exception("Material: filename "+filename+" is in a bad format")
                        self.h[i]=float(plan[0])
                        self.k[i]=float(plan[1])
                        self.l[i]=float(plan[2])
                        self.E[i]=float(plan[3])
                        self.nu[i]=float(plan[4])

                self.q=np.zeros(self.NPLANES,dtype=float)

                cosa=np.cos(self.alpha)
                cos2a=cosa*cosa
                cosb=np.cos(self.beta)
                cos2b=cosb*cosb
                cosg=np.cos(self.gamma)
                cos2g=cosg*cosg
                sina=np.cos(self.alpha)
                sin2a=sina*sina
                sinb=np.cos(self.beta)
                sin2b=sinb*sinb
                sing=np.cos(self.gamma)
                sin2g=sing*sing
                a2=self.a*self.a
                b2=self.b*self.b
                c2=self.c*self.c
                ab=self.a*self.b
                bc=self.b*self.c
                ca=self.c*self.a
                h2=self.h*self.h
                k2=self.k*self.k
                l2=self.l*self.l
                hk=self.h*self.k
                hl=self.h*self.l
                kl=self.k*self.l
                lh=self.l*self.h
                
                if self.System=="CUBIC":
                        self.q=(h2+k2+l2)/a2
                elif self.System=="HEXAG":
                        self.q=4.0*(h2+hk+k2)/(3.0*a2)+l2/c2
                elif self.System=="TRIGO":
                        self.q=(h2+k2+l2)*sin2a-2.0*(hk+kl+hl)*cosa*(1-cosa)
                        self.q/=a2*(1.0-3.0+cos2a+2.0*cos2a*cosa)
                elif self.System=="TETRA":
                        self.q=(h2+k2)/a2+l2/c2
                elif self.System=="ORTHO":
                        self.q=h2/a2+k2/b2+l2/c2
                elif self.System=="MONOC":
                        self.q=h2/(a2*sin2b)+k2/b2+l2/(c2*sin2b)+2*hl*cosb/(ac*sin2b)
                elif self.System=="TRICL":
                        self.q=h2*sin2a/a2+k2*sin2b/b2+l2*sin2g/c2
                        self.q+=2.0*hk*(cosa*cosb-cosg)/ab
                        self.q+=2.0*kl*(cosb*cosg-cosa)/bc
                        self.q+=2.0*lh*(cosg*cosa-cosb)/ca
                        self.q/=1.0-cos2a-cos2b-cos2g+2.0*cosa*cosb*cosg
                else:
                        raise Exception("Material: System "+self.System+" do not exists")
                self.q=2.0*np.pi*np.sqrt(self.q)


