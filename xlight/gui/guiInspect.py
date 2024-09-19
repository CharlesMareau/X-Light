
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


        #self.EnableButton = QCheckBox("Enable")
        #layout.addWidget(self.EnableButton)

        

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

        #
        # self.test=AngleWidget()
        # self.test.AngleLabel.setText("test"+" ("+"\u00B0"+")")
        # self.test.AngleEdit.setText("1.1")
        # layout.addWidget(self.test)
        # layout.addRow(self.test)

        self.setLayout(layout)


class InfoWidget(QWidget):
    def __init__(self,parent=None):
        super(InfoWidget, self).__init__(parent)

        self.profil=None
        
        self.setFixedWidth(200)
# Vertical layout for information widget
        layout = QFormLayout()

# Create Lock/Unlock Button
        self.LockUnlockButton = QPushButton("Edit angles")
# Create Label and Edit text box for Khi angle
        self.KhiLabel=QLabel()
        self.KhiLabel.setText("\u03c7"+" ("+"\u00B0"+")")
        self.KhiEdit=QLineEdit()
        self.KhiEdit.setMaxLength(10)
        self.KhiEdit.setReadOnly(True)
        self.KhiEdit.validator = QDoubleValidator()
        self.KhiEdit.setValidator(self.KhiEdit.validator)
        self.KhiEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')
# Create Label and Edit text box for Phi angle
        self.PhiLabel=QLabel()
        self.PhiLabel.setText("\u03c6"+" ("+"\u00B0"+")")
        self.PhiEdit=QLineEdit()
        self.PhiEdit.setMaxLength(10)
        self.PhiEdit.setReadOnly(True)
        self.PhiEdit.validator = QDoubleValidator()
        self.PhiEdit.setValidator(self.PhiEdit.validator)
        self.PhiEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')
# Create Label and Edit text box for Gamma angle
        self.GammaLabel=QLabel()
        self.GammaLabel.setText("\u03b3"+" ("+"\u00B0"+")")
        self.GammaEdit=QLineEdit()
        self.GammaEdit.setMaxLength(10)
        self.GammaEdit.setReadOnly(True)
        self.GammaEdit.validator = QDoubleValidator()
        self.GammaEdit.setValidator(self.GammaEdit.validator)
        self.GammaEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')

        self.AngleLabel=QLabel()
        self.AngleLabel.setText("")
        self.EmptyLabel=QLabel()
        self.EmptyLabel.setText("")
        self.EnableLabel=QLabel()
        self.EnableLabel.setText("")
        
        self.TimeLabel=QLabel()
        self.AnodeLabel=QLabel()
        self.R2Label=QLabel()
        
        layout.addWidget(self.KhiLabel)
        layout.addWidget(self.KhiEdit)
        layout.addWidget(self.PhiLabel)
        layout.addWidget(self.PhiEdit)
        layout.addWidget(self.GammaLabel)
        layout.addWidget(self.GammaEdit)
        layout.addWidget(self.LockUnlockButton)
        layout.addWidget(self.AngleLabel)
        layout.addWidget(self.EmptyLabel)
        layout.addWidget(self.TimeLabel)
        layout.addWidget(self.AnodeLabel)
        layout.addWidget(self.R2Label)

        #self.EnableButton = QCheckBox("Enable")
        self.EnableButton = QPushButton("Exclude data")
        # self.EnableButton.setCheckable(True)
        layout.addWidget(self.EnableButton)
        layout.addWidget(self.EnableLabel)


        #redb = QPushButton('Red', self)
        #redb.setCheckable(True)
        #layout.addWidget(redb)
        #self.EnableButton.stateChanged.connect(lambda:self.stateProfil())

        self.LockUnlockButton.clicked.connect(lambda:self.LockUnlock())
        self.Set()

        self.setLayout(layout)
        

    def LockUnlock(self):
        if (self.KhiEdit.isReadOnly()):
            self.LockUnlockButton.setText("Lock angles")
            self.KhiEdit.setReadOnly(False)
            self.KhiEdit.setStyleSheet('QLineEdit {background-color: #ffffff}')
        else:
            self.LockUnlockButton.setText("Edit angles")
            self.KhiEdit.setReadOnly(True)
            self.KhiEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')
        if (self.PhiEdit.isReadOnly()):
            self.PhiEdit.setReadOnly(False)
            self.PhiEdit.setStyleSheet('QLineEdit {background-color: #ffffff}')
        else:
            self.PhiEdit.setReadOnly(True)
            self.PhiEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')
        if (self.GammaEdit.isReadOnly()):
            self.GammaEdit.setStyleSheet('QLineEdit {background-color: #ffffff}')
            self.GammaEdit.setReadOnly(False)
        else:
            self.GammaEdit.setReadOnly(True)
            self.GammaEdit.setStyleSheet('QLineEdit {background-color: #d7d6d5}')
    
    def Set(self,profil=None):
        if profil:
            self.KhiEdit.setText(str(profil.Khi))
            self.PhiEdit.setText(str(profil.Phi))
            self.GammaEdit.setText(str(profil.Gamma))
            time="%1.2f" % (profil.Time)
            self.TimeLabel.setText("Time="+time+"s")
            self.AnodeLabel.setText("Anode="+str(profil.Anode.name))

            self.LockUnlockButton.setVisible(True)
            self.KhiLabel.setVisible(True)
            self.KhiEdit.setVisible(True)
            self.PhiLabel.setVisible(True)
            self.PhiEdit.setVisible(True)
            self.GammaLabel.setVisible(True)
            self.GammaEdit.setVisible(True)
            self.TimeLabel.setVisible(True)
            self.AnodeLabel.setVisible(True)
            #self.R2Label.setVisible(True)
            self.EnableButton.setVisible(True)
            
            if profil.Fun.IsInit:
                R2="%1.3f" % (profil.Fun.r_squared)
                self.R2Label.setText("R\u00b2="+R2)
                self.R2Label.setVisible(True)
            else:
                self.R2Label.setText("R\u00b2=")
                self.R2Label.setVisible(False)
            self.profil=profil
            # if profil.IsEnable:
                # self.EnableButton.setChecked(True)
            # else:
                # self.EnableButton.setChecked(False)
            
            #self.EnableButton.stateChanged.connect(self.stateProfil())
        else:
            self.TimeLabel.setText("Time=")
            self.AnodeLabel.setText("Anode=")
            self.R2Label.setText("R\u00b2=")

            self.LockUnlockButton.setVisible(False)
            self.KhiLabel.setVisible(False)
            self.KhiEdit.setVisible(False)
            self.PhiLabel.setVisible(False)
            self.PhiEdit.setVisible(False)
            self.GammaLabel.setVisible(False)
            self.GammaEdit.setVisible(False)
            self.TimeLabel.setVisible(False)
            self.AnodeLabel.setVisible(False)
            self.R2Label.setVisible(False)
            # self.EnableButton.setChecked(False)
            self.EnableButton.setVisible(False)

        # if self.EnableButton.isChecked():
            # self.EnableButton.setText("Enabled")
            # self.EnableButton.setStyleSheet('QPushButton {background-color: #ffffff}')
        # else:
            # self.EnableButton.setText("Disabled")
            # self.EnableButton.setStyleSheet('QPushButton {background-color: #d7d6d5}')
            #self.profil=None
    #def stateProfil(self):
    #    print("HHH")
    #    if self.profil:
    #        self.profil.SetEnable(self.EnableButton.isChecked())
    #        if self.EnableButton.isChecked():
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
        self.info.EnableButton.clicked.connect(lambda:self.ChangeState())
        self.ChangeState()
        
        self.info.KhiEdit.returnPressed.connect(lambda:self.ModifyKhi())
        self.ModifyKhi()
        self.info.PhiEdit.returnPressed.connect(lambda:self.ModifyPhi())
        self.ModifyPhi()
        self.info.GammaEdit.returnPressed.connect(lambda:self.ModifyGamma())
        self.ModifyGamma()


        self.Displacement.nextButton.clicked.connect(self.Next)
        self.Displacement.lastButton.clicked.connect(self.Last)

        self.Displacement.previousButton.clicked.connect(self.Previous)
        self.Displacement.firstButton.clicked.connect(self.First)

        
        self.setLayout(self.layout)
        self.SetDisplay()


        return
        
    def ModifyKhi(self):
        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            val=float(self.info.KhiEdit.text())
            self.model.profils[self.iprofil].Khi=val
            self.ReLoad()
            self.info.AngleLabel.setText("Khi angle has been edited!")

    def ModifyPhi(self):
        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            val=float(self.info.PhiEdit.text())
            self.model.profils[self.iprofil].Phi=val
            self.ReLoad()
            self.info.AngleLabel.setText("Phi angle has been edited!")

    def ModifyGamma(self):
        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            val=float(self.info.GammaEdit.text())
            self.model.profils[self.iprofil].Gamma=val
            self.ReLoad()
            self.info.AngleLabel.setText("Gamma angle has been edited!")

    def ChangeState(self):
        if self.iprofil>=0 and self.iprofil<len(self.model.profils):
            if self.model.profils[self.iprofil].IsEnable:
                self.model.profils[self.iprofil].SetEnable(False)
                self.info.EnableButton.setText("Include data")
                self.info.EnableButton.setStyleSheet('QPushButton {background-color: #ffffff}')
                self.info.EnableLabel.setText("Profile has been excluded!")
                print("Profile has been excluded!")
            else:
                self.model.profils[self.iprofil].SetEnable(True)
                self.info.EnableButton.setText("Exclude data")
                self.info.EnableButton.setStyleSheet('QPushButton {background-color: #d7d6d5}')
                self.info.EnableLabel.setText("Profile has been included!")
                print("Profile has been included!")
            #self.model.profils[self.iprofil].SetEnable(self.info.EnableButton.isChecked())
            # self.model.profils[self.iprofil].SetEnable(True)
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
        self.info.EnableLabel.setText("")
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
            if self.model.profils[self.iprofil].IsEnable:
                self.info.EnableButton.setText("Exclude data")
                self.info.EnableButton.setStyleSheet('QPushButton {background-color: #d7d6d5}')
            else:
                self.info.EnableButton.setText("Include data")
                self.info.EnableButton.setStyleSheet('QPushButton {background-color: #ffffff}')
            self.ax.plot(ppp.TwoTheta,ppp.Intensity,'*-',label="experiment", color='black')
            if ppp.Fun.IsInit and ppp.IsEnable:
                ii=ppp.GetFunctionData(False)
                self.ax.plot(ppp.TwoTheta,ii, '-',label="model", color="red")
        else:
            self.info.Set()

        self.canvas.draw()
