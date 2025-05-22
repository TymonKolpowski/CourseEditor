from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QSpinBox, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from widgety.dodajSzkoleniePage import dodajSzkoleniePage
from widgety.addCourseDocumentsWidget import fileListItem
import os, json, shutil
class editCourseWidget(QVBoxLayout):
    def __init__(self, pathToCms, courseTag):
        super().__init__()
        self.mainWidget = dodajSzkoleniePage(pathToCms)
        self.addWidget(self.mainWidget)
        self.pathToCms = pathToCms
        self.courseTag = courseTag
        #ściąganie danych
        jsonData = []
        with open(os.path.join(pathToCms, courseTag, "metadata.json"), "r") as dataFile:
            jsonData = json.load(dataFile)

        #zmienianie wyglądu layoutu

        #nazwa
        nazwa = jsonData["nazwa"] if "nazwa" in jsonData.keys() else "Data corrupted"
        self.mainWidget.nazwaInput.setText(nazwa)

        #kategoria
        kategoria = jsonData["kategoria"] if "kategoria" in jsonData.keys() else "Data corrupted"
        self.mainWidget.wyborKategori.setCurrentIndex(self.mainWidget.wyborKategori.findText(kategoria))

        #liczba godzin
        godziny = jsonData["godziny"] if "godziny" in jsonData.keys() else 1
        self.mainWidget.godzinyInput.setValue(int(godziny))

        #banner
        banner = jsonData["banner"] if "banner" in jsonData.keys() else "Data corrupted"
        self.mainWidget.wgrajBannerLabel.setStyleSheet("color: green")
        self.mainWidget.wgrajBannerLabel.setText(f"Wgrano plik: {QUrl(banner.replace("\\","/")).fileName()}")
        self.mainWidget.bannerUrl = False

        #pliki
        pliki = jsonData["pliki"] if "pliki" in jsonData.keys() else []
        if pliki != []:
            self.mainWidget.addCourseDocuments.deleteFileButton.setDisabled(False)
            for plik in pliki:
                self.mainWidget.addCourseDocuments.fileList.addItem(fileListItem(QUrl(plik.replace("\\","/")).fileName(), plik))

        #zmienianie funkcji i outputu
        self.mainWidget.metadataButton.setText("Edytuj dane szkolenia")
        self.mainWidget.metadataButton.clicked.disconnect()
        self.mainWidget.metadataButton.clicked.connect(self.editCourseListener)

    def editCourseListener(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle("Uwaga!")
        messageBox.setText("Czy na pewno chcesz edytować kurs? Tej akcji nie można cofnąć")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.setIcon(QMessageBox.Warning)
        odp = messageBox.exec()
        if odp == QMessageBox.Yes:
            self.editCourse()

    def getFormValues(self, printValues: bool):
        nazwaValue = self.mainWidget.nazwaInput.text()
        kategoriaValue = self.mainWidget.wyborKategori.currentText()
        godzinyValue = self.mainWidget.godzinyInput.text()
        bannerValue = self.mainWidget.bannerUrl
        courseFiles = self.mainWidget.addCourseDocuments.getFilePaths()
        if self.mainWidget.bannerUrl != "":
            if self.mainWidget.bannerUrl == False:
                bannerValue = False
            else:
                bannerValue = self.mainWidget.bannerUrl.path().replace("/","",1)
        if printValues:
            print(f"Nazwa: {nazwaValue}")
            print(f"Kategoria: {kategoriaValue}")
            print(f"Godziny: {godzinyValue}")
            print(f"Banner: {bannerValue}")
            print(f"Pliki: {courseFiles}")
        return [nazwaValue, kategoriaValue, godzinyValue, bannerValue, courseFiles]

    def editCourse(self):
        if self.mainWidget.checkFormValue(self.getFormValues(True)) == False:
            self.mainWidget.metadataLabel.setText("Nie udało się edytować pliku, któreś pole jest puste")
        else:
            self.mainWidget.metadataLabel.setText("Edytowanie pliku metadanych...")
            formData = self.getFormValues(False)

            plikiArray = []
            newFiles = []
            if formData[4] !=[]:
                for plik in formData[4]:
                    print(plik)
                    if plik == os.path.join(self.mainWidget.plikiFolderName,QUrl(plik).fileName()):
                        plikiArray.append(plik)
                    else:
                        plikiArray.append(os.path.join(self.mainWidget.plikiFolderName, QUrl(plik).fileName()))
                        newFiles.append(plik)
            
            tag = self.mainWidget.generateTag(formData[0])
            dirName = os.path.join(self.pathToCms, tag)

            with open(os.path.join(self.pathToCms, self.courseTag, "metadata.json"), "r+") as oldData:
                jsonData = json.load(oldData)
                oldTag = jsonData["tag"]
                oldPliki = jsonData["pliki"]
                oldDirname = os.path.join(self.pathToCms, oldTag)
                if tag != oldTag:
                    dirName = self.mainWidget.renameDirIfExists(os.path.join(self.pathToCms, tag))

                jsonData["nazwa"] = formData[0]
                jsonData["kategoria"] = formData[1]
                jsonData["godziny"] = formData[2]
                if formData[3] != False:
                    jsonData["banner"] = os.path.join(self.mainWidget.bannerFolderName, QUrl(formData[3]).fileName())
                    try:
                        os.mkdir(os.path.join(oldDirname, self.mainWidget.bannerFolderName+"_new"))
                        shutil.copy(formData[3], os.path.join(oldDirname, self.mainWidget.bannerFolderName+"_new", QUrl(formData[3]).fileName()))
                    except shutil.SameFileError:
                        pass
                jsonData["tag"] = tag
                jsonData["pliki"] = plikiArray
                oldData.seek(0)
                json.dump(jsonData, oldData, indent=1)
                oldData.truncate()
                self.courseTag = tag

            if oldTag != tag:
                os.rename(os.path.join(self.pathToCms, oldTag), dirName)

            if newFiles != []:
                for file in newFiles:
                    self.copyFileToDir(dirName, file, "pliki")
            
            if plikiArray != oldPliki:
                os.rename(os.path.join(dirName, "pliki"), os.path.join(dirName, "old_pliki"))
                oldFiles = os.listdir(os.path.join(dirName, "old_pliki"))
                os.mkdir(os.path.join(dirName, "pliki"))
                for oldFile in oldFiles:
                    shutil.copy(os.path.join(dirName, "old_pliki", oldFile), os.path.join(dirName, "pliki", oldFile))

                shutil.rmtree(os.path.join(dirName, "old_pliki"))
            
            
            if formData[3] != False:
                shutil.rmtree(os.path.join(dirName, self.mainWidget.bannerFolderName))
                os.rename(os.path.join(dirName, self.mainWidget.bannerFolderName+"_new"), os.path.join(dirName, self.mainWidget.bannerFolderName))
            self.mainWidget.metadataLabel.setText("Zedytowano plik metadanych...")
            
    def copyFileToDir(self, dirPath, filePath, finalDirName):
        if os.path.exists(os.path.join(dirPath, finalDirName)) == False:
            os.mkdir(os.path.join(dirPath, finalDirName))
        if os.path.join(dirPath, filePath) == os.path.join(dirPath, finalDirName):
            shutil.copy(os.path.join(dirPath, filePath), os.path.join(dirPath, finalDirName))

                

