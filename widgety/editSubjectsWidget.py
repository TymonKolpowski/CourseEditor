from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QSpinBox, QMessageBox
from PyQt5.QtCore import Qt
from widgety.addSubjectWidget import addSubjectWidget
from widgety.seeSubjectWidget import seeSubjectWidget
from widgety.editSubjectWidget import editSubjectWidget
import os, json
class editSubjectsWidget(QVBoxLayout):
    def __init__(self, pathToCms, courseTag):
        super().__init__()

        self.mainWidget = QWidget()

        self.pathToCms = pathToCms
        self.courseTag = courseTag

        self.subjectList = QListWidget()
        self.subjectList.currentItemChanged.connect(self.listItemChangedListener)
        self.buttonsToToggle = []
        
        self.layoutHolder = QWidget()

        self.seeSubject = QPushButton("Zobacz temat")
        self.seeSubject.clicked.connect(self.seeSubjectListener)
        self.buttonsToToggle.append(self.seeSubject)

        self.addSubject = QPushButton("Dodaj temat")
        self.addSubject.clicked.connect(self.addSubjectListener)

        self.editSubject = QPushButton("Edytuj temat")
        self.editSubject.clicked.connect(self.editSubjectListener)
        self.buttonsToToggle.append(self.editSubject)

        self.deleteSubject = QPushButton("Usuń temat")
        self.deleteSubject.clicked.connect(self.deleteSubjectListener)
        self.buttonsToToggle.append(self.deleteSubject)

        self.currentCourseLabel = QLabel()
        self.currentCourseLabel.setAlignment(Qt.AlignCenter)
        self.currentCourseLabel.setStyleSheet("font-weight: bold")

        self.disableButtons()

        #ściąganie danych
        self.loadList()
        # jsonData = []
        # with open(os.path.join(pathToCms, courseTag, "metadata.json"), "r") as dataFile:
        #     jsonData = json.load(dataFile)

        # if "nazwa" in jsonData.keys() and "tag" in jsonData.keys():
        #     self.currentCourseLabel.setText(f"Tematy dla kursu {jsonData["nazwa"]} - {jsonData["tag"]}")
        # else:
        #     self.currentCourseLabel.setText("Wystąpił błąd, nie można znaleźć wymaganych danych")
        
        # if "tematy" not in jsonData.keys():
        #     self.subjectList.addItem("Wystąpił błąd, nie można znaleźć wymaganych danych")
        #     self.subjectList.setDisabled(True)
        # else:
        #     if jsonData["tematy"] == []:
        #         self.subjectList.addItem("Nie ma żadnych tematów dla kursu")
        #         self.subjectList.setDisabled(True)
        #     else:
        #         for temat in jsonData["tematy"]:
        #             self.subjectList.addItem(temat["nazwa"])
        
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(self.currentCourseLabel)
        tempLayout.addWidget(self.subjectList)
        tempLayout.addWidget(self.seeSubject)
        tempLayout.addWidget(self.addSubject)
        tempLayout.addWidget(self.editSubject)
        tempLayout.addWidget(self.deleteSubject)
        self.mainWidget.setLayout(tempLayout)
        self.addWidget(self.mainWidget)

    def loadList(self):
        self.subjectList.clear()
        self.subjectList.setEnabled(True)
        with open(os.path.join(self.pathToCms, self.courseTag, "metadata.json"), "r") as dataFile:
            jsonData = json.load(dataFile)

        if "nazwa" in jsonData.keys() and "tag" in jsonData.keys():
            self.currentCourseLabel.setText(f"Tematy dla kursu {jsonData["nazwa"]} - {jsonData["tag"]}")
        else:
            self.currentCourseLabel.setText("Wystąpił błąd, nie można znaleźć wymaganych danych")
        
        if "tematy" not in jsonData.keys():
            self.subjectList.addItem("Wystąpił błąd, nie można znaleźć wymaganych danych")
            self.subjectList.setDisabled(True)
        else:
            if jsonData["tematy"] == []:
                self.subjectList.addItem("Nie ma żadnych tematów dla kursu")
                self.subjectList.setDisabled(True)
            else:
                for temat in jsonData["tematy"]:
                    self.subjectList.addItem(temat["nazwa"])

    def backButtonListener(self):
        temp = QWidget()
        temp.setLayout(self.mainWidget.layout())
        self.mainWidget.setLayout(self.layoutHolder.layout())
        self.loadList()

    def seeSubjectListener(self):
        self.backButton = QPushButton("Wróć")
        self.backButton.clicked.connect(self.backButtonListener)

        self.layoutHolder = QWidget()
        self.layoutHolder.setLayout(self.mainWidget.layout())
        nextLayout = QVBoxLayout()
        nextLayout.addLayout(seeSubjectWidget(self.pathToCms, self.courseTag, self.subjectList.currentRow()))
        nextLayout.addWidget(self.backButton)
        self.mainWidget.setLayout(nextLayout)

    def addSubjectListener(self):
        self.backButton = QPushButton("Wróć")
        self.backButton.clicked.connect(self.backButtonListener)

        self.layoutHolder = QWidget()
        self.layoutHolder.setLayout(self.mainWidget.layout())
        nextLayout = QVBoxLayout()
        nextLayout.addLayout(addSubjectWidget(self.pathToCms, self.courseTag))
        nextLayout.addWidget(self.backButton)
        self.mainWidget.setLayout(nextLayout)

    def editSubjectListener(self):
        self.backButton = QPushButton("Wróć")
        self.backButton.clicked.connect(self.backButtonListener)

        self.layoutHolder = QWidget()
        self.layoutHolder.setLayout(self.mainWidget.layout())
        nextLayout = QVBoxLayout()
        nextLayout.addLayout(editSubjectWidget(self.pathToCms, self.courseTag, self.subjectList.currentRow()))
        nextLayout.addWidget(self.backButton)
        self.mainWidget.setLayout(nextLayout)

    def deleteSubjectListener(self):
        rowToDelete = self.subjectList.currentRow()
        with open(os.path.join(self.pathToCms, self.courseTag, "metadata.json"), "r+") as oldData:
            data = json.load(oldData)
            data["tematy"].pop(rowToDelete)
            oldData.seek(0)
            json.dump(data, oldData, indent=2)
            oldData.truncate()
        self.subjectList.takeItem(rowToDelete)
        self.listItemChangedListener()
        
    def enableButtons(self):
        for button in self.buttonsToToggle:
            button.setDisabled(False)
    def disableButtons(self):
        for button in self.buttonsToToggle:
            button.setDisabled(True)
    def listItemChangedListener(self):
        if self.subjectList.count() == 0:
            self.disableButtons()
        else:
            self.enableButtons()