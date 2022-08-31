
import numpy as np


class Correction():
        def __init__(self):
                self.Lorentz=False
                self.Polarisation=False
                self.ThetaM=0.0
                self.Absorption=False
        def __str__(self):
                return "Lorentz"+str(self.Lorentz)+" Polarisation"+str(self.Polarisation)+str(self.ThetaM)+" Absorption"+str(self.Absorption)

        def GetFactor(self,twotheta,gamma,omega,khi):
                C=1.0
                tt=(twotheta/2.0)*(np.pi/180.0)
                tt2=(twotheta)*(np.pi/180.0)
                tm2=(2.0*self.ThetaM)*(np.pi/180.0)
                gg=gamma*np.pi/180.0
                oo=omega*np.pi/180.0
                kk=khi*np.pi/180.0
                if self.Lorentz:
                        C=C*(np.sin(tt)**2)
                if self.Polarisation:
                        numerator=1.0+np.cos(tm2)**2
                        denom1=1.0+(np.cos(tt)**2)*(np.cos(tm2)**2)*(np.cos(gg)**2)
                        denom2=(np.cos(tm2)**2+np.cos(tt2)**2)*(np.sin(gg)**2)
                        C=C*numerator/(denom1+denom2)
                if self.Absorption:
                        cb=np.sin(oo)*np.cos(kk)
                        ck=np.sin(tt2)*np.sin(gg)*np.sin(kk)+\
                                np.sin(tt2)*np.cos(gg)*np.cos(oo)*np.cos(kk)-\
                                np.cos(tt2)*np.sin(oo)*np.cos(kk)
                        C*=(cb+ck)/cb
                        
                return C
                

