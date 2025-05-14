

#from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QMainWindow, QLabel, QMenuBar, QMenu, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox, QComboBox, QVBoxLayout, QToolButton, QDoubleSpinBox, QListWidget, QListWidgetItem
#from PySide6.QtGui import QCloseEvent, QAction, QKeySequence

#from PySide6.QtCore import Slot

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *




from ..core import *
from ..readers import ReaderParameters




from pathlib import Path


#import core.read



from PySide6.QtGui import QAction, QIcon, QKeySequence, QScreen


class ReaderWidget(QWidget):
    def __init__(self,parent=None, model=None):
        super(ReaderWidget, self).__init__(parent)
        layout = QFormLayout(self)
        #layout = QVBoxLayout(self)


        Parameters=ReaderParameters()
        layout.addRow(QLabel("2D Integration"))

        #layout2=QHBoxLayout(self)
        #layout.addWidget(QLabel("\u0394\u03b3"))
        self.DeltaGamma=QDoubleSpinBox(self)
        self.DeltaGamma.setValue(Parameters.DeltaGamma)
        self.DeltaGamma.setRange(0.0,360.0)
        #self.DeltaGamma.setPrefix("\u0394\u03b3 = ")
        self.DeltaGamma.setSuffix("\u00B0")
        layout.addRow("\u0394\u03b3",self.DeltaGamma)

        #layout.addWidget(QLabel("\u03942\u03b8"))
        self.DeltaTwoTheta=QDoubleSpinBox(self)
        self.DeltaTwoTheta.setValue(Parameters.DeltaTwoTheta)
        self.DeltaTwoTheta.setRange(0.0,360.0)
        #self.DeltaTwoTheta.setPrefix("\u03942\u03b8 = ")
        self.DeltaTwoTheta.setSuffix("\u00B0")
        layout.addRow("\u03942\u03b8",self.DeltaTwoTheta)

        #layout2

        self.OldPath=Path.home()
        self.button = QPushButton("Import data")

        #self.button.setStyleSheet("background-color:rgb(209,1,35)")
        
        layout.addRow(self.button)
        self.model=model
        self.button.clicked.connect(self.openFiles)

        self.ImportedFiles=QListWidget(self)
        layout.addRow(self.ImportedFiles)
        self.updateImportedFiles()

        self.clear = QPushButton("Clear data")
        layout.addRow(self.clear)
        #self.model=model
        self.clear.clicked.connect(self.Clear)

    def Clear(self):
        self.model.clear()
        self.updateImportedFiles()
        

        

    def updateImportedFiles(self):
        self.ImportedFiles.clear()
        for M in self.model.files:
            QListWidgetItem(M,self.ImportedFiles)
    

    #@Slot()
    def openFiles(self):
        self.model.reader_parameters.DeltaTwoTheta=self.DeltaTwoTheta.value()
        self.model.reader_parameters.DeltaGamma=self.DeltaGamma.value()
        #self.model.reader_parameters=self.ReaderParameters
        #exts=core.read.GetExt()

        re=GetListReader()
        ff="All Files (*.*);;"
        n=0
        for r in re:
            if n>0:
                ff+=";;"
            ff+=r.FileType+" (*."+r.FileExt+")"
            n+=1
            #print(r.FileExt)

        
        #filter_ext="Diffraction ("
        #i=0
        #for e in read.GetExt():
        #    if i>0:
        #        filter_ext+=" *."+e
        #    else:
        #        filter_ext+="*."+e
        #    i+=1
        #filter_ext+=");;All Files (*.*)"
        #filter_ext="Images (*.png *.xpm *.jpg);;All Files (*.*)"



        #filter = "TXT (*.txt);;PDF (*.pdf)"
        #file_name = QFileDialog()
        #file_name.setFileMode(QFileDialog.ExistingFiles)
        #names = file_name.getOpenFilesNameAndFilter(self, "Open files", "C\\Desktop", filter)
        #print(names)
        fileNames = QFileDialog.getOpenFileNames(None, "Open File(s)", str(self.OldPath), ff, options=QFileDialog.DontUseNativeDialog)
        #print(fileNames[0])

        msg="Error, file can not be opened"
        if fileNames[0]:
            msg=""
            for f in fileNames[0]:
                try:
                    self.model.ImportFile(str(f))
                    self.OldPath=os.path.dirname(f)
                    msg="File "+str(f)+" is opened succefully"
                except BaseException as e:
                    msg=str(e)
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText(msg)
                    msgBox.setWindowTitle("File Reader")
                    msgBox.setStandardButtons(QMessageBox.Ok)

                    returnValue = msgBox.exec()

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Importation is done")
            msgBox.setWindowTitle("File Reader")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.updateImportedFiles()



