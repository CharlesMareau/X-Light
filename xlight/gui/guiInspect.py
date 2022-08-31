
import sys

#from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QMainWindow, QLabel, QMenuBar, QMenu, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox, QGridLayout, QSpinBox, QToolButton, QLCDNumber, QFrame, QVBoxLayout, QScrollBar
#from PySide6.QtGui import QCloseEvent, QAction, QKeySequence

#from PySide6.QtCore import Qt


#from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen, QPalette



#from PySide6.QtCore import QPointF
#from PySide6.QtGui import QPainter
#from PySide6.QtWidgets import QMainWindow, QApplication
#from PySide6.QtCharts import QChart, QChartView, QLineSeries,QScatterSeries,QValueAxis

#from PySide6.QtCore import Slot

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


#from qtrangeslider import QRangeSlider

#import gui.toto as toto
#import gui.tab as tab


from ..core import *



from pathlib import Path

import numpy as np



class PowerBar(QWidget):
    def __init__(self,parent=None):
        super(PowerBar, self).__init__(parent)


        layout = QHBoxLayout()


        #self.enable = QCheckBox("Enable")
        #layout.addWidget(self.enable)

        

        self.firstButton = QToolButton()
        #icon = QIcon.fromTheme("go-first-symbolic.svg")
        icon = QIcon.fromTheme("go-first", QIcon("xlight/icon/go-first.png"))
        self.firstButton.setIcon(icon)
        layout.addWidget(self.firstButton)


        self.previousButton = QToolButton()
        #icon = QIcon.fromTheme("go-previous-symbolic.svg")
        icon = QIcon.fromTheme("go-previous", QIcon("xlight/icon/go-previous.png"))
        self.previousButton.setIcon(icon)
        layout.addWidget(self.previousButton)


        self.lcd = QLCDNumber()
        #self.lcd.resize(40, 40)
        layout.addWidget(self.lcd)

        self.nextButton = QToolButton()
        #icon = QIcon.fromTheme("go-next-symbolic.svg")
        icon = QIcon.fromTheme("go-next", QIcon("xlight/icon/go-next.png"))
        self.nextButton.setIcon(icon)
        layout.addWidget(self.nextButton)


        self.lastButton = QToolButton()
        #icon = QIcon.fromTheme("go-last-symbolic.svg")
        icon = QIcon.fromTheme("go-last", QIcon("xlight/icon/go-last.png"))
        self.lastButton.setIcon(icon)
        layout.addWidget(self.lastButton)

        self.setLayout(layout)




class InfoWidget(QWidget):
    def __init__(self,parent=None):
        super(InfoWidget, self).__init__(parent)

        self.profil=None
        
        layout = QVBoxLayout()
        self.KhiLabel=QLabel()
        self.PhiLabel=QLabel()
        self.GammaLabel=QLabel()
        self.TimeLabel=QLabel()
        self.AnodeLabel=QLabel()
        self.R2Label=QLabel()
        layout.addWidget(self.KhiLabel)
        layout.addWidget(self.PhiLabel)
        layout.addWidget(self.GammaLabel)
        layout.addWidget(self.TimeLabel)
        layout.addWidget(self.AnodeLabel)
        layout.addWidget(self.R2Label)

        #self.enable = QCheckBox("Enable")
        self.enable = QPushButton()
        self.enable.setCheckable(True)
        layout.addWidget(self.enable)


        #redb = QPushButton('Red', self)
        #redb.setCheckable(True)
        #layout.addWidget(redb)
        #self.enable.stateChanged.connect(lambda:self.stateProfil())
        self.Set()

        self.setLayout(layout)
        
    def Set(self,profil=None):
        if profil:
            khi="%1.2f" % (profil.Khi)
            self.KhiLabel.setText("\u03c7="+khi+"\u00B0")
            phi="%1.2f" % (profil.Phi)
            self.PhiLabel.setText("\u03c6="+phi+"\u00B0")
            gamma="%1.2f" % (profil.Gamma)
            self.GammaLabel.setText("\u03b3="+gamma+"\u00B0")
            time="%1.2f" % (profil.Time)
            self.TimeLabel.setText("Time="+time+"s")
            self.AnodeLabel.setText("Anode="+str(profil.Anode.name))

            self.KhiLabel.setVisible(True)
            self.PhiLabel.setVisible(True)
            self.GammaLabel.setVisible(True)
            self.TimeLabel.setVisible(True)
            self.AnodeLabel.setVisible(True)
            #self.R2Label.setVisible(True)
            self.enable.setVisible(True)
            
            if profil.Fun.IsInit:
                R2="%1.3f" % (profil.Fun.r_squared)
                self.R2Label.setText("R\u00b2="+R2)
                self.R2Label.setVisible(True)
            else:
                self.R2Label.setText("R\u00b2=")
                self.R2Label.setVisible(False)
            self.profil=profil
            if profil.IsEnable:
                self.enable.setChecked(True)
            else:
                self.enable.setChecked(False)
            
            #self.enable.stateChanged.connect(self.stateProfil())
        else:
            self.KhiLabel.setText("\u03c7=")
            self.PhiLabel.setText("\u03c6=")
            self.GammaLabel.setText("\u03b3=")
            self.TimeLabel.setText("Time=")
            self.AnodeLabel.setText("Anode=")
            self.R2Label.setText("R\u00b2=")
            self.KhiLabel.setVisible(False)
            self.PhiLabel.setVisible(False)
            self.GammaLabel.setVisible(False)
            self.TimeLabel.setVisible(False)
            self.AnodeLabel.setVisible(False)
            self.R2Label.setVisible(False)
            self.enable.setChecked(False)
            self.enable.setVisible(False)

        if self.enable.isChecked():
            self.enable.setText("Enable")
            self.enable.setStyleSheet('QPushButton {background-color: green}')
        else:
            self.enable.setText("Disable")
            self.enable.setStyleSheet('QPushButton {background-color: red}')
            #self.profil=None
    #def stateProfil(self):
    #    print("HHH")
    #    if self.profil:
    #        self.profil.SetEnable(self.enable.isChecked())
    #        if self.enable.isChecked():
    #            #self.profil.Enable=True
    #            print("toto")
    #        else:
    #            #self.profil.IsEnable=False
    #            print("tutu")


#from QCharts import *


def format_coord(x, y):
    xlabel=u"2\u03b8="
    ylabel="Intensity="
    xvalue="%1.2f" % (x)
    yvalue="%1.2f" % (y)
    xunity=u"\u00B0"
    yunity=" cps"
    return xlabel+xvalue+xunity+", "+ylabel+yvalue+yunity
    #return '2u\03b8=%1.4f, Intensity=%1.4f' % (x, y)




class InspectWidget(QWidget):
    def __init__(self,parent=None, model=None):
        super(InspectWidget, self).__init__(parent)
        self.model=model



        self.figure = plt.figure()
        self.ax=self.figure.add_subplot(111)
        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        #self.toolbar.removeAction('forward')
        unwanted_buttons=['Back','Forward','Subplots','Customize']
        for x in self.toolbar.actions():
            #print(x.text())
            if x.text() in unwanted_buttons:
                self.toolbar.removeAction(x)

        #self.toolbar.toolitems=[('Home', 'Reset original view', 'home', 'home')]
        #self.toolbar = NavigationToolbar(self.canvas)
        self.layout = QGridLayout(self)
        




        self.Displacement=PowerBar(self)
        self.layout.addWidget(self.Displacement,0,0,1,1)
        self.iprofil=0
        

        #self.layout.addWidget(self.ChartView,1,0,1,1)
        self.layout.addWidget(self.toolbar,0,1,1,1)
        self.layout.addWidget(self.canvas,1,0,1,2)


        self.info=InfoWidget()
        self.layout.addWidget(self.info,1,2)
        self.info.enable.clicked.connect(lambda:self.ChangeState())
        self.ChangeState()


        self.Displacement.nextButton.clicked.connect(self.Next)
        self.Displacement.lastButton.clicked.connect(self.Last)

        self.Displacement.previousButton.clicked.connect(self.Previous)
        self.Displacement.firstButton.clicked.connect(self.First)




        
        self.setLayout(self.layout)
        self.SetDisplay()


        return

    def ChangeState(self):
        #print("zzz")
        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            self.model.profils[self.iprofil].SetEnable(self.info.enable.isChecked())
            self.ReLoad()

    def Next(self):
        self.iprofil+=1
        self.iprofil=min(self.iprofil,len(self.model.profils)-1)
        self.iprofil=max(0,self.iprofil)
        #self.Displacement.lcd.display(self.iprofil+1)
        #self.ReLoad()
        self.SetDisplay()
    def Last(self):
        self.iprofil=len(self.model.profils)-1
        self.iprofil=max(0,self.iprofil)
        #self.Displacement.lcd.display(self.iprofil+1)
        #self.ReLoad()
        self.SetDisplay()

    def Previous(self):
        self.iprofil-=1
        self.iprofil=max(0,self.iprofil)
        #self.Displacement.lcd.display(self.iprofil+1)
        #self.ReLoad()
        self.SetDisplay()
    def First(self):
        self.iprofil=0
        #self.Displacement.lcd.display(self.iprofil+1)
        self.SetDisplay()
        #self.ReLoad()
    def SetDisplay(self):
        self.Displacement.lcd.display(self.iprofil+1)
        self.ReLoad()



    def ReLoad(self):
        self.ax.clear()
        self.ax.set_xlabel(u"2\u03b8 (deg)", fontsize=20)
        self.ax.set_ylabel('Intensity (cps)', fontsize=20)
        self.ax.format_coord = format_coord
        self.figure.tight_layout()

        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            ppp=self.model.profils[self.iprofil]
            self.info.Set(self.model.profils[self.iprofil])
            self.ax.plot(ppp.TwoTheta,ppp.Intensity,'*-',label="experiment", color='black')
            if ppp.Fun.IsInit and ppp.IsEnable:
                ii=ppp.GetFunctionData(False)
                self.ax.plot(ppp.TwoTheta,ii, '-',label="model", color="red")
        else:
            self.info.Set()

        self.canvas.draw()
