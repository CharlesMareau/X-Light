#import matplotlib.pyplot as plt


from scipy.optimize import minimize,minimize_scalar,curve_fit
import numpy as np


class Function():
        def __init__(self):
                self.OptiMethod="Powell"
                #self.OptiMethod="nelder-mead"
                #self.OptiMethod="CG"
                #self.OptiMethod="BFGS"
                #self.OptiMethod="TNC"
                
                self.Symmetry=True
                self.Name="Gauss"
                self.Noise=0
                self.Pics=[]
                self.IDX=[]
                #self.Pics=[0.95]
                self.Params=[0.0]
                self.Omega=[]

                self.Tol_Noise=0.25
                self.Tol_Pic=0.01

                self.Params=None

                self.IsInit=False

                self.Variance=None

                self.r_squared=1.0 #error R2
                

        def NParamPic(self):
                n=0
                if self.Name=="Gauss":
                        n=3
                elif self.Name=="Lorentz":
                        n=3
                elif self.Name=="PseudoVoigt":
                        n=4
                elif self.Name=="PearsonVII":
                        n=4
                else:
                        raise Exception("Function name: "+self.Name+" is not implemented")
                if not self.Symmetry:
                        n+=1
                return n


        def GetNoise(self,q,params=None):
                #out=np.ones(len(q))*params[0]
                out=0.0
                for o in range(self.Noise+1):
                        if not params is None:
                                #print(o,params,q)
                                out+=(q**o)*params[o]
                        else:
                                out+=(q**o)*self.Params[o]
                return out

        def GetPicXY(self,q,params):
                x=[]
                y=[]
                l=self.Anode.lambda2/self.Anode.lambda1
                #print(params[1],l*params[1])
                #print(params[2],params[3])
                if self.Symmetry:
                        x=(q-params[1])/params[2]
                        y=(q-params[1]*l)/params[2]
                else:
                        w1=np.where(q<params[1])
                        w2=np.where(q>=params[1])
                        x=np.zeros(len(q))
                        x[w1]=(q[w1]-params[1])/params[2]
                        x[w2]=(q[w2]-params[1])/params[3]
                        y=np.zeros(len(q))
                        #print(x)
                        #for i in range(len(q)):
                        #        if q[i]<params[1]:
                        #                x[i]=(q[i]-params[1])/params[2]
                        #                y[i]=(q[i]-params[1]*l)/params[2]
                        #        else:
                        #                x[i]=(q[i]-params[1])/params[3]
                        #                y[i]=(q[i]-params[1]*l)/params[3]
                        #print(x)
                        w1=np.where(q<params[1]*l)
                        w2=np.where(q>=params[1]*l)
                        y[w1]=(q[w1]-params[1]*l)/params[2]
                        y[w2]=(q[w2]-params[1]*l)/params[3]
                return x,y
        
        def GetPicGauss(self,q,params):
                x,y=self.GetPicXY(q,params)
                return params[0]*np.exp(-np.log(2.0)*x*x)+self.Anode.R*params[0]*np.exp(-np.log(2.0)*y*y)
                #print(x)
                #f1=params[0]*np.exp(-np.log(2.0)*x*x)
                #f2=params[0]*np.exp(-np.log(2.0)*y*y)
                #return f1+f2
        def GetPicLorentz(self,q,params):
                x,y=self.GetPicXY(q,params)
                return params[0]/(1.0+x*x)+self.Anode.R*params[0]/(1.0+y*y)
        def GetPicPseudoVoigt(self,q,params):
                l=self.GetPicLorentz(q,params)
                g=self.GetPicGauss(q,params)
                if self.Symmetry:
                        p=params[3]
                else:
                        p=params[4]
                #f p<0.0 or p>1.0:
                #       print(p)
                p=max(0.0,p)
                p=min(1.0,p)
                return p*l+(1.0-p)*g
        def GetPearsonVII(self,q,params):
                x,y=self.GetPicXY(q,params)
                if self.Symmetry:
                        p=params[3]
                else:
                        p=params[4]
                #print((2.0**(1.0/p))**p)
                p=max(1.0,p)
                #if p<1.0:
                #        print(p)
                f1=params[0]/((1.0+(x**2)*(2.0**(1.0/p)-1.0))**(p))
                f2=self.Anode.R*params[0]/((1.0+(y**2)*(2.0**(1.0/p)-1.0))**(p))
                return f1+f2
                

        def GetPic(self,q,params):
                if self.Name=="Gauss":
                        return self.GetPicGauss(q,params)
                elif self.Name=="Lorentz":
                        return self.GetPicLorentz(q,params)
                elif self.Name=="PseudoVoigt":
                        return self.GetPicPseudoVoigt(q,params)
                elif self.Name=="PearsonVII":
                        return self.GetPearsonVII(q,params)
                else:
                        raise Exception("Function name: "+self.Name+" is not implemented")

                        
        def GetFunction(self,q,params=None):
                pp=[]
                if params is None:
                        params=self.Params
                pp=params
                #pp[0]=1.0
                #print(str(pp))
                f=self.GetNoise(q,pp)
                for nb in range(len(self.Pics)):
                        n1=self.Noise+1+nb*self.NParamPic()
                        n2=n1+self.NParamPic()
                        pp=params[n1:n2]
                        f+=self.GetPic(q,pp)
                #print(str(f))
                #import matplotlib.pyplot as plt
                #plt.plot(q, f)
                #plt.show()
                #print("rr")
                return f

        def Init(self,material,anode,q,i,delta_i=None):
                #i=i+100.0
                                
                self.Anode=anode

                self.Pics=[]
                self.IDX=[]
                qmin=np.min(q)
                qmax=np.max(q)
                idx=0
                for q0 in material.q:
                        q1=(1.0-self.Tol_Pic)*q0
                        q2=(1.0+self.Tol_Pic)*q0
                        #if (q1>qmin) and (q2<qmax):
                        if (q0>qmin) and (q0<qmax):
                                self.Pics.append(q0)
                                self.IDX.append(idx)
                        idx+=1
                                
                self.Params=np.zeros(self.Noise+1+self.NParamPic()*len(self.Pics))
                self.Params[0:self.Noise+1]=self.InitNoise(q,i)
                #print(str(self.Params[0]))
                #print(str(self.Params[1]))
                nb=0

                
                #bound=[-float('inf')*np.ones(len(self.Params)),float('inf')*np.ones(len(self.Params))]
                bound=[[],[]]
                for p in range(len(self.Params)):
                        #bound.append([-float('inf'),float('inf')])
                        if p>self.Noise:
                                bound[0].append(1.0e-8)
                        else:
                                bound[0].append(-np.inf)
                        bound[1].append( np.inf)
                
                for pic in self.Pics:
                        #print(pic)
                        #print(np.min(q),np.max(q))
                        n1=self.Noise+1+nb*self.NParamPic()
                        n2=n1+self.NParamPic()
                        if self.Name=="PseudoVoigt":
                                if self.Symmetry:
                                        bound[0][n1+3]=0.0
                                        bound[1][n1+3]=1.0
                                else:
                                        bound[0][n1+4]=0.0
                                        bound[1][n1+4]=1.0
                        elif self.Name=="PearsonVII":
                                if self.Symmetry:
                                        bound[0][n1+3]=1.0
                                else:
                                        bound[0][n1+4]=1.0
                        self.Params[n1:n2]=self.InitPic(pic,q,i)
                        nb+=1
                
                x0=self.Params

                bound[0]=tuple(bound[0])
                bound[1]=tuple(bound[1])
                bound=tuple(bound)
                #bound=None

                #self.IsInit=True
                #return

                #print(i[0],delta_i[0],np.sqrt(i[0]))

                fun= lambda x,*p: self.GetFunction(x,p)
                #delta_i+=1.0e-8
                #print(str(delta_i))
                self.Params,covariance=curve_fit(fun,q,i,p0=x0,sigma=delta_i,bounds=bound)
                
                #self.Params,covariance=curve_fit(fun,q,i,p0=x0,bounds=bound)
                

                residual=i-self.GetFunction(q,self.Params)
                ss_res=np.sum(residual**2)
                ss_tot=np.sum((i-np.mean(i))**2)
                self.r_squared=1.0-(ss_res/ss_tot)
                #print(self.r_squared)
                self.Variance=np.diag(covariance)

                self.IsInit=True

        def GetShape(self,ipic):
                p0=self.Noise+1+ipic*self.NParamPic()
                i=self.Params[p0]
                delta_i=np.sqrt(self.Variance[p0])
                #print(i,delta_i )
                q=self.Params[p0+1]
                delta_q=np.sqrt(self.Variance[p0+1])
                if self.Symmetry:
                        w=2.0*self.Params[p0+2]
                        delta_w=2.0*np.sqrt(self.Variance[p0+2])
                else:
                        w=self.Params[p0+2]+self.Params[p0+3]
                        delta_w=np.sqrt(self.Variance[p0+2])+np.sqrt(self.Variance[p0+3])
                res=dict()
                res['i_hkl']=i
                res['di_hkl']=delta_i
                res['q_hkl']=q
                res['dq_hkl']=delta_q
                res['w_hkl']=w
                res['dw_hkl']=delta_w

                return res
        def InitNoise(self,q,i):
                cond=np.where(np.abs(i)>0.00000001)
                qq=q
                ii=i
                is_end=False
                x0=np.zeros(self.Noise+1)
                iter=0
                aaa=i-i
                cond2=np.where(aaa<self.Tol_Noise)
                while not is_end:
                        cond2p=cond2
                        iter+=1
                        #fun= lambda x: self.FNoise(qq,ii,x)
                        #res = minimize(fun, x0, method=self.OptiMethod)
                        fun= lambda x,*p: self.GetNoise(x,p)
                        x0,cov=curve_fit(fun,qq,ii,p0=x0)
                        #i2=self.GetNoise(q,res.x)
                        i2=self.GetNoise(q,x0)
                        aaa=(i-i2)#/i
                        aaa[cond]/=i[cond]
                        cond2=np.where(aaa<=self.Tol_Noise)
                        ii=i[cond2]
                        qq=q[cond2]
                        if np.array_equal(cond2,cond2p) :
                                is_end=True
                        #x0=res.x
                #x0[0]=max(x0[0],1.0e-5)
                return x0
        def InitPic(self,q0,q,i):
                wh=np.where((q>(1.0-self.Tol_Pic)*q0) & (q<(1.0+self.Tol_Pic)*q0))
                
                #if (wh.size==0):
                #        print("toto")
                #        raise Exception("No data to initialyse the pic with q="+str(q0))
                #else:
                #        print("tutu")
                #print(len(wh))
                #print(wh)
                #print(wh)
                q=q[(wh)]
                if q.size==0:
                        raise Exception("No data to initialyse the pic with q="+str(q0))

                #print(q)
                i=i[(wh)]
                f=i-self.GetNoise(q)

                A1=np.trapz(f,x=q)
                A2=np.trapz(f*q,x=q)
                #print(A1,A2)
                param=np.zeros(self.NParamPic())
                param[0]=np.max(f)
                param[1]=A2/A1
                param[2]=0.5*A1/param[0]
                #print(param)
                if not self.Symmetry:
                        param[3]=param[2]
                if self.Name=="PseudoVoigt":
                        if self.Symmetry:
                                param[3]=0.5
                        else:
                                param[4]=0.5
                if self.Name=="PearsonVII":
                        if self.Symmetry:
                                param[3]=2.0
                        else:
                                param[4]=2.0
                
                return param
                
