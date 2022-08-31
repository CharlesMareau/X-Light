
import sys

#from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QMainWindow, QLabel, QMenuBar, QMenu, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox, QGridLayout, QSpinBox, QToolButton, QLCDNumber, QFrame, QVBoxLayout, QListWidget, QListWidgetItem, QDoubleSpinBox, QGroupBox, QScrollArea, QSizeGrip, QSplitter, QTextEdit, QListView

#from PySide6.QtGui import QCloseEvent, QAction, QKeySequence

#from PySide6.QtCore import Qt


#from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen

#from PySide6.QtCore import QFile,QTextStream



#from PySide6.QtCore import QPointF
#from PySide6.QtGui import QPainter
#from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar
#from PySide6.QtCharts import QChart, QChartView, QLineSeries,QScatterSeries,QValueAxis

#from PySide6.QtCore import Slot

#from PySide6.QtCore import Qt


from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *



#import gui.toto as toto
#import gui.tab as tab


from ..core import *



from pathlib import Path
from ..  import config



class OptionWidget(QWidget):
        def __init__(self,parent=None):
                super(OptionWidget,self).__init__(parent)
                layout = QFormLayout(self)
                #layout = QVBoxLayout(self)

                fun=Function()
                #self.show=QCheckBox("show/hide options",self)
                #self.show.setChecked(False)
                #layout.addWidget(self.show)

                #self.show.stateChanged.connect(lambda:self.ShowHide())

                #self.Tol_Noise_Label=QLabel("Noise tolerance")
                #layout.addWidget(self.Tol_Noise_Label)
                self.Tol_Noise=QDoubleSpinBox(self)
                self.Tol_Noise.setSuffix("%")
                self.Tol_Noise.setValue(100.0*fun.Tol_Noise)
                layout.addRow("Background tolerance",self.Tol_Noise)

                #self.Tol_Noise.hide()
                #self.Tol_Noise_Label.hide()

                #self.Tol_Pic_Label=QLabel("Pic tolerance")
                #layout.addWidget(self.Tol_Pic_Label)
                self.Tol_Pic=QDoubleSpinBox(self)
                self.Tol_Pic.setSuffix("%")
                self.Tol_Pic.setValue(100.0*fun.Tol_Pic)
                layout.addRow("Peak tolerance",self.Tol_Pic)

                #self.Tol_Pic.hide()
                #self.Tol_Pic_Label.hide()

                #self.ShowHide()
                
                #layout.addWidget(QLabel("Correction"))
                #self.aaa=QPushButton(self)#QCheckBox("Lorentz",self)
                #layout.addWidget(self.aaa)
                #self.aaa.hide()

        #def ShowHide(self):
        #        if self.show.isChecked():
        #                self.Tol_Noise.show()
        #                self.Tol_Noise_Label.show()
        #                self.Tol_Pic.show()
        #                self.Tol_Pic_Label.show()
        #        else:
        #                self.Tol_Noise.hide()
        #                self.Tol_Noise_Label.hide()
        #                self.Tol_Pic.hide()
        #                self.Tol_Pic_Label.hide()
                
                
                
        def GetValues(self,function):
                function.Tol_Noise=self.Tol_Noise.value()/100.0
                function.Tol_Pic=self.Tol_Pic.value()/100.0

                
                

class CorrectionWidget(QWidget):
        def __init__(self, parent=None):
                super(CorrectionWidget, self).__init__(parent)
                layout = QFormLayout(self)

                #for i in range(100):
                #        layout.addRow(QLabel("Correction"))
                
                layout.addRow(QLabel("Correction"))
                #self.none=QRadioButton("None",self)
                #self.none.setChecked(True)
                #layout.addWidget(self.none)
                self.lorentz=QCheckBox("Lorentz",self)
                #self.lorentz.setChecked(True)
                layout.addRow(self.lorentz)
                
                self.polarisation=QCheckBox("Polarization",self)
                self.polarisation.stateChanged.connect(self.statePolarisation)
                #layout.addWidget(self.polarisation)

                self.theta=QDoubleSpinBox(self)
                self.theta.setDisabled(True)
                #layout.addWidget(self.theta)
                self.theta.setSuffix("\u00B0")
                self.theta.setRange(0.0,360.0)
                layout.addRow(self.polarisation,self.theta)
                
                
                self.absorption=QCheckBox("Absorption",self)
                layout.addRow(self.absorption)
        def statePolarisation(self,state):
                if self.sender() == self.polarisation:
                        if state == Qt.Checked:
                                self.theta.setDisabled(False)
                        else :
                                self.theta.setDisabled(True)
        def GetValues(self,correction):
                correction.Lorentz=self.lorentz.isChecked()
                correction.Polarisation=self.polarisation.isChecked()
                if correction.Polarisation:
                        correction.ThetaM=self.theta.value()
                correction.Absorption=self.absorption.isChecked()
                                



class MaterialWidget(QWidget):
        def __init__(self, parent=None):
                super(MaterialWidget,self).__init__(parent)
                layout = QVBoxLayout(self)
                #layout = QFormLayout(self)
                layout.addWidget(QLabel("Materials"))
                self.list=QListWidget(self)

                #self.list.setStyleSheet("QListView::item:selected{background-color: rgb(209,1,35);}")
                #self.list.setFixedHeight ( 300 )
                self.list.setSortingEnabled(True)
                self.materials=GetMaterialDict()
                for M in self.materials.keys():
                        QListWidgetItem(M,self.list)
                #layout.addRow(self.list)
                #self.split=QSplitter()
                #self.split.addWidget(QTextEdit())
                #self.split.addWidget(QTextEdit())

                self.list.setResizeMode(QListView.Fixed)
                self.list.resizeMode()
                layout.addWidget(self.list)
        def GetValues(self,material):
                if self.list.currentItem():
                        material.ImportFile(self.materials[self.list.currentItem().text()])
                else:
                        raise Exception("Please select a material")


class PicWidget(QWidget):
        def __init__(self, parent=None):
                super(PicWidget, self).__init__(parent)
                layout = QFormLayout(self)
                #layout.addWidget(QLabel("Function"))
                layout.addRow(QLabel("Pic"))
                self.gauss=QRadioButton("Gauss",self)
                layout.addRow(self.gauss)
                self.lorentz=QRadioButton("Lorentz",self)
                layout.addRow(self.lorentz)
                self.pseudovoigt=QRadioButton("Pseudo-Voigt",self)
                layout.addRow(self.pseudovoigt)
                self.pearsonvii=QRadioButton("Pearson VII",self)
                layout.addRow(self.pearsonvii)                
                self.pseudovoigt.setChecked(True)
                self.symmetry=QCheckBox("Symmetry",self)
                self.symmetry.setChecked(True)
                layout.addRow(self.symmetry)
        def GetValues(self,function):
                if self.gauss.isChecked():
                        function.Name="Gauss"
                elif self.lorentz.isChecked():
                        function.Name="Lorentz"
                elif self.pseudovoigt.isChecked():
                        function.Name="PseudoVoigt"
                elif self.pearsonvii.isChecked():
                        function.Name="PearsonVII"
                if self.symmetry.isChecked():
                        function.Symmetry=True
                else:
                        function.Symmetry=False
                


                
                #layout.addWidget(QLabel("Noise"))
                #self.order=QSpinBox(self)
                #self.order.setMinimum(1)
                #self.order.setMaximum(5)
                #layout.addWidget(self.order)

class NoiseWidget(QWidget):
        def __init__(self, parent=None):
                super(NoiseWidget, self).__init__(parent)
                layout = QFormLayout(self)
                #layout.addWidget(QLabel("Noise"))
                self.order=QSpinBox(self)
                self.order.setMinimum(0)
                self.order.setMaximum(99)
                self.order.setValue(1)
                layout.addRow("Background order",self.order)
        def GetValues(self,function):
                function.Noise=self.order.value()
        
class FunctionWidget(QWidget):
        def __init__(self, parent=None):
                super(FunctionWidget, self).__init__(parent)
                layout = QFormLayout(self)
                self.pic=PicWidget(self)
                self.noise=NoiseWidget(self)
                layout.addRow(QLabel("Function"))
                layout.addRow(self.pic)
                layout.addRow(self.noise)
        def GetValues(self,function):
                self.noise.GetValues(function)
                self.pic.GetValues(function)

#class toto(QProgressBar):
#        pass



