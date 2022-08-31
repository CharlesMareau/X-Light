
from .reader import Reader,ReaderParameters

from .detector import Detector

from ..config import *

from ..core.utils import is_number_float

from ..core.profil import Profil
#from ..core.anode import Anode


import numpy as np

import os
import math

from os import SEEK_SET
import struct


from numba import jit

@jit(nopython=True) # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(p,q,data,mask,SUM,NP):
    #print(data.shape,mask.shape,p.shape,q.shape)
    #print(NP.shape,SUM.shape)
    #print(np.max(p),np.max(q))
    for i in range(data.shape[0]):   # Numba likes loops
        for j in range(data.shape[1]):
            #print(data[i][j])
            if mask[i][j]==False:
                if p[i][j]>=0 and p[i][j]<NP.shape[0] and q[i][j]>=0 and q[i][j]<NP.shape[1]:
                    #print(i,j,p[i][j],q[i][j])
                    NP[p[i][j],q[i][j]]+=1
                    SUM[p[i][j]][q[i][j]]+=float(data[i][j])
                    #if p[i][j]==0 and q[i][j]==0:
                    #    print(i,j,data[j][i])

class ReaderGFRM(Reader):
    
    FileExt="gfrm"
    FileType="GFRM BRUKER"
    
        
    def ReadHeaderLine(f,line:int):
        pos=line*80
        f.seek(pos,SEEK_SET)
        key=f.read(8).decode()
        pos+=8
        val=f.read(72).decode()
        return key,val
    
        
    def Read(filename:str,parameters=None):
        #print(filename)
        if parameters is None:
            parameters=ReaderParameters()
        try:
            with open(filename, "rb") as f:
                #print("hello")
                key,val=ReaderGFRM.ReadHeaderLine(f,0) #FORMAT
                format=int(val)
                if (format !=86) and (format!=100) :
                    raise Exception("ReaderGFRM : BAD FORMAT")
                key,val=ReaderGFRM.ReadHeaderLine(f,1)
                version=int(val)
                key,val=ReaderGFRM.ReadHeaderLine(f,2)
                header_size=512*int(val)
            
                key,val=ReaderGFRM.ReadHeaderLine(f,29)
                time=float(val)
            
                key,val=ReaderGFRM.ReadHeaderLine(f,37)
                angles=val.split()
                alpha=float(angles[0])
                omega=float(angles[1])
                phi=float(angles[2])
                khi=90.0-float(angles[3])
                #print(alpha)

                key,val=ReaderGFRM.ReadHeaderLine(f,39)
                bytes_per_pixel=int(val.split()[0])
                #print(key)

                key,val=ReaderGFRM.ReadHeaderLine(f,40)
                nrows=int(val.split()[0])

                key,val=ReaderGFRM.ReadHeaderLine(f,41)
                ncols=int(val.split()[0])

                key,val=ReaderGFRM.ReadHeaderLine(f,44)
                anode=val

                key,val=ReaderGFRM.ReadHeaderLine(f,65)
                axis=int(val)

                key,val=ReaderGFRM.ReadHeaderLine(f,78)
                dettype=val.split()[0]
                #print(dettype)

                detector=Detector(dettype)
                key,val=ReaderGFRM.ReadHeaderLine(f,73)
                
                #find dectector center
                key,val=ReaderGFRM.ReadHeaderLine(f,54)
                try:
                     detector.xc=float(val.split()[2])
                     detector.yc=float(val.split()[3])
                except:
                    try:
                        detector.xc=float(val.split()[0])
                        detector.yc=float(val.split()[1])
                    except:
                        print("WARNING! COULD NOT READ DETECTOR CENTER. DEFAULT VALUE IS USED.")
                #print(detector.xc)
                #print(detector.yc)
    
                #find dectector distance
                key,val=ReaderGFRM.ReadHeaderLine(f,55)
                try:
                     detector.dist=float(val.split()[1])*10.0
                except:
                    try:
                        detector.dist=float(val.split()[0])*10.0
                    except:
                        print("WARNING! COULD NOT READ DETECTOR DISTANCE. DEFAULT VALUE IS USED.")                            
                #print(detector.dist)
                        
                #find detector resolution                
                if detector.nx!=ncols:
                    detector.nx=ncols
                    print("WARNING! THE NUMBER OF COLUMNS IS NOT CONSISTENT WITH THAT OF DETECTOR INPUT FILE.")
                #print(detector.nx)
                if detector.ny!=nrows:
                    detector.ny=nrows
                    print("WARNING! THE NUMBER OF COLUMNS IS NOT CONSISTENT WITH THAT OF DETECTOR INPUT FILE.")              
                #print(detector.ny)
                #find mask parameters
                if val.strip()=="$NULL":
                    key,val1=ReaderGFRM.ReadHeaderLine(f,74)
                    key,val2=ReaderGFRM.ReadHeaderLine(f,75)
                    val=(val1+val2).split()
                    #print(val[0])
                    #print(val2)
                    detector.MinX  =int(val[0])
                    detector.MinXPY=int(val[1])
                    detector.MinY  =int(val[2])
                    detector.MaxXMY=int(val[3])
                    detector.MaxX  =int(val[4])
                    detector.MaxXPY=int(val[5])
                    detector.MaxY  =int(val[6])
                    detector.MaxYMX=int(val[7])

                #for i in range(92):
                #    key,val=ReaderGFRM.ReadHeaderLine(f,i)
                #    print(key)
                #    print(val)
            
                f.seek(header_size,SEEK_SET)

                #print(bytes_per_pixel)
                #print(nrows)
                #print(ncols)
                #ncols=1

                #print(np.dtype(np.uint16))
                if bytes_per_pixel==1:
                    data=np.fromstring(f.read(nrows*ncols),"<B")
                elif bytes_per_pixel==2:
                    data=np.fromstring(f.read(nrows*ncols*2),"<H")
                elif bytes_per_pixel==4:
                    data=np.fromstring(f.read(nrows*ncols*4),"<I")

            #print(data.dtype)
            #data=np.array(data,dtype="H")

            ###########ATTENTION, LE X (i) est les 2eme indice ###############
                    
            data=data.reshape([nrows,ncols])

            #import matplotlib.pyplot as plt
            #import numpy as np
            #plt.matshow(data)
            #plt.show()
            #data=data.reshape([ncols,nrows])
            #print(data.shape)
            #print(nrows,ncols)
            
            #print(data)

            #print("A1")
            
            mask=np.array(data,dtype=bool)
            twotheta=np.array(data,dtype=float)
            gamma=np.array(data,dtype=float)
            #print('aa')
            
            #detector=Detector(dettype)
            nx=detector.nx
            ny=detector.ny
            dx=detector.dx
            dy=detector.dy
            xc=detector.xc
            yc=detector.yc
            dist=detector.dist
            #nx=195
            #print(nx,ny)
            #print(data.shape)
            #print(nrows,ncols)
            
                        
                        
            alpha=alpha*math.pi/180.0
            
            
            xx=np.linspace(-xc*dx,float(nx-1-xc)*dx,nx)
            #print("hello")
            #xx=np.linspace(0,float(nx)*dx,nx)
            #xx=xx-xc
            yy=np.linspace(-yc*dx,float(ny-1-yc)*dy,ny)
            #yy=np.linspace(0,float(ny)*dy,ny)
            #yy=yy-yc
            xxv, yyv = np.meshgrid(xx, yy)

            #print(xxv.shape)
            #print(yyv.shape)
            #print(data.shape)
            #return
            
            #azert=math.acos(xxv*math.sin(alpha+dist*math.cos(alpha)/np.sqrt(dist*dist+xxv*xxv+yyv*yyv)))
        

            ii=np.linspace(1,nx,nx)
            jj=np.linspace(1,ny,ny)
        
            iiv, jjv = np.meshgrid(ii, jj)

            #print(iiv.shape)
            #print(jjv.shape)
            #print(data.shape)
            #return


            #print('A2')
            #return
            #iiv, jjv = np.meshgrid(ii, jj)

            #mask=np.array((iiv>=MinX) or (,dtype=bool)

            #mask=np.logical_or(iiv<=MinX, iiv>=MaxX)
            #mask=np.logical_or(mask,jjv<=MinY)
            #mask=np.logical_or(mask,jjv>=MaxY)
            #mask=np.logical_or(mask,iiv+jjv<=MinXPY)
            #mask=np.logical_or(mask,iiv+jjv>=MaxXPY)
            #mask=np.logical_or(mask,iiv-jjv>=MaxXMY)
            #mask=np.logical_or(mask,jjv-iiv>=MaxYMX)

            #print(settype)
            #print(np.max(jjv))
            #mask=detector.getMask(iiv,jjv)
            #mask=np.transpose(mask)
            #print('toto')
            #print(nrows,ncols)
            mask=detector.getMask(nrows,ncols)
            #print(mask)
            #mask=detector.getMask(jjv,iiv)

            #import matplotlib.pyplot as plt
            #aaa=np.ma.masked_array(data,mask)
            #plt.matshow(aaa)
            #plt.show()
            #print(mask.shape)
            #print(data.shape)



            #abc2=np.ma.masked_array(data,mask)
            #import matplotlib.pyplot as plt
            #plt.imshow(mask)
            #plt.show()







            
            #print(mask)
        
            twotheta=np.arccos((xxv*math.sin(alpha)+dist*math.cos(alpha))/
                               np.sqrt(dist*dist+xxv*xxv+yyv*yyv))*180.0/np.pi

            gamma=270.0-np.sign(xxv*np.cos(alpha)-dist*np.sin(alpha))*\
                np.arccos(-yyv/np.sqrt(yyv*yyv+(xxv*np.cos(alpha)-dist*np.sin(alpha))**2))*180.0/np.pi -360.0


            twotheta2=np.ma.masked_array(twotheta,mask)
            #print(twotheta2.shape)
            #print(data.shape)
            #return
            #twotheta2=twotheta
            max_twotheta=np.max(twotheta2)
            min_twotheta=np.min(twotheta2)

            #max_twotheta=np.min(twotheta2[:,0])
            #min_twotheta=np.max(twotheta2[:,nx-1])
            
            #print("MAX 2THETA")
            #print(max_twotheta)
            #print("MIN 2THETA")
            #print(min_twotheta)

            #print(
            #print(np.transpose(twotheta2[0]).shape)
            #print(nx,twotheta2.shape)
            #print(data[ny-1][nx-1])
            #return

            gamma2=np.ma.masked_array(gamma,mask)

            #print(mask)
            #gamma2=gamma
            #max_gamma=np.max(gamma2)
            #min_gamma=np.min(gamma2)

            max_gamma=np.max(gamma2[:,nx-1])
            min_gamma=np.min(gamma2[:,nx-1])
            #print(np.max(gamma2),max_gamma)
            #print(np.min(gamma2),min_gamma)


            DeltaGamma=parameters.DeltaGamma#10.0
            DeltaTwoTheta=parameters.DeltaTwoTheta#0.05
            ng=int((max_gamma-min_gamma)/DeltaGamma)+1
            ng=max(ng,2)
            dg=(max_gamma-min_gamma)/(float(ng-1))
            n2t=int((max_twotheta-min_twotheta)/DeltaTwoTheta)+1
            d2t=(max_twotheta-min_twotheta)/(float(n2t))

            Intensity=np.zeros(ng*n2t,dtype=float).reshape([ng,n2t])
            NP=np.zeros(ng*n2t,dtype=int).reshape([ng,n2t])

            #print("ng=",ng)

            fac=0.9999999999 # else idx==n2t/ng where n2t/gamma==max
            idxq=np.array((n2t*fac)*(twotheta-min_twotheta)/(max_twotheta-min_twotheta),dtype=int)
            idxp=np.array((ng*fac)*(gamma-min_gamma)/(max_gamma-min_gamma),dtype=int)

            #print(np.min(idxq),np.max(idxq))
            #print(NP.shape)
            #return

            #print('a1')
            data=np.array(data,int)
            #print(data.dtype)
            #print(data.shape)
            
            #print(nx)
            #print(ny)
            go_fast(idxp,idxq,data,mask,Intensity,NP)
            #print('a2')
            #for i in range(nx):
            #    for j in range(ny):
            #        if mask[i][j]==False:
            #            #print(data[j][i])
            #            NP[idxp[i][j]][idxq[i][j]]+=1
            #            Intensity[idxp[i][j]][idxq[i][j]]+=data[j][i]
            #            if idxp[i][j]==0 and idxq[i][j]==0:
            #                print(data[j][i])
            #                print(Intensity[idxp[i][j]][idxq[i][j]])

            #return
            profils=[]
            for p in range(ng):
                #print(p)
                Mp=0
                Si=0.0
                for q in range(n2t):
                    if NP[p][q]>0:
                        Mp+=1
                        Si+=Intensity[p][q]
                if Mp>0 and Si>0.0:
                    #print("ADD")
                    #add=False
                    profil=Profil()
                    profil.Anode.name=anode.strip()
                    profil.Phi=phi
                    profil.Khi=khi
                    profil.Time=time
                    profil.Gamma=p*dg+min_gamma+0.5*dg
                    for q in range(n2t):
                        if NP[p][q]>0:
                            twothe=q*d2t+min_twotheta+0.5*d2t
                            #print(Intensity[p][q],NP[p][q])
                            intens=float(Intensity[p][q])/float(NP[p][q])
                            #if q==0 and p==0:
                            #    print(p,q,intens,float(NP[p][q]))
                            #print(p,q,intens,float(NP[p][q]))
                            dintens=np.sqrt(max(1.0e-6,intens))/float(NP[p][q])
                            #if (intens>0.0):
                            profil.AddData(intens,twothe,omega,dintens)
                            #print(intens,twothe,omega,dintens)
                            #profil.AddData(intens,twothe,omega,dintens)
                    #print(profil)
                    profils.append(profil)
            #print('END')
            #return
            #print(profils)
            return profils
        except BaseException as e:
            return e
    

                    
                












