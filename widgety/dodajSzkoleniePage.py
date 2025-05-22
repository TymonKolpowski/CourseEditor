from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QSpinBox
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from widgety.addCourseDocumentsWidget import addCourseDocumentsWidget
import os, json, shutil
class dodajSzkoleniePage(QWidget):
	def __init__(self, pathToCms):
		super().__init__()

		self.pathToCms = pathToCms
		self.bannerFolderName = "banner"
		self.plikiFolderName = "pliki"
		#main layout
		layout = QVBoxLayout()
		
		#nazwa
		nazwaLabel = QLabel("Nazwa: ")
		nazwaLabel.setStyleSheet("color: red")
		self.nazwaInput = QLineEdit()
		def nazwaLabelValidation():
			if self.nazwaInput.text().strip() != "":
				nazwaLabel.setStyleSheet("color: green")
			else:
				nazwaLabel.setStyleSheet("color: red")
		self.nazwaInput.textChanged.connect(nazwaLabelValidation)
		nazwaLabel.setBuddy(self.nazwaInput)
		nazwaLayout = QHBoxLayout()
		nazwaLayout.addWidget(nazwaLabel)
		nazwaLayout.addWidget(self.nazwaInput)
		self.nazwaValue = ""
		
		#kategoria
		self.wyborKategori = QComboBox()
		kategorie = ["pierwsza", "druga", "trzecia"]
		for kategoria in kategorie:
			self.wyborKategori.addItem(kategoria)
		kategorieLabel = QLabel("Wybierz kategorię: ")
		kategorieLabel.setStyleSheet("color: green")
		kategorieLabel.setBuddy(self.wyborKategori)
		kategorieLayout = QHBoxLayout()
		kategorieLayout.addWidget(kategorieLabel)
		kategorieLayout.addWidget(self.wyborKategori)
		self.kategoriaValue = ""
		
		#liczba godzin
		godzinyLabel = QLabel("Wybierz liczbę godzin: ")
		godzinyLabel.setStyleSheet("color: green")
		self.godzinyInput = QSpinBox()
		self.godzinyInput.setMaximum(999)
		self.godzinyInput.setMinimum(1)
		godzinyLabel.setBuddy(self.godzinyInput)
		godzinyLayout = QHBoxLayout()
		godzinyLayout.addWidget(godzinyLabel)
		godzinyLayout.addWidget(self.godzinyInput)
		self.godzinyValue = ""

		#wgraj baner
		wgrajBannerLayout = QHBoxLayout()
		wgrajBannerButton = QPushButton("Wgraj banner")
		wgrajBannerButton.clicked.connect(self.wgrajBannerListener)
		self.wgrajBannerLabel = QLabel("Nie wybrano pliku :C")
		self.wgrajBannerLabel.setStyleSheet("color: red")
		wgrajBannerLayout.addWidget(self.wgrajBannerLabel)
		wgrajBannerLayout.addWidget(wgrajBannerButton)
		self.bannerUrl = ""
		
		#NOWOSC - DODAWANIE DOKUMENTOW - PLS DZIALAJ
		self.addCourseDocuments = addCourseDocumentsWidget()

		#plik metadanych
		metadataLayout = QVBoxLayout()
		self.metadataButton = QPushButton("Stwórz plik metadanych")
		self.metadataButton.clicked.connect(self.createMatedataListener)
		#metadataStatus
		self.metadataLabel = QLabel("")
		self.metadataLabel.setFixedHeight(20)
		self.metadataLabel.setAlignment(Qt.AlignCenter)
		metadataLayout.addWidget(self.metadataButton)
		metadataLayout.addWidget(self.metadataLabel)
		
		#dodanie wszystkiego
		layout.addLayout(nazwaLayout)
		layout.addLayout(kategorieLayout)
		layout.addLayout(godzinyLayout)
		layout.addLayout(wgrajBannerLayout)

		layout.addWidget(self.addCourseDocuments)

		layout.addLayout(metadataLayout)
		self.setLayout(layout)
	#listenery
	def wgrajBannerListener(self):
		fileDialog = QFileDialog()
		#fileDialog.setNameFilter({"Image Files (*.png *.jpg *.jpeg)"});
		self.bannerUrl = fileDialog.getOpenFileUrl(filter="Image Files (*.png *.jpg *.jpeg)")[0]
		if self.bannerUrl.url() != "":
			self.wgrajBannerLabel.setText(f"Wgrano plik: {self.bannerUrl.fileName()}")
			self.wgrajBannerLabel.setStyleSheet("color: green")
		else:
			self.bannerUrl = ""
			self.wgrajBannerLabel.setText("Nie wybrano pliku :C")
			self.wgrajBannerLabel.setStyleSheet("color: red")
		
	def getFormValues(self, printValues: bool):
		nazwaValue = self.nazwaInput.text()
		kategoriaValue = self.wyborKategori.currentText()
		godzinyValue = self.godzinyInput.text()
		bannerValue = self.bannerUrl
		courseFiles = self.addCourseDocuments.getFilePaths()
		if self.bannerUrl != "":
			bannerValue = self.bannerUrl.path().replace("/","",1)
		if printValues:
			print(f"Nazwa: {nazwaValue}")
			print(f"Kategoria: {kategoriaValue}")
			print(f"Godziny: {godzinyValue}")
			print(f"Banner: {bannerValue}")
			print(f"Pliki: {courseFiles}")
		return [nazwaValue, kategoriaValue, godzinyValue, bannerValue, courseFiles]
	
	def checkFormValue(self, values: list):
		for value in values:
			if value == "":
				return False
		return True
	
	def createMatedataListener(self):
		if self.checkFormValue(self.getFormValues(False)) == False:
			self.metadataLabel.setText("Nie udało się stworzyć pliku, któreś pole jest puste")
		else:
			self.metadataLabel.setText("Tworzenie pliku metadanych...")
			formData = self.getFormValues(False)

			#editing pliki to relative path
			plikiArray = []
			if formData[4] != []:
				for plik in formData[4]:
					plikiArray.append(os.path.join(self.plikiFolderName, QUrl(plik).fileName()))

			dataTemplate = {
				"nazwa":formData[0],
				"kategoria":formData[1],
				"godziny":formData[2],
				"banner":os.path.join(self.bannerFolderName ,QUrl(formData[3]).fileName()),
				"tag": self.generateTag(formData[0]),
				"pliki": plikiArray,
				"tematy":[]
			}
			if os.path.exists(self.pathToCms) == False:
				os.makedirs(self.pathToCms)
			dirPath = self.renameDirIfExists(os.path.join(self.pathToCms, self.generateTag(formData[0])))
			os.mkdir(dirPath)
			os.mkdir(os.path.join(dirPath, self.plikiFolderName))
			with open(os.path.join(dirPath, f"metadata.json"), "w") as file:
				json.dump(dataTemplate, file, indent=1)

			#kopiowanie bannera
			self.copyFileToDir(dirPath, formData[3], self.bannerFolderName)

			#kopiowanie plików
			for plik in formData[4]:
				self.copyFileToDir(dirPath, plik, "pliki")

			#koniec wszystkiego
			self.metadataLabel.setText("Stworzono plik metadanych")

	def copyFileToDir(self, dirPath, filePath, finalDirName):
		if os.path.exists(os.path.join(dirPath, finalDirName)) == False:
			os.mkdir(os.path.join(dirPath, finalDirName))
		if filePath[1] != ":":
			shutil.copy(os.path.abspath("/"+filePath), os.path.join(dirPath, finalDirName))
		else:
			shutil.copy(os.path.abspath(filePath), os.path.join(dirPath, finalDirName))
	
	def renameDirIfExists(self, dirPath):
		ogDirPath = dirPath
		dirCounter = 1
		while os.path.exists(dirPath):
			dirPath = f"{ogDirPath}({dirCounter})"
			dirCounter += 1
		return dirPath

	def generateTag(self, name: str):

		nameParts = name.strip().split(" ")
		tag = ""
		print(nameParts)
		for part in nameParts:
			if part != "":
				tag += part[0].capitalize()
		return tag

		
	
