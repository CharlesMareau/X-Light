
import sys

#from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QMainWindow, QLabel, QMenuBar, QMenu, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox, QGridLayout, QSpinBox, QToolButton, QLCDNumber, QFrame, QVBoxLayout, QListWidget, QListWidgetItem, QDoubleSpinBox, QGroupBox, QScrollArea, QSizeGrip, QSplitter, QTextEdit, QListView, QTableWidget,QTableWidgetItem, QSizePolicy,QTableView,QHeaderView
#from PySide6.QtGui import QCloseEvent, QAction, QKeySequence

#from PySide6.QtCore import Qt,QSize


#from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen



#from PySide6.QtCore import QPointF,QAbstractTableModel
#from PySide6.QtGui import QPainter
#from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar
#from PySide6.QtCharts import QChart, QChartView, QLineSeries,QScatterSeries,QValueAxis

#from PySide6.QtCore import Slot

#from PySide6.QtCore import Qt

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.patches as patches



#import gui.toto as toto
#import gui.tab as tab


from ..core import *



from pathlib import Path
from ..  import config




class PowerBar(QWidget):
    def __init__(self,parent=None):
        super(PowerBar, self).__init__(parent)


        layout = QHBoxLayout()


        #self.enable = QCheckBox("Enable")
        #layout.addWidget(self.enable)

        

        self.firstButton = QToolButton()
        icon = QIcon.fromTheme("go-first-symbolic.svg")
        self.firstButton.setIcon(icon)
        layout.addWidget(self.firstButton)


        self.previousButton = QToolButton()
        icon = QIcon.fromTheme("go-previous-symbolic.svg")
        self.previousButton.setIcon(icon)
        layout.addWidget(self.previousButton)


        self.lcd = QLCDNumber()
        #self.lcd.resize(40, 40)
        layout.addWidget(self.lcd)



        self.nextButton = QToolButton()
        icon = QIcon.fromTheme("go-next-symbolic.svg")
        self.nextButton.setIcon(icon)
        layout.addWidget(self.nextButton)


        self.lastButton = QToolButton()
        icon = QIcon.fromTheme("go-last-symbolic.svg")
        self.lastButton.setIcon(icon)
        layout.addWidget(self.lastButton)

        self.setLayout(layout)



def term(base, exponent):
    return u'{}<sub>{}</sub>'.format(base, exponent)



