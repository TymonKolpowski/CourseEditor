from widgety.addSubjectWidget import addSubjectWidget
from widgety.addAssignmentWidget import assignmentListWidgetItem
from PyQt5.QtWidgets import QLabel
import os, json
class seeSubjectWidget(addSubjectWidget):
    def __init__(self, pathToCms, courseTag, currentRow):
        super().__init__(pathToCms, courseTag)
        self.nazwaLineEdit.setReadOnly(True)
        self.opisTextEdit.setReadOnly(True)
        self.godzinySpinBox.setReadOnly(True)
        self.addSubjectButton.setVisible(False)

        #zadania
        self.addAssignmentWidget.addAssignmentButton.setVisible(False)
        self.addAssignmentWidget.deleteAssignmentButton.setVisible(False)

        self.addAssignmentWidget.nazwaLineEdit.setReadOnly(True)
        self.addAssignmentWidget.opisTextEdit.setReadOnly(True)
        self.addAssignmentWidget.terminLineEdit.setReadOnly(True)
        self.addAssignmentWidget.typComboBox.clear()

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

        #zadania
        self.zadaniaData:list = self.subjectData["zadania"]
        if self.zadaniaData == []:
            self.addAssignmentWidget.assignmentList.addItem("Nie dodano żadnych zadań")
            self.addAssignmentWidget.assignmentList.setDisabled(True)
        else:
            for zadanie in self.zadaniaData:
                self.addAssignmentWidget.assignmentList.addItem(assignmentListWidgetItem(zadanie.copy()))
        
        self.addAssignmentWidget.assignmentList.currentItemChanged.connect(self.assignmentListSelectionChanged)
        
    def assignmentListSelectionChanged(self):
        currentItemVariables = self.addAssignmentWidget.assignmentList.currentItem().variables
        self.addAssignmentWidget.nazwaLineEdit.setText(currentItemVariables["nazwa"])
        self.addAssignmentWidget.opisTextEdit.setText(currentItemVariables["opis"])
        self.addAssignmentWidget.terminLineEdit.setText(currentItemVariables["termin"])
        self.addAssignmentWidget.typComboBox.clear()
        self.addAssignmentWidget.typComboBox.addItem(currentItemVariables["typ"])