import os
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBar, QFileDialog

from widgety.dodajSzkoleniePage import dodajSzkoleniePage
from widgety.mainMenuWidget import mainMenuWidget
from widgety.chooseCourseWidget import chooseCourseWidget

class CourseEditor(QMainWindow):
	def __init__(self, pathToCms):
		super().__init__()
		
		#sciezka do naszego folderu cms
		self.pathToCms = os.path.join(pathToCms, "media")
		
		#ustawienia okna
		self.setWindowTitle("Course Editor")
		self.setFixedSize(QSize(640,480))
		
		#generuje main menu
		self.useMainMenu()

		#dodaje toolbar
		self.useToolbar()

		#pokaz okno
		self.show()

	#listnery
	def przegladaj_kat_listener(self):
		if os.path.exists(self.pathToCms) == False:
			os.makedirs(self.pathToCms)
		fileDialog = QFileDialog()
		mainUrl = fileDialog.directoryUrl().toString()
		fileDialog.setDirectory(f"{mainUrl}/{self.pathToCms}")
		if fileDialog.exec_() == 0:
			fileDialog.setDirectory(mainUrl)
	# moze bdzie potrzebne
	# def old_przegladaj_kat_listener(self):
	# 	self.setCentralWidget(mediaDisplayWidget(self.list_media_directory()))

	def dodaj_szkol_listener(self):
		self.setCentralWidget(dodajSzkoleniePage(self.pathToCms))

	def wybierz_szkol_listener(self):
		self.setCentralWidget(chooseCourseWidget(self.pathToCms))

	def setListeners(self, widget):
		widget.przegladaj_kat_button.clicked.connect(self.przegladaj_kat_listener)
		widget.dodaj_szkol_button.clicked.connect(self.dodaj_szkol_listener)
		widget.wybierz_szkol_button.clicked.connect(self.wybierz_szkol_listener)

	def useMainMenu(self):
		#dodawanie instancji main menu
		mainWidget = mainMenuWidget()
		#-dodawanie listenerow do przyciskow
		self.setListeners(mainWidget)
		#ustawianie main menu
		self.setCentralWidget(mainWidget)
	
	def useToolbar(self):
		#przycisk do powrotu do menu
		mainMenuButton = QPushButton("Menu główne")
		mainMenuButton.clicked.connect(self.useMainMenu)

		coursesButton = QPushButton("Szkolenia")
		coursesButton.clicked.connect(self.wybierz_szkol_listener)

		addCoursesButton = QPushButton("Dodaj szkolenia")
		addCoursesButton.clicked.connect(self.dodaj_szkol_listener)

		#toolbar
		toolbar = QToolBar("Toolbar")
		toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
		toolbar.addWidget(mainMenuButton)
		toolbar.addWidget(coursesButton)
		toolbar.addWidget(addCoursesButton)
		self.addToolBar(toolbar)

app = QApplication(sys.argv)
course_editor = CourseEditor("cms")
app.exec_()