class TensorWidget(QWidget):
    def __init__(self):
        super(TensorWidget, self).__init__(parent=None)
        layout = QGridLayout()
        self.setLayout(layout)
        #self.S11=QLabel("S11")
        #self.S12=QLabel("S12")
        #self.S13=QLabel("S13")
        #self.S21=QLabel("S21")
        #self.S22=QLabel("S22")
        #self.S23=QLabel("S23")
        #self.S31=QLabel("S31")
        #self.S32=QLabel("S32")
        #self.S33=QLabel("S33")
        self.S=[[QLabel("SIJ") for x in range(3)] for y in range(3)]
        self.DS=[[QLabel("DSIJ") for x in range(3)] for y in range(3)]
        self.P=QLabel("P")
        self.MISES=QLabel("Mises")
        self.TRESCA=QLabel("Tresca")
        layout.addWidget(QLabel("\u03c3 (MPa) = "),1,0)
        layout.addWidget(QLabel(""),3,0)
        layout.addWidget(QLabel("\u03b4\u03c3 (MPa) = "),5,0)
        for i in range(3):
            for j in range(3):
                layout.addWidget(self.S[i][j],i,j+1)
                layout.addWidget(self.DS[i][j],i+4,j+1)

        layout.addWidget(QLabel(""),7,0)
        layout.addWidget(QLabel("Mises (MPa)"),8,1)
        layout.addWidget(self.MISES,9,1)
        layout.addWidget(QLabel("Tresca (MPa)"),8,2)
        layout.addWidget(self.TRESCA,9,2)
        layout.addWidget(QLabel("Pressure (MPa)"),8,3)
        layout.addWidget(self.P,9,3)



        #self.Displacement=PowerBar(self)
        layout.addWidget(QLabel(""),10,0)
        layout.addWidget(QLabel("\u03D5"),11,1)
        self.PHI=QLabel("PHI")
        layout.addWidget(self.PHI,12,1)
        self.SPHI=QLabel("SPHI")
        s=u'\u03c3<sub>\u03D5</sub> (MPa)'
        layout.addWidget(QLabel(s),11,2)
        layout.addWidget(self.SPHI,12,2)
        self.TPHI=QLabel("TPHI")
        s=u'\u03c4<sub>\u03D5</sub> (MPa)'
        layout.addWidget(QLabel(s),11,3)
        layout.addWidget(self.TPHI,12,3)

        #layout.addWidget(self.S11,0,1)
        #layout.addWidget(self.S12,0,2)
        #layout.addWidget(self.S13,0,3)
        #layout.addWidget(self.S21,1,1)
        #layout.addWidget(self.S22,1,2)
        #layout.addWidget(self.S23,1,3)
        #layout.addWidget(self.S31,2,1)
        #layout.addWidget(self.S32,2,2)
        #layout.addWidget(self.S33,2,3)
        layout.setColumnStretch(30,1)
        layout.setRowStretch(30,1)
        
        self.export = QPushButton("Export")
        self.export.clicked.connect(self.Export)
        layout.addWidget(self.export)
        
    def Export(self):
                #msgBox = QMessageBox()
                #msgBox.setIcon(QMessageBox.Critical)
                #msgBox.setText("Evaluation needs to be performed")
                #msgBox.setWindowTitle("Error")
                #msgBox.setStandardButtons(QMessageBox.Ok)
                #returnValue = msgBox.exec()
                #return
                filename=QFileDialog.getSaveFileName(None,"Evaluate data file", str(Path.home()),options=QFileDialog.DontUseNativeDialog)
                if filename[0]=="":
                        return
                f=open(filename[0],"w")
                f.write(" s11 s22 s33 s12 s23 s31 std(s11) std(s22) std(s33) std(s12) std(s23) std(s31) mises tresca pressure")
                f.write("\n")
                f.write(" "+self.S[0][0].text())
                f.write(" "+self.S[1][1].text())
                f.write(" "+self.S[2][2].text())
                f.write(" "+self.S[0][1].text())
                f.write(" "+self.S[1][2].text())
                f.write(" "+self.S[2][0].text())
                f.write(" "+self.DS[0][0].text())
                f.write(" "+self.DS[1][1].text())
                f.write(" "+self.DS[2][2].text())
                f.write(" "+self.DS[0][1].text())
                f.write(" "+self.DS[1][2].text())
                f.write(" "+self.DS[2][0].text())
                f.write(" "+self.MISES.text())
                f.write(" "+self.TRESCA.text())
                f.write(" "+self.P.text())
                f.write("\n")
                f.close()
                
    def Set(self,S,DS,W,K=None):
        mises=np.sqrt(0.5*((W[2]-W[1])**2+(W[1]-W[0])**2+(W[2]-W[0])**2))
        tresca=np.maximum(np.maximum(np.abs(W[2]-W[1]),np.abs(W[2]-W[0])),np.abs(W[1]-W[0]))
        hydro=(W[0]+W[1]+W[2])/3.0


        s="{:.2e}".format(mises)
        self.MISES.setText(s)

        s="{:.2e}".format(tresca)
        self.TRESCA.setText(s)

        s="{:+.2e}".format(hydro)
        self.P.setText(s)
        
        for i in range(3):
            for j in range(3):
                #print(i,j)
                s="{:+.2e}".format(S[i][j])
                ds="\u00B1"+"{:.2e}".format(DS[i][j])
                self.S[i][j].setText(s)
                self.DS[i][j].setText(ds)
                #self.S11="{:+.2e}".format(S[0][0])+" \u00B1 "+"{:.2e}".format(DS[0][0])


        if K:
            s="{:.2f}".format(K[0]*180.0/np.pi)
            self.PHI.setText(s+"\u00B0")
            t=np.matmul(S,K[1])            
            sn=np.matmul(t,K[1])
            st=t[2]
            #np.sqrt(np.matmul(t,t)-sn**2)
            s="{:.2e}".format(sn)
            self.SPHI.setText(s)
            s="{:.2e}".format(st)
            self.TPHI.setText(s)
        else:
            s="{:.2f}".format(0.0)
            self.PHI.setText(s+"\u00B0")
            s="{:.2e}".format(0.0)
            self.SPHI.setText(s)
            self.TPHI.setText(s)


