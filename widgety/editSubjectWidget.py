from PyQt5.QtWidgets import QPushButton
from widgety.addSubjectWidget import addSubjectWidget
from widgety.addAssignmentWidget import assignmentListWidgetItem
import os, json
class editSubjectWidget(addSubjectWidget):
    def __init__(self, pathToCms, courseTag, currentRow):
        super().__init__(pathToCms, courseTag)
        self.addSubjectButton.setVisible(False)

        self.pathToCms = pathToCms
        self.courseTag = courseTag
        self.currentRow = currentRow

        #wczytywanie starych wartosci
        with open(os.path.join(pathToCms, courseTag, "metadata.json"), "r") as dataFile:
            jsonData = json.load(dataFile)

        self.subjectData = jsonData["tematy"][currentRow]

        if "nazwa" in self.subjectData.keys():
            self.nazwaLineEdit.setText(self.subjectData["nazwa"])
        else:
            self.nazwaLineEdit.setText("Data corrupted")

        if "opis" in self.subjectData.keys():
            self.opisTextEdit.setText(self.subjectData["opis"])
        else:
            self.opisTextEdit.setText("Data corrupted")

        if "godziny" in self.subjectData.keys():
            self.godzinySpinBox.setValue(int(self.subjectData["godziny"]))
        else:
            self.godzinySpinBox.setValue(1)

        self.editButton = QPushButton("Edytuj temat")
        self.editButton.clicked.connect(self.editButtonListener)

        self.addWidget(self.editButton)

        #zadania
        self.reloadAssignmentList()
        
        self.addAssignmentWidget.assignmentList.currentItemChanged.connect(self.assignmentListSelectionChanged)

        self.addAssignmentWidget.editAssignmentButton = QPushButton("Edytuj zadanie")
        self.addAssignmentWidget.editAssignmentButton.setDisabled(True)
        self.addAssignmentWidget.editAssignmentButton.clicked.connect(self.editAssignmentButtonListener)

        self.addAssignmentWidget.resetFormButton = QPushButton("Resetuj formularz")
        self.addAssignmentWidget.resetFormButton.clicked.connect(self.resetAssignmentForm)

        self.addAssignmentWidget.addWidget(self.addAssignmentWidget.editAssignmentButton)
        self.addAssignmentWidget.addWidget(self.addAssignmentWidget.resetFormButton)
        
    def reloadAssignmentList(self):
            self.addAssignmentWidget.assignmentList.clear()
            self.zadaniaData = self.subjectData["zadania"]
            if self.zadaniaData == []:
                self.addAssignmentWidget.assignmentList.addItem("Nie dodano żadnych zadań")
                self.addAssignmentWidget.assignmentList.setDisabled(True)
            else:
                for zadanie in self.zadaniaData:
                    self.addAssignmentWidget.assignmentList.addItem(assignmentListWidgetItem(zadanie.copy()))

    def resetAssignmentForm(self):
        self.addAssignmentWidget.assignmentList.clearSelection()
        self.addAssignmentWidget.assignmentList.clearFocus()
        self.addAssignmentWidget.nazwaLineEdit.clear()
        self.addAssignmentWidget.opisTextEdit.clear()
        self.addAssignmentWidget.terminLineEdit.clear()
        self.addAssignmentWidget.typComboBox.clear()
        self.addAssignmentWidget.typComboBox.addItems(self.addAssignmentWidget.typy)

    def assignmentListSelectionChanged(self):
        if self.addAssignmentWidget.assignmentList.currentItem() != None:
            currentItemVariables = self.addAssignmentWidget.assignmentList.currentItem().variables
            self.addAssignmentWidget.nazwaLineEdit.setText(currentItemVariables["nazwa"])
            self.addAssignmentWidget.opisTextEdit.setText(currentItemVariables["opis"])
            self.addAssignmentWidget.terminLineEdit.setText(currentItemVariables["termin"])
            self.addAssignmentWidget.typComboBox.setCurrentText(currentItemVariables["typ"])
            self.addAssignmentWidget.editAssignmentButton.setDisabled(False)
        else:
            self.resetAssignmentForm()
            self.addAssignmentWidget.editAssignmentButton.setDisabled(True)
    def editAssignmentButtonListener(self):
        self.addAssignmentWidget.loadFormData()
        self.addAssignmentWidget.assignmentList.currentItem().variables = self.addAssignmentWidget.dataTemplate.copy()
    
    def editButtonListener(self):
        with open(os.path.join(self.pathToCms, self.courseTag, "metadata.json"), "r+") as oldData:
            data = json.load(oldData)
            self.loadFormData()
            self.dataTemplate["zadania"] = self.addAssignmentWidget.getDictData()
            data["tematy"][self.currentRow] = self.dataTemplate
            oldData.seek(0)
            json.dump(data, oldData, indent=2)
            oldData.truncate()
        self.editButton.setText("Zedytowano temat!")
        


        