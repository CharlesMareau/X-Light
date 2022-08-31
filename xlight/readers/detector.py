from ..config import *

import numpy as np



class Detector():
    def __init__(self,filetype:str):
        LL=GetDetectorDict()
        with open(LL[filetype]) as f:
            f.readline()
            f.readline()
            line=f.readline().split()
            self.nx=int(line[0])
            self.ny=int(line[1])
            f.readline()
            line=f.readline().split();
            self.dx=float(line[0])
            self.dy=float(line[1])
            f.readline()
            line=f.readline().split();
            self.xc=float(line[0])
            self.yc=float(line[1])
            f.readline()
            self.dist=float(f.readline())
            f.readline()
            line=f.readline().split()
            self.MinX=int(line[0])
            self.MinXPY=int(line[1])
            self.MinY=int(line[2])
            self.MaxXMY=int(line[3])
            self.MaxX=int(line[4])
            self.MaxXPY=int(line[5])
            self.MaxY=int(line[6])
            self.MaxYMX=int(line[7])

    def getMask(self,nrows,ncols):
        #self.MinX=0
        #self.MinY=0
        #self.MinXPY=0
        #self.MaxX=100000
        #self.MaxXMY=100000
        #self.MaxXPY=100000
        #self.MaxY=100000
        #self.MaxYMX=100000
        #print(nrows,ncols)
        mask=np.zeros((nrows,ncols),dtype=bool)
        #mask=mask.reshape([nrows,ncols])
        for j in range(nrows):
            for i in range(ncols):
                if (i<=self.MinX and i>=self.MaxX and
                    j<=self.MinY and j>=self.MaxY and
                    i+j<=MinXPY and i+j>=MaxXPY and
                    i-j>=MaxXMY and j-i>=MaxYMX):
                    mask[j][i]=True
                
                        
        #        mask[i][j]=False

        #print(mask)

        #print(iiv)
        #print(jjv)
        
        #mask=np.logical_or(iiv<self.MinX, iiv>self.MaxX)
        #mask=np.logical_or(mask,jjv<self.MinY)
        #mask=np.logical_or(mask,jjv>self.MaxY)
        #mask=np.logical_or(mask,iiv+jjv<self.MinXPY)
        #mask=np.logical_or(mask,iiv+jjv>self.MaxXPY)
        #mask=np.logical_or(mask,iiv-jjv>self.MaxXMY)
        #mask=np.logical_or(mask,jjv-iiv>self.MaxYMX)
        #mask=np.logical_or(iiv<0, iiv>self.MaxX*1000)
        return mask
        #return False

        
    
    