def format_coord2(x, y):
    xlabel=u'\u03D5='
    ylabel=u"\u03A8="
    psi=2.0*np.arctan(np.sqrt(x**2+y**2))*180.0/np.pi
    phi=0.0
    if psi>1.0:
        phi=np.arccos(x/np.tan(psi*(np.pi/180.0)/2.0))*180.0/np.pi
        if y<0:
            phi=360.0-phi
        if phi>180.0:
            phi-=180.0
            psi=-psi
    xvalue="%1.2f" % (phi)
    yvalue="%1.2f" % (psi)
    xunity=u"\u00B0"
    yunity=u"\u00B0"
    return xlabel+xvalue+xunity+", "+ylabel+yvalue+yunity

def format_coord3(x, y):
    xlabel=u"sin\u00B2\u03A8="
    ylabel=u'\u03B5<sub>ijk</sub>='
    xvalue="%1.2f" % (x)
    yvalue="{:e}".format(y)
    xunity=""
    yunity=""
    return xlabel+xvalue+xunity+", "+ylabel+yvalue+yunity

class PhiWidget(QWidget):
    def __init__(self):
        super(PhiWidget,self).__init__(parent=None)
        layout = QHBoxLayout()
        #self.Button=QPushButton("Update")
        #layout.addWidget(self.Button)
        #self.PHI=QSpinBox()
        #layout.addWidget(self.PHI)

        self.PHI=QDoubleSpinBox(self)
        self.PHI.setValue(0.0)
        self.PHI.setRange(-180.0,180.0)
        self.PHI.setSingleStep(5.0)
        self.PHI.setPrefix("\u03D5 = ")
        self.PHI.setSuffix("\u00B0")
        layout.addWidget(self.PHI)
        
        self.DeltaPHI=QDoubleSpinBox(self)
        self.DeltaPHI.setValue(5.0)
        self.DeltaPHI.setRange(1.0,90.0)
        self.DeltaPHI.setSingleStep(1.0)
        self.DeltaPHI.setPrefix("\u0394\u03D5 = ")
        self.DeltaPHI.setSuffix("\u00B0")
        layout.addWidget(self.DeltaPHI)
        self.setLayout(layout)
        


class StressWidget(QWidget):
    def __init__(self,model=None):
        #super().__init__()
        super(StressWidget, self).__init__(parent=None)
        self.model=model
        layout = QGridLayout()
        
        self.setLayout(layout)

        self.NPic=0
        self.NPro=0
        self.ipro=0

        self.phi=[]
        self.psi=[]
        self.k=[]
        self.eps=[]
        self.enable=[]
        self.app=None

        self.S=None
        self.DS=None


        
        self.Tensor=TensorWidget()
        layout.addWidget(self.Tensor,0,0,2,1)
        #layout.addWidget(self.Tensor,0,0,1,1)

        self.PhiUSER=PhiWidget()


        self.PhiUSER.DeltaPHI.valueChanged.connect(self.Set)
        self.PhiUSER.PHI.valueChanged.connect(self.Set)
        #layout.addWidget(tutu,1,0,1,1)

        #self.Displacement=PowerBar(self)
        #layout.addWidget(self.Displacement,0,1,1,2)
        layout.addWidget(self.PhiUSER,0,1,1,2)

        #self.Displacement.nextButton.clicked.connect(self.Next)
        #self.Displacement.lastButton.clicked.connect(self.Last)

        #self.Displacement.previousButton.clicked.connect(self.Previous)
        #self.Displacement.firstButton.clicked.connect(self.First)


        #self.figure = plt.figure()
        #self.canvas = FigureCanvas(self.figure)
        #####layout.addWidget(self.canvas,1,1)
        layout.setColumnStretch(2,2)
        layout.setRowStretch(1,1)

        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)


        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        unwanted_buttons=['Back','Forward','Subplots','Customize']
        for x in self.toolbar2.actions():
            if x.text() in unwanted_buttons:
                self.toolbar2.removeAction(x)

        

        
        
        self.figure3 = plt.figure()
        self.canvas3 = FigureCanvas(self.figure3)


        self.toolbar3 = NavigationToolbar(self.canvas3, self)
        unwanted_buttons=['Back','Forward','Subplots','Customize']
        for x in self.toolbar3.actions():
            if x.text() in unwanted_buttons:
                self.toolbar3.removeAction(x)

        
        #layout.addWidget(self.canvas2,0,1,2,1)
        #layout.addWidget(self.toolbar2,2,1)
        #layout.addWidget(self.canvas3,0,2,2,1)
        #layout.addWidget(self.toolbar3,2,2)

        layout.addWidget(self.canvas2,1,1)
        layout.addWidget(self.toolbar2,2,1)
        layout.addWidget(self.canvas3,1,2)
        layout.addWidget(self.toolbar3,2,2)


        
        self.Set2()
        self.Set3()
        #layout.addWidget(QLabel("V11"),0,0)
        #layout.addWidget(QLabel("V12"),0,1)
        #layout.addWidget(QLabel("V13"),0,2)
        #layout.addWidget(QLabel("V21"),1,0)
        #layout.addWidget(QLabel("V22"),1,1)
        #layout.addWidget(QLabel("V23"),1,2)

    #def Next(self):
    #    self.ipro+=1
    #    self.ipro=min(self.ipro,self.NPro-1)
    #    self.ipro=max(0,self.ipro)
    #    self.Displacement.lcd.display(self.ipro+1)
    #    self.Set()
    #    #self.ReLoad()
    #def Last(self):
    #    self.ipro=self.NPro
    #    self.ipro=max(0,self.NPro-1)
    #    self.Displacement.lcd.display(self.ipro+1)
    #    self.Set()
    #    #self.ReLoad()

    #def Previous(self):
    #    self.ipro-=1
    #    self.ipro=max(0,self.ipro)
    #    self.Displacement.lcd.display(self.ipro+1)
    #    self.Set()
    #    #self.ReLoad()
    #def First(self):
    #    self.ipro=0
    #    self.Displacement.lcd.display(self.ipro+1)
    #    self.Set()
    #    #self.ReLoad()
    #def MinMaxDisplacment(self):
    #    if self.ipro<0:
    #        self.ipro=0;
    #    if self.ipro>=self.NPro:
    #        self.ipro=self.NPro-1
    #    if self.NPro==0:
    #        self.ipro=0
    #    self.Displacement.lcd.display(self.ipro+1)
    #    self.Set()



    def Update(self,S,DS):

        self.S=S
        self.DS=DS

        beta=[]

        self.phi=[]
        self.psi=[]
        #self.k=[]
        self.eps=[]
        #self.app=None
        self.enable=[]

        #self.NPro=0
        self.NPic=0
        for profil in self.model.profils:
            data=[]
            ddd=profil.GetLocalizeData()
            for d in ddd:
                self.NPic+=1
                n=self.model.Compute_n(d)
                psi=np.arccos(n[2])
                phi=np.arctan2(n[1],n[0])
                if np.sqrt(n[1]**2+n[0]**2)>1.0e-4:
                    phi=np.arctan2(n[1],n[0])
                else:
                    phi=0.0
                if phi<0:
                    phi+=np.pi
                    psi=-psi
                if phi>=np.pi:
                    phi-=np.pi
                    psi=-psi
                self.phi.append(phi)
                self.psi.append(psi)
                self.eps.append((d['q0']/d['q_hkl'])-1)
                #New=True
                #tol=10.0*np.pi/180.0
                #for j in range(self.NPro):
                #    if (np.abs(phi-beta[j])<tol):
                #        New=False
                #if (np.abs(psi)<tol):
                #    New=False
                #if New:
                #    self.NPro+=1
                #    beta.append(phi)
                #    self.k.append([phi,np.array([np.cos(phi),np.sin(phi),0.0])])
                #    
                if profil.IsEnable:
                    self.enable.append(True)
                else:
                    self.enable.append(False)

        #tol=10.0*np.pi/180.0
        #if self.NPic>0 and self.NPro>0 :
        #    self.app=np.zeros((self.NPic,self.NPro),dtype=bool)
        #    for i in range(self.NPic):
        #        for j in range(self.NPro):
        #            if (np.abs(self.phi[i]-beta[j])<tol) :#and (np.abs(self.psi[i])>tol) :
        #                self.app[i][j]=True
        #            else:
        #                self.app[i][j]=False
    

        #self.MinMaxDisplacment()
        

    def Set2(self):

        self.figure2.clear()
        ax = self.figure2.add_subplot(111)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)

        ax.format_coord = format_coord2


        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')

        theta = np.linspace( 0 , 2.0*np.pi , 360 )
        a1 = np.cos( theta )
        b1 = np.sin( theta )
        ax.plot(a1,b1, color='black')
        x1=[]
        y1=[]
        x2=[]
        y2=[]

        for i in range(self.NPic):
            if self.enable[i]:
                x1.append(np.cos(self.phi[i])*np.tan(self.psi[i]/2.0))
                y1.append(np.sin(self.phi[i])*np.tan(self.psi[i]/2.0))
            else:
                x2.append(np.cos(self.phi[i])*np.tan(self.psi[i]/2.0))
                y2.append(np.sin(self.phi[i])*np.tan(self.psi[i]/2.0))



        phi=self.PhiUSER.PHI.value()
        dphi=self.PhiUSER.DeltaPHI.value()

        phi-=90.0
        dh=dphi/45.0
        x=-0.5*dh*np.cos((phi)*np.pi/180.0)+np.sin((phi)*np.pi/180.0)
        y=-0.5*dh*np.sin((phi)*np.pi/180.0)-np.cos((phi)*np.pi/180.0)
        ax.add_patch(patches.Rectangle((x,y),dh,2.0,angle=phi,edgecolor='yellow',facecolor='yellow',fill=True))
        ax.scatter(x2,y2,color='grey')
        ax.scatter(x1,y1,color='red')



        


        #ax.plot(0,0)
        ax.set_title('Stereographic projection')

        ax.annotate('S1', xy=(1.05, 0.05))
        ax.annotate('S2', xy=(0.05, 1.05))
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
        #, xycoords=('axes fraction', 'data'), 
        #    xytext=(arrow_length, 0), textcoords='offset points',
        #    ha='left', va='center',
        #    arrowprops=dict(arrowstyle='<|-', fc='black'))
        
        ax.set_ylabel('S2', fontsize=16)
        ax.set_aspect('equal')
        
        self.canvas2.draw()


    def Set3(self):
        #print('tptp')
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        phi=-self.PhiUSER.PHI.value()*np.pi/180.0
        dy=self.PhiUSER.DeltaPHI.value()/90.0
        for i in range(self.NPic):
            x=np.cos(self.phi[i])*np.tan(self.psi[i]/2.0)
            y=np.sin(self.phi[i])*np.tan(self.psi[i]/2.0)
            xx=np.cos(phi)*x-np.sin(phi)*y
            yy=np.sin(phi)*x+np.cos(phi)*y
            if np.abs(yy)<=dy:
                if self.enable[i]:
                    x1.append(np.sin(self.psi[i])**2)
                    y1.append(self.eps[i])
                else:
                    x2.append(np.sin(self.psi[i])**2)
                    y2.append(self.eps[i])
            
            #print('hello')
            #if self.app[i][self.ipro]:
            #    if self.enable[i]:
            #        x1.append(np.sin(self.psi[i])**2)
            #        y1.append(self.eps[i])
            #    else:
            #        x2.append(np.sin(self.psi[i])**2)
            #        y2.append(self.eps[i])
                    
                
        self.figure3.clear()
        ax = self.figure3.add_subplot(111)
        ax.format_coord = format_coord3
        ax.scatter(x2,y2,color='grey')
        ax.scatter(x1,y1,color='red')
        ax.set_xlabel(r'$sin^2\psi$', fontsize=16)
        ax.set_ylabel(r'$\epsilon_{hkl}$', fontsize=16)

        ax.set_title('Lattice strains')
        self.canvas3.draw()
                
        #print(str(psi))

    #def Set3(self):
    #    tol=1.0e-4
    #    Npro=0
    #    beta=[]
    #    for profil in self.model.profils:
    #        ddd=profil.GetLocalizeData()
    #        for d in ddd:
    #            New=True
    #            for j in range(Npro):
    #                if (d['Phi']-beta[j] < tol) and (
        
        
        


    def Set1(self):
        #s ="\u03c3\u2081\u2081=({:+.2e}".format(S[0][0])+" \u00B1 "+"{:.2e}".format(DS[0][0])+")\t"
        #s+="\u03c3\u2081\u2082=({:+.2e}".format(S[0][1])+" \u00B1 "+"{:.2e}".format(DS[0][1])+")\t"
        #s+="\u03c3\u2081\u2083=({:+.2e}".format(S[0][2])+" \u00B1 "+"{:.2e}".format(DS[0][2])+")\n"
        #s+="\u03c3\u2082\u2081=({:+.2e}".format(S[1][0])+" \u00B1 "+"{:.2e}".format(DS[1][0])+")\t"
        #s+="\u03c3\u2082\u2082=({:+.2e}".format(S[1][1])+" \u00B1 "+"{:.2e}".format(DS[1][1])+")\t"
        #s+="\u03c3\u2082\u2083=({:+.2e}".format(S[1][2])+" \u00B1 "+"{:.2e}".format(DS[1][2])+")\n"
        #s+="\u03c3\u2083\u2081=({:+.2e}".format(S[2][0])+" \u00B1 "+"{:.2e}".format(DS[2][0])+")\t"
        #s+="\u03c3\u2083\u2082=({:+.2e}".format(S[2][1])+" \u00B1 "+"{:.2e}".format(DS[2][1])+")\t"
        #s+="\u03c3\u2083\u2083=({:+.2e}".format(S[2][2])+" \u00B1 "+"{:.2e}".format(DS[2][2])+")\n"


        W,V=np.linalg.eig(self.S)
        idx = np.argsort(W)
        W = W[idx]
        V = V[:,idx]
        #s+="\n"
        #s+="\u03c3\u2081={:+.2e}".format(W[2])+"\t"
        #s+="\u03c3\u2082={:+.2e}".format(W[1])+"\t"
        #s+="\u03c3\u2083={:+.2e}".format(W[0])+"\n"

        #mises=np.sqrt(0.5*((W[2]-W[1])**2+(W[1]-W[0])**2+(W[2]-W[0])**2))
        #tesca=np.maximum(np.maximum(np.abs(W[2]-W[1]),np.abs(W[2]-W[0])),np.abs(W[1]-W[0]))
        #hydro=(W[0]+W[1]+W[2])/3.0
        #s+="\n"
        #s+="Mises={:+.2e}".format(mises)+"\t"
        #s+="Tresca={:+.2e}".format(tesca)+"\t"
        #s+="Hydro={:+.2e}".format(hydro)+"\n"
        #self.Tensor.setText(s)

        #K=None
        #if self.k:
        #    K=self.k[self.ipro]
        #print(len(self.k))

        phi=self.PhiUSER.PHI.value()*np.pi/180.0
        K=[phi,np.array([np.cos(phi),np.sin(phi),0.0])]
        
        self.Tensor.Set(self.S,self.DS,W,K)




        
        #self.figure.clear()
        #ax = self.figure.add_subplot(111)

        #theta = np.linspace( 0 , np.pi , 180 )
        #c1=(W[1]+W[0])/2.0
        #r1=np.abs(W[0]-W[1])/2.0
        #a1 = r1 * np.cos( theta ) + c1
        #b1 = r1 * np.sin( theta )
        #ax.plot(a1,b1)

        #c2=(W[2]+W[0])/2.0
        #r2=np.abs(W[0]-W[2])/2.0
        #a2 = r2 * np.cos( theta ) + c2
        #b2 = r2 * np.sin( theta )
        #ax.plot(a2,b2)

        #c3=(W[2]+W[1])/2.0
        #r3=np.abs(W[2]-W[1])/2.0
        #a3 = r3 * np.cos( theta ) + c3
        #b3 = r3 * np.sin( theta )
        #ax.plot(a3,b3)

        #ax.plot(0,0)

        #ax.spines['left'].set_position('zero')
        #ax.spines['right'].set_color('none')
        #ax.spines['bottom'].set_position('zero')
        #ax.spines['top'].set_color('none')

        #ax.set_ylim(bottom=0)
        #ax.set_aspect('equal')

        #self.canvas.draw()




    def Set(self):
        self.Set1()
        self.Set2()
        self.Set3()
        


        

class StressWidget2(QGroupBox):
    def __init__(self):
        super(StressWidget2, self).__init__(parent=None)
        #self.horizontalGroupBox = QGroupBox("Grid")
        #self.setGeometry(10, 10, 10, 10)
        layout = QGridLayout()
        layout.setHorizontalSpacing(0.0)
        layout.setVerticalSpacing(0.0)
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)
        ##layout.setColumnStretch(0, 4)

        #layout.addItem(QPushButton('1'))
        #layout.addItem(QPushButton('2'))
        #layout.addItem(QPushButton('3'))
        #layout.addWidget(QPushButton('1'),0,0)
        #layout.addWidget(QPushButton('2'),0,1)
        #layout.addWidget(QPushButton('3'),0,2)
        #layout.addWidget(QPushButton('4'),1,0)
        #layout.addWidget(QPushButton('5'),1,1)
        #layout.addWidget(QPushButton('6'),1,2)
        #layout.addWidget(QPushButton('7'),2,0)
        #layout.addWidget(QPushButton('8'),2,1)
        #layout.addWidget(QPushButton('9'),2,2)
        self.setLayout(layout)
        
        #self.horizontalGroupBox.setLayout(layout)
    def Set(self,S,DS):
        return
        


class ComputeWidget(QWidget):
    def __init__(self,parent=None, model=None):
        super(ComputeWidget, self).__init__(parent)
        self.model=model
        layout = QVBoxLayout(self)
        self.SIGMA1=QRadioButton("Uniaxial along s1 (free surface)",self)
        self.SIGMA2=QRadioButton("Uniaxial along s2 (free surface)",self)
        self.SIGMA3=QRadioButton("Biaxial along s1 and s2 (free surface)",self)
        self.SIGMA5=QRadioButton("Triaxial along s1, s2 and s3 (free surface)",self)
        self.SIGMA6=QRadioButton("Triaxial along s1, s2 and s3 (constrained surface)",self)
        self.SIGMA3.setChecked(True)
        layout.addWidget(self.SIGMA1)
        layout.addWidget(self.SIGMA2)
        layout.addWidget(self.SIGMA3)
        layout.addWidget(self.SIGMA5)
        layout.addWidget(self.SIGMA6)
        self.run = QPushButton("Evaluate")
        self.run.clicked.connect(self.Submit)
        layout.addWidget(self.run)

        self.Stress=StressWidget(self.model)#QLabel("")
        self.Stress.Update(np.zeros((3,3)),np.zeros((3,3)))
        self.Stress.Set()
        layout.addWidget(self.Stress)

        



    #def SetStress(self,S,DS):
    #    s="Stress\n"
    #    for i in range(3):
    #            for j in range(3):
    #                 s+="({:+.2e}".format(S[i][j])+" \u00B1 "+"{:.2e}".format(DS[i][j])+")\t"
    #            s+="\n"
    #    self.Stress.setText(s)
         
    def Submit(self):
        NSIGMA=0
        ISIGMA=0
        if self.SIGMA1.isChecked():
            NSIGMA=1
            ISIGMA=1
        elif self.SIGMA2.isChecked():
            NSIGMA=1
            ISIGMA=2     
        elif self.SIGMA3.isChecked():
            NSIGMA=3
            ISIGMA=3
        elif self.SIGMA5.isChecked():
            NSIGMA=5
            ISIGMA=5
        elif self.SIGMA6.isChecked():
            NSIGMA=6
            ISIGMA=6
        try:
            S,DS=self.model.Compute(NSIGMA,ISIGMA)
            self.Stress.Update(S,DS)
            self.Stress.Set()
            #self.Stress.Set2()
            #self.Stress.Set3()
            #print(S)
        except BaseException as e:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(str(e))
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()

  
