from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QMessageBox
from widgety.courseDisplayWidget import courseDisplayWidget
from widgety.editCourseWidget import editCourseWidget
from widgety.editSubjectsWidget import editSubjectsWidget
import os, json, shutil
class chooseCourseWidget(QWidget):
	def __init__(self, pathToCms):
		super().__init__()
		self.pathToCms = pathToCms
		
        #przyciski kontrolne
		buttonLayout = QHBoxLayout()
		
		self.seeCourseButton = QPushButton("Zobacz szkolenie")
		self.seeCourseButton.setDisabled(True)
		self.seeCourseButton.clicked.connect(self.seeCourseListener)
		
		self.editCourseButton = QPushButton("Edytuj szkolenie")
		self.editCourseButton.setDisabled(True)
		self.editCourseButton.clicked.connect(self.editCourseListener)
		
		self.editSubjectsButton = QPushButton("Edytuj tematy szkolenia")
		self.editSubjectsButton.setDisabled(True)
		self.editSubjectsButton.clicked.connect(self.editSubjectsListener)

		self.deleteCourseButton = QPushButton("Usun szkolenie")
		self.deleteCourseButton.setDisabled(True)
		self.deleteCourseButton.clicked.connect(self.deleteCourseListener)

		self.courseTagsArray = self.listDirectory(pathToCms)
		layout = QVBoxLayout()
		self.lista = QListWidget()
		def enableDeleteAndEditCourseButton():
			if self.courseTagsArray != []:
				self.seeCourseButton.setDisabled(False)
				self.deleteCourseButton.setDisabled(False)
				self.editCourseButton.setDisabled(False)
				self.editSubjectsButton.setDisabled(False)
		self.lista.itemSelectionChanged.connect(enableDeleteAndEditCourseButton)
		
        #listowanie kursow
		if self.courseTagsArray == False or self.courseTagsArray == []:
			self.lista.addItem(f"{pathToCms} path does not exist or is empty")
			self.disableButtons()
		else:
			for tag in self.courseTagsArray:
				with open(f"{pathToCms}/{tag}/metadata.json", "r") as dataFile:
					jsonData = json.load(dataFile)
					if "nazwa" in jsonData.keys():
						output = f"{jsonData["nazwa"]} - {tag}"
					else:
						output = f"Course metadata corrupted - {tag}"
					self.lista.addItem(QListWidgetItem(output))
			
		
		buttonLayout.addWidget(self.seeCourseButton)
		buttonLayout.addWidget(self.editCourseButton)
		buttonLayout.addWidget(self.editSubjectsButton)
		buttonLayout.addWidget(self.deleteCourseButton)
		
		layout.addWidget(self.lista)
		layout.addLayout(buttonLayout)
		self.setLayout(layout)
		
	def listDirectory(self, path) -> list[str]:
		try:
			return os.listdir(path)
		except FileNotFoundError:
			return False
	def getSelectedCourseTag(self):
		return self.lista.selectedItems()[0].text().split(" - ")[1]
	def seeCourseListener(self):
		temp = QWidget()
		temp.setLayout(self.layout())
		self.setLayout(courseDisplayWidget(self.pathToCms, self.getSelectedCourseTag()))
	def deleteSelectedCourse(self):
		shutil.rmtree(os.path.join(self.pathToCms, self.getSelectedCourseTag()))
		self.lista.takeItem(self.lista.currentRow())
		if self.lista.count() == 0:
			self.disableButtons()
		
	def deleteCourseListener(self):
		messageBox = QMessageBox()
		messageBox.setWindowTitle("Uwaga!")
		messageBox.setText("Czy na pewno chcesz usunąć kurs? Usunie to wszystkie pliki. Tej akcji nie można cofnąć")
		messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		messageBox.setIcon(QMessageBox.Warning)
		odp = messageBox.exec()
		if odp == QMessageBox.Yes:
			self.deleteSelectedCourse()

	def editCourseListener(self):
		temp = QWidget()
		temp.setLayout(self.layout())
		self.setLayout(editCourseWidget(self.pathToCms, self.getSelectedCourseTag()))

	def editSubjectsListener(self):
		temp = QWidget()
		temp.setLayout(self.layout())
		self.setLayout(editSubjectsWidget(self.pathToCms, self.getSelectedCourseTag()))
			
	def disableButtons(self):
		self.seeCourseButton.setDisabled(True)
		self.editCourseButton.setDisabled(True)
		self.editSubjectsButton.setDisabled(True)
		self.deleteCourseButton.setDisabled(True)