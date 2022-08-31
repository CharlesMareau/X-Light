import sys

#from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QMainWindow, QLabel, QMenuBar, QMenu, QTabWidget, QFormLayout, QLineEdit, QHBoxLayout, QRadioButton, QCheckBox
#from PySide6.QtGui import QCloseEvent, QAction, QKeySequence, QIcon, QPixmap

#from PySide6.QtCore import Qt



#from PySide6.QtCore import QPointF
#from PySide6.QtGui import QPainter
#from PySide6.QtWidgets import QMainWindow, QApplication
#from PySide6.QtCharts import QChart, QChartView, QLineSeries,QScatterSeries 

#from PySide6.QtCore import Slot


from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *


import os





from pathlib import Path


from ..core.read import *
from ..core.model import Model

from .guiReader import *
from .guiInspect import *
from .guiLocalize import *
from .guiCompute import *

from ..config import IconFile

class DodoPushButton(QPushButton):
	def __del__(self):
		print("del")



class TabWidget(QTabWidget):
   def __init__(self, parent = None):

      self.model=model.Model()

      super(TabWidget, self).__init__(parent)
      self.tab1 = ReaderWidget(model=self.model)
      self.tab2 = InspectWidget(model=self.model)
      self.tab3 = LocalizeWidget(model=self.model)
      self.tab4 = ComputeWidget(model=self.model)

      #scroll = QScrollArea()
      #scroll.setWidgetResizable(self)
      #scroll.setWidget(self.tab3)

      #self.tab2.setStyleSheet("background-color: grey;")
      
		
      self.addTab(self.tab1,"Import")
      self.addTab(self.tab2,"Inspect")
      #self.scroll3 = QScrollArea()
      #self.scroll3.setWidget(self.tab3)
      #self.scroll3.setWidgetResizable(True)
      #self.scroll3.viewport().setStyleSheet("background-color: white;")
      self.addTab(self.tab3,"Localize")
      self.addTab(self.tab4,"Evaluate")

      self.setWindowTitle("X Light")

      self.currentChanged.connect(self.onChange)

		
   #@Slot()
   #def openFile(self):
   #   #exts=core.read.GetExt()
   #   filter_ext="Diffraction ("
   #   i=0
   #   for e in core.read.GetExt():
   #     if i>0:
   #       filter_ext+=" *."+e
   #     else:
   #       filter_ext+="*."+e
   #   filter_ext+=");;All Files (*.*)"
   #   #filter_ext="Images (*.png *.xpm *.jpg);;All Files (*.*)"
   #   
   #   fileName = QFileDialog.getOpenFileName(None, "Open File", str(Path.home()), filter_ext, options=QFileDialog.DontUseNativeDialog)
      #fileName = QFileDialog.getOpenFileName(None, "Open Image", str(Path.home()), "Images (*.png *.xpm *.jpg);;All Files (*.*)")
   #   
   #   if fileName[0]:
   #     self.model.ImportFile(str(fileName[0]))
   #   #self.tab1UI()
      
      
   @Slot()  
   def onChange(self,i):
      if (i==1):
         self.tab2.ReLoad()












class MainWindow(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super(MainWindow,self).__init__(parent)
        #self.setWindowIcon(QIcon('/home/crobert/Documents/ToDo/Charles/X-Light/X-Light.gif'))
        #print(IconFile)
        self.setWindowIcon(QIcon(IconFile))
        #self.setWindowIcon(QIcon(QPixmap(IconFile)))
        self.setWindowTitle("X Light")
        #self.resize(400, 200)
        #self.setStyleSheet("background-color: white;")


        self.centralWidget = TabWidget()
        ##self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)



        #self.setStyleSheet("QMenuBar::item:selected {background-color: rgb(209,1,35);} QMenu::item:selected {background-color: rgb(209,1,35);}")

        #self.centralWidget.show()

        #self.centralWidget = toto.Dialog()
        #self.setCentralWidget(self.centralWidget)

        #toto.Dialog()

        #self.plot()

        self._createActions()
        self._connectActions()
        self._createMenuBar()

        #self.button = QPushButton("Import File(s)")
        #self.button.show()
        #self.button.hide()


        #self.profils=[]

        self.show()


    def _createMenuBar(self):
        #menuBar = self.menuBar()
        ## Creating menus using a QMenu object
        #fileMenu = QMenu("&File", self)
        #menuBar.addMenu(fileMenu)
        ## Creating menus using a title
        #editMenu = menuBar.addMenu("&Edit")
        #helpMenu = menuBar.addMenu("&Help")


        menuBar = self.menuBar()
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        # Help menu
        # helpMenu = menuBar.addMenu(QIcon(":help-content.svg"), "&Help")
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)








    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

        self.newAction.setShortcut("Ctrl+N")
        self.openAction.setShortcut("Ctrl+O")
        #self.aboutAction.setShortcut("Ctrl+A")



    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)




    def newFile(self):
        # Logic for creating a new file goes here...
        self.centralWidget.setText("<b>File > New</b> clicked")
        self.centralWidget.deleteLater()
        #self.centralWidget = toto.Dialog()
        self.setCentralWidget(self.centralWidget)

    def openFile(self):

        #exts=core.read.GetExt()
        filter_ext="Diffraction ("
        i=0
        for e in core.read.GetExt():
            if i>0:
                filter_ext+=" *."+e
            else:
                filter_ext+="*."+e
        filter_ext+=");;All Files (*.*)"
        #filter_ext="Images (*.png *.xpm *.jpg);;All Files (*.*)"

        fileName = QFileDialog.getOpenFileName(None, "Open File", str(Path.home()), filter_ext, options=QFileDialog.DontUseNativeDialog)
        #fileName = QFileDialog.getOpenFileName(None, "Open Image", str(Path.home()), "Images (*.png *.xpm *.jpg);;All Files (*.*)")


        if fileName[0]:
            self.centralWidget.setText(str(fileName[0]))
            profils=read.ReadFile(str(fileName[0]))
            if profils:
                self.profils.append(profils)
        else:
            self.centralWidget.setText("<b>File > Open...</b> clicked")




        #self.centralWidget.setText("<b>File > Open...</b> clicked")



    def plot(self):
        #self.series = QLineSeries()
        self.series = QScatterSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)
        self.series.append(QPointF(11, 1))
        self.series.append(QPointF(13, 3))
        self.series.append(QPointF(17, 6))
        self.series.append(QPointF(18, 3))
        self.series.append(QPointF(20, 2))

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("Simple line chart example")

        self._chart_view = QChartView(self.chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)

        #self.centralWidget
        self.setCentralWidget(self._chart_view)



    def saveFile(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")








def run():
    app = QApplication(sys.argv)


    ex = MainWindow()
    #ex = Window()
    #ex = toto.Dialog()
    ex.showMaximized()

    sys.exit(app.exec())
