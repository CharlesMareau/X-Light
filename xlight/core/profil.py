import numpy as np
from ..config import *

#import model as CM
#from core.model import *
#from core.model import Function
import copy
#from core.function import Function
from .anode import Anode
from .function import Function
from .correction import Correction

#import xlight.core.model as CM

#from core import toto

from scipy.optimize import minimize

import sys



class ProfilData:
        def __init__(self, Intensity:float, TwoTheta:float, Omega:float):
                self.Intensity=Intensity
                self.TwoTheta=TwoTheta
                self.Omega=Omega
        def __setattr__(self, name, value):
                if name == 'Intensity' and not isinstance(value, float):
                        raise TypeError('profil_data().Intensity must be a float')
                if name == 'TwoTheta' and not isinstance(value, float):
                        raise TypeError('profil_data().TwoTheta must be a float')
                if name == 'Omega' and not isinstance(value, float):
                        raise TypeError('profil_data().Omega must be a float')
                super().__setattr__(name, value)
        def __str__(self):
                return "<profil_data Intensity:%s TwoTheta:%s Omega:%s>" % (self.Intensity, self.TwoTheta, self.Omega)



        

class Profil:
        def __init__(self, Khi=0.0,Phi=0.0,Gamma=0.0,Time=1.0):
                #self.data=[]
                
                
                self.Intensity=None
                self.DIntensity=None
                self.TwoTheta=None
                self.Omega=None
                self.NDATA=0
                
                self.Khi=Khi
                self.Phi=Phi
                self.Gamma=Gamma
                self.Time=Time
                self.Anode=Anode()

                self.i=None
                self.di=None
                self.q=None
                #self.lambda1=None
                #self.lambda2=None
                #self.R=None

                self.Fun=Function()
                self.Correction=Correction()

                self.IsEnable=True

        def SetEnable(self,enable):
                self.IsEnable=enable

        def GetFunctionData(self,correction=False):
                i=self.Fun.GetFunction(self.q)
                if not correction:
                        i*=self.Time/self.Correction.GetFactor(self.TwoTheta,self.Gamma,self.Omega,
                                                               self.Khi)
                        #print(self.Fun.Pics)
                return i
                
        def Localize(self,correction,material,function):
                self.Correction=copy.copy(correction)
                self.i=(self.Intensity/self.Time)*self.Correction.GetFactor(self.TwoTheta,
                                                                            self.Gamma,
                                                                            self.Omega,
                                                                            self.Khi)
                self.di=(self.DIntensity/self.Time)*self.Correction.GetFactor(self.TwoTheta,
                                                                              self.Gamma,
                                                                              self.Omega,
                                                                              self.Khi)
                
                self.q=4.0*np.pi*np.sin((self.TwoTheta/2.0)*(np.pi/180.0))/self.Anode.getLambda()
                self.Fun=copy.copy(function)
                #delta_i=None#np.sqrt(self.i)/len(self.i)
                self.Fun.Init(material,self.Anode,self.q,self.i,self.di)

        def GetLocalizeData(self):
                data=[]
                #print(self.Omega)
                for pic in range(len(self.Fun.Pics)):
                        d=self.Fun.GetShape(pic)
                        d['Omega']=np.interp(d['q_hkl'],self.q,self.Omega)*np.pi/180.0
                        d['q0']=self.Fun.Pics[pic]
                        d['plan']=self.Fun.IDX[pic]
                        d['Khi']=self.Khi*np.pi/180.0
                        d['Phi']=self.Phi*np.pi/180.0
                        d['Gamma']=self.Gamma*np.pi/180.0
                        d['Theta']=np.arcsin(d['q_hkl']*self.Anode.getLambda()/(4.0*np.pi))
                        data.append(d)
                return data
                

                

        def __setattr__(self, name, value):
                if name == 'Khi' and not isinstance(value, float):
                        raise TypeError('profil().Khi must be a float')
                if name == 'Phi' and not isinstance(value, float):
                        raise TypeError('profil().Phi must be a float')
                if name == 'Gamma' and not isinstance(value, float):
                        raise TypeError('profil().Gamma must be a float')
                if name == 'Time' and not isinstance(value, float):
                        raise TypeError('profil().Time must be a float')
                super().__setattr__(name, value)

        def __str__(self):
                return "<profil NbOfData:%s Khi:%s Phi:%s Gamma:%s Time:%s Anode:%s>" % (self.NDATA,self.Khi,self.Phi,self.Gamma,self.Time,self.Anode.name)
        def AddData(self,Intensity:float,TwoTheta:float,Omega:float,DIntensity=None):
                if Intensity<=0.0:
                        return
                if DIntensity is None:
                        DIntensity=np.sqrt(Intensity)
                if self.NDATA==0:
                        self.Intensity=np.array([Intensity])
                        self.TwoTheta=np.array([TwoTheta])
                        self.Omega=np.array([Omega])
                        self.DIntensity=np.array([DIntensity])
                else:
                        self.Intensity=np.append(self.Intensity,Intensity)
                        self.TwoTheta=np.append(self.TwoTheta,TwoTheta)
                        self.Omega=np.append(self.Omega,Omega)
                        self.DIntensity=np.append(self.DIntensity,DIntensity)
                self.NDATA+=1
                #self.data.append(ProfilData(Intensity,TwoTheta,Omega))



