
from .profil import Profil
from .read import ReadFile
from .correction import Correction
from .material import Material
from .function import Function

from ..readers import ReaderParameters

import numpy as np


class Model():
    def __init__(self):
        self.profils = []
        self.correction=Correction()
        self.material=Material()
        self.function=Function()
        self.reader_parameters=ReaderParameters()
        self.files = []
    def clear(self):
        self.profils = []
        self.correction=Correction()
        self.material=Material()
        self.function=Function()
        self.reader_parameters=ReaderParameters()
        self.files = []
    def ImportFile(self,filename:str):
        try:
            profils=ReadFile(str(filename),self.reader_parameters)
            self.files.append(str(filename))
        except BaseException as e:
            raise e
        if profils:
            for profil in profils:
                self.profils.append(profil)
    def Localize(self,progress=None):

        if not progress is None:
            progress.setValue(0)

        if self.material.q is None:
            raise Exception("Material is not imported")

        n=0
        for profil in self.profils:
            try:
                profil.Localize(self.correction,self.material,self.function)
            except BaseException as e:
                raise e
            n+=1
            if not progress is None:
                progress.setValue(n*100.0/len(self.profils))

    def GetLocalizeData(self):
        data=[]
        for profil in self.profils:
            if profil.IsEnable:
                ddd=profil.GetLocalizeData()
                for d in ddd:
                    data.append(d)
        return data

    def Compute_n(self,d):
        #print(d)
        m=[np.cos(d['Theta'])*np.sin(d['Gamma']),\
           -np.sin(d['Theta']),\
           np.cos(d['Theta'])*np.cos(d['Gamma'])]
        R1=np.matrix([[np.cos(d['Omega']),0.0,-np.sin(d['Omega'])],\
                      [0.0,1.0,0.0],\
                      [np.sin(d['Omega']),0.0,np.cos(d['Omega'])]])
        R2=np.matrix([[1.0,0.0,0.0],\
                      [0.0,np.cos(d['Khi']),-np.sin(d['Khi'])],\
                      [0.0,np.sin(d['Khi']),np.cos(d['Khi'])]])
        R3=np.matrix([[np.cos(d['Phi']-np.pi/2.0),np.sin(d['Phi']-np.pi/2.0),0.0],\
                      [-np.sin(d['Phi']-np.pi/2.0),np.cos(d['Phi']-np.pi/2.0),0.0],\
                      [0.0,0.0,1.0]])
        ckhi=np.cos(d['Khi'])
        skhi=np.sin(d['Khi'])
        cphi=np.cos(d['Phi'])
        sphi=np.sin(d['Phi'])
        come=np.cos(d['Omega'])
        some=np.sin(d['Omega'])
        R=np.matrix([[ckhi*cphi,come*sphi+some*skhi*cphi,some*sphi-come*skhi*cphi],\
                     [-ckhi*sphi,come*cphi-some*skhi*sphi,some*cphi+come*skhi*sphi],\
                     [skhi,-some*ckhi,come*ckhi]])
        return np.tensordot(R,m,axes=1)

    def Compute(self,NSIGMA=1,ISIGMA=1):
        data=self.GetLocalizeData()
        n=[]
        plans=[]
        MM=len(data)
        nu=[]
        young=[]
        for d in data:
            #m=[np.cos(d['Theta'])*np.sin(d['Gamma']),\
            #   -np.sin(d['Theta']),\
            #    np.cos(d['Theta'])*np.cos(d['Gamma'])]
            #R1=np.matrix([[np.cos(d['Omega']),0.0,-np.sin(d['Omega'])],\
            #              [0.0,1.0,0.0],\
            #              [np.sin(d['Omega']),0.0,np.cos(d['Omega'])]])
            #R2=np.matrix([[1.0,0.0,0.0],\
            #              [0.0,np.cos(d['Khi']),-np.sin(d['Khi'])],\
            #              [0.0,np.sin(d['Khi']),np.cos(d['Khi'])]])
            #R3=np.matrix([[np.cos(d['Phi']-np.pi/2.0),np.sin(d['Phi']-np.pi/2.0),0.0],\
            #              [-np.sin(d['Phi']-np.pi/2.0),np.cos(d['Phi']-np.pi/2.0),0.0],\
            #              [0.0,0.0,1.0]])
            #ckhi=np.cos(d['Khi'])
            #skhi=np.sin(d['Khi'])
            #cphi=np.cos(d['Phi'])
            #sphi=np.sin(d['Phi'])
            #come=np.cos(d['Omega'])
            #some=np.sin(d['Omega'])
            #R=np.matrix([[ckhi*cphi,come*sphi+some*skhi*cphi,some*sphi-come*skhi*cphi],\
            #             [-ckhi*sphi,come*cphi-some*skhi*sphi,some*cphi+come*skhi*sphi],\
            #             [skhi,-some*ckhi,come*ckhi]])
            #n.append(np.tensordot(R,m,axes=1))
            n.append(self.Compute_n(d))
            if not d['plan'] in plans:
                plans.append(d['plan'])
            
            nu.append(self.material.nu[d['plan']])
            young.append(self.material.E[d['plan']]/1000.0)
        if NSIGMA<6:
            FREE_SURFACE=True
            NPLANS=len(plans)
        else:
            FREE_SURFACE=False
            NPLANS=0
        NN=NSIGMA+NPLANS
        if NN>MM:
            raise Exception("Number of unknows ("+str(NN)+") > number of data ("+str(MM)+")")

        idx_sigma=np.zeros((NSIGMA,2),dtype=np.uint8)
        if ISIGMA==1: #uniaxial along s1
            idx_sigma[0][0]=0
            idx_sigma[0][1]=0
        if ISIGMA==2: #uniaxial along s2
            idx_sigma[0][0]=1
            idx_sigma[0][1]=1         
        if ISIGMA==3:  #biaxial along s1 and s2
            idx_sigma[0][0]=0
            idx_sigma[0][1]=0
            idx_sigma[1][0]=1
            idx_sigma[1][1]=1
            idx_sigma[2][0]=0
            idx_sigma[2][1]=1            
        if ISIGMA==5: #triaxial along s1, s2 and s3
            idx_sigma[0][0]=0
            idx_sigma[0][1]=0
            idx_sigma[1][0]=1
            idx_sigma[1][1]=1
            idx_sigma[2][0]=1
            idx_sigma[2][1]=2
            idx_sigma[3][0]=0
            idx_sigma[3][1]=2
            idx_sigma[4][0]=0
            idx_sigma[4][1]=1            
        if ISIGMA==6:  #triaxial along s1, s2 and s3
            idx_sigma[0][0]=0
            idx_sigma[0][1]=0
            idx_sigma[1][0]=1
            idx_sigma[1][1]=1
            idx_sigma[2][0]=2
            idx_sigma[2][1]=2
            idx_sigma[3][0]=1
            idx_sigma[3][1]=2
            idx_sigma[4][0]=0
            idx_sigma[4][1]=2
            idx_sigma[5][0]=0
            idx_sigma[5][1]=1    

        kron=lambda i,j: 1.0 if i == j else 0.0

        #print(kron(0,1))


        #print(n[0])
        F=np.zeros((NSIGMA,MM))
        for ij in range(NSIGMA):
            i=idx_sigma[ij][0]
            j=idx_sigma[ij][1]
            for hkl in range(MM):
                F[ij][hkl]=n[hkl][i]*n[hkl][j]*(1.0+nu[hkl])/young[hkl]-\
                    kron(i,j)*nu[hkl]/young[hkl]
                #print(str(F[ij][hkl])+" ")
            #print("\n")

        B=np.zeros(MM)
        A=np.zeros((MM,NN))
        for hkl in range(MM):
            if FREE_SURFACE:
                B[hkl]=data[hkl]['q_hkl']
            else:
                B[hkl]=data[hkl]['q_hkl']-data[hkl]['q0']

            k=0
            for j in range(NPLANS):
                if plans[j]==data[hkl]['plan']:
                    A[hkl][k]=1.0
                else:
                    A[hkl][k]=0.0
                k+=1
            for j in range(NSIGMA):
                A[hkl][k]=-data[hkl]['q_hkl']*F[j][hkl]
                k+=1

        rcond=1.0e-6
        X=np.matmul(np.linalg.pinv(A,rcond=rcond),B)

        D=np.zeros((NN,NN))
        for i in range(NN):
            for j in range(NN):
                for k in range(MM):
                    D[i][j]+=A[k][i]*A[k][j]/(data[k]['dq_hkl']**2)
        dX=np.sqrt(np.diagonal(np.linalg.pinv(D,rcond=rcond)))

        Stress=np.zeros((3,3))
        dStress=np.zeros((3,3))
        for ij in range(NSIGMA):
            i=idx_sigma[ij][0]
            j=idx_sigma[ij][1]
            Stress[i][j]=X[NPLANS+ij]
            dStress[i][j]=dX[NPLANS+ij]
            if i!=j:
                Stress[j][i]=Stress[i][j]
                dStress[j][i]=dStress[i][j]
        print("Stress",Stress[0][0]*1000.0,Stress[1][1]*1000.0,Stress[2][2]*1000.0,Stress[0][1]*1000.0,Stress[1][2]*1000.0,Stress[2][1]*1000.0)
        print("dStress",dStress[0][0]*1000.0,dStress[1][1]*1000.0,dStress[2][2]*1000.0,dStress[0][1]*1000.0,dStress[1][2]*1000.0,dStress[2][1]*1000.0)
        return Stress*1000.0,dStress*1000.0

                
        
    
