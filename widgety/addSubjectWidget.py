from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QSpinBox, QListWidget, QScrollArea
from PyQt5.QtCore import Qt
from widgety.addAssignmentWidget import addAssignmentWidget
import os, json
class addSubjectWidget(QVBoxLayout):
    def __init__(self, pathToCms, courseTag):
        super().__init__()

        self.pathToCms = pathToCms
        self.courseTag = courseTag

        #template for json entry
        self.dataTemplate = {
            "nazwa": None,
            "opis": None,
            "godziny": None,
            "zadania": []
        }

        #nazwa
        self.nazwaLayout = QHBoxLayout()
        self.nazwaLabel = QLabel("Nazwa: ")
        self.nazwaLineEdit = QLineEdit()

        self.nazwaLineEdit.textChanged.connect(self.nazwaLineEditListener)

        self.nazwaLayout.addWidget(self.nazwaLabel)
        self.nazwaLayout.addWidget(self.nazwaLineEdit)

        #opis
        self.opisLayout = QHBoxLayout()
        self.opisLabel = QLabel("Opis: ")
        self.opisTextEdit = QTextEdit()
        self.opisTextEdit.setMaximumHeight(50)
        self.opisLayout.addWidget(self.opisLabel)
        self.opisLayout.addWidget(self.opisTextEdit)
        
        #godziny
        self.godzinyLayout = QHBoxLayout()
        self.godzinyLabel = QLabel("Liczba godzin: ")
        self.godzinySpinBox = QSpinBox()
        self.godzinySpinBox.setMaximum(999)
        self.godzinySpinBox.setMinimum(1)
        self.godzinyLayout.addWidget(self.godzinyLabel)
        self.godzinyLayout.addWidget(self.godzinySpinBox)

        #zadania
        self.zadaniaLayout = QVBoxLayout()
        self.zadaniaLabel = QLabel("Zadania")
        self.zadaniaLabel.setAlignment(Qt.AlignCenter)
        self.zadaniaLabel.setStyleSheet("font-weight: bold")
        self.zadaniaLayout.addWidget(self.zadaniaLabel)
        self.addAssignmentWidget = addAssignmentWidget()
        self.zadaniaLayout.addLayout(self.addAssignmentWidget)

        #dodaj temat
        self.addSubjectButton = QPushButton("Dodaj temat")
        self.addSubjectButton.setDisabled(True)
        self.addSubjectButton.clicked.connect(self.addSubjectButtonListener)

        self.addLayout(self.nazwaLayout)
        self.addLayout(self.godzinyLayout)
        self.addLayout(self.opisLayout)

        #zadania w scrollarea
        self.assignmentScrollArea = QScrollArea()
        tempWidget = QWidget()
        tempWidget.setLayout(self.zadaniaLayout)
        tempWidget.setFixedWidth(550)
        self.assignmentScrollArea.setWidget(tempWidget)
        self.addWidget(self.assignmentScrollArea)
        
        self.addWidget(self.addSubjectButton)

    def nazwaLineEditListener(self):
        if self.nazwaLineEdit.text().strip() != "":
            self.addSubjectButton.setDisabled(False)
        else:
            self.addSubjectButton.setDisabled(True)
    
    def loadFormData(self):
        self.dataTemplate["nazwa"] = self.nazwaLineEdit.text().strip()
        self.dataTemplate["opis"] = self.opisTextEdit.toPlainText().strip()
        self.dataTemplate["godziny"] = self.godzinySpinBox.value()
        self.dataTemplate["zadania"] = self.addAssignmentWidget.getDictData()
    
    def addSubjectButtonListener(self):
        with open(os.path.join(self.pathToCms, self.courseTag, "metadata.json"), "r+") as oldData:
            jsonData = json.load(oldData)
            self.loadFormData()
            jsonData["tematy"].append(self.dataTemplate)
            oldData.seek(0)
            json.dump(jsonData, oldData, indent=2)
        self.nazwaLineEdit.clear()
        self.opisTextEdit.clear()
        self.godzinySpinBox.setValue(1)
        self.addAssignmentWidget.assignmentList.clear()