class LocalizeWidget(QWidget):
        def __init__(self,parent=None, model=None):
                super(LocalizeWidget, self).__init__(parent)
                self.model=model
                layout = QFormLayout(self)
                self.Correction=CorrectionWidget()


                #self.scroll = QScrollArea()
                #scroll.setWidgetResizable(self)
                #self.scroll.setWidget(self.Correction)

                
                layout.addRow(self.Correction)
                self.Materials=MaterialWidget()
                layout.addRow(self.Materials)
                self.Function=FunctionWidget()
                layout.addRow(self.Function)
                self.run = QPushButton("Run")
                self.run.clicked.connect(self.Submit)
                layout.addWidget(self.run)

                
                self.progress=QProgressBar()#toto()

                #self.progress.setStyleSheet("QProgressBar{text-align: center;} QProgressBar::chunk{background-color: rgb(209,1,35);}")
                #self.progress.setStyleSheet("QProgressBar{text-align: center;} QProgressBar::chunk{background-color: darkRed;}")
                #self.progress.setStyleSheet("QProgressBar{text-align: center;}")
                
                layout.addWidget(self.progress)
                self.progress.setValue(0)

                self.export = QPushButton("Export")
                self.export.clicked.connect(self.Export)
                layout.addWidget(self.export)

                
                #self.Options.hide()


                self.showOptions=QCheckBox("Show/Hide options",self)
                self.showOptions.setChecked(False)
                layout.addWidget(self.showOptions)
                self.showOptions.stateChanged.connect(lambda:self.ShowHideOptions())

                self.Options=OptionWidget()
                layout.addRow(self.Options)

                self.ShowHideOptions()
                #self.Noise=NoiseWidget()
                #layout.addWidget(self.Noise)

        def ShowHideOptions(self):
                #self.Options.show()

                if self.showOptions.isChecked():
                        self.Options.show()
                else:
                        self.Options.hide()
        def Submit(self):
                self.progress.setValue(0)
                try:
                        self.Correction.GetValues(self.model.correction)
                        self.Materials.GetValues(self.model.material)
                        self.Function.GetValues(self.model.function)
                        self.Options.GetValues(self.model.function)
                        self.model.Localize(self.progress)
                except BaseException as e:
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Critical)
                        msgBox.setText(str(e))
                        msgBox.setWindowTitle("Error")
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        returnValue = msgBox.exec()

        def Export(self):
                #fileName = QFileDialog.getOpenFileName(None,"Localize data file", str(Path.home()), "Image Files (*.png *.jpg *.bmp)")
                data=self.model.GetLocalizeData()
                if data==[]:
                        #try:
                        #        self.Submit()
                        #except BaseException as e:
                        #        return
                        #data=self.model.GetLocalizeData()
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Critical)
                        msgBox.setText("Localization needs to be performed")
                        msgBox.setWindowTitle("Error")
                        msgBox.setStandardButtons(QMessageBox.Ok)
                        returnValue = msgBox.exec()
                        return
                filename=QFileDialog.getSaveFileName(None,"Localize data file", str(Path.home()),options=QFileDialog.DontUseNativeDialog)
                if filename[0]=="":
                        return
                #print(filename[0])
                #f=QFile(filename[0])
                #f.open(QFile.WriteOnly | QFile.Text)
                #out=QTextStream(f)
                #f.write("data\n")
                
                f=open(filename[0],"w")
                keys=data[0].keys()
                f.write('#')
                for k in keys:
                        f.write(k+" ")
                        if k=="plan_idx":
                                f.write("plan_h plan_k plan_l ")
                        #out << k << " "
                #out << "\n"
                f.write("\n")
                for d in data:
                        #print(d)
                        for k in keys:
                                #out << d[k] << " "
                                #print(type(d[k]))
                                #if d[k] is type(3.14):
                                #        print("double"+str(d[k]))
                                #if d[k] is type(3):
                                #        print("integer"+str(d[k]))
                                f.write(str(d[k])+" ")
                                if k=="plan":
                                         f.write(str(self.model.material.h[d['plan']])+" ")
                                         f.write(str(self.model.material.k[d['plan']])+" ")
                                         f.write(str(self.model.material.l[d['plan']])+" ")
                        #out << "\n"
                        f.write("\n")
                #out << data
                f.close()
		
		

