from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QLineEdit, QSpinBox, QListWidget, QComboBox, QListWidgetItem
class addAssignmentWidget(QVBoxLayout):
    def __init__(self):
        super().__init__()

        #template for json entry
        self.dataTemplate = {
            "nazwa": None,
            "opis": None,
            "termin": None,
            "typ": None
        }

        #lista zadan
        self.assignmentList = QListWidget()
        self.assignmentList.currentItemChanged.connect(self.listItemChangedListener)

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
        
        #termin
        self.terminLayout = QHBoxLayout()
        self.terminLabel = QLabel("Termin: ")
        self.terminLineEdit = QLineEdit()
        self.terminLayout.addWidget(self.terminLabel)
        self.terminLayout.addWidget(self.terminLineEdit)

        #typ
        self.typLayout = QHBoxLayout()
        self.typLabel = QLabel("Typ: ")
        self.typComboBox = QComboBox()
        self.typy = ["praca domowa", "praca na lekcji"]
        for typ in self.typy:
            self.typComboBox.addItem(typ)
        self.typComboBox.setCurrentText(self.typy[0])
        self.typLayout.addWidget(self.typLabel)
        self.typLayout.addWidget(self.typComboBox)

        #dodaj zadanie
        self.addAssignmentButton = QPushButton("Dodaj zadanie")
        self.addAssignmentButton.setDisabled(True)
        self.addAssignmentButton.clicked.connect(self.addAssignmentButtonListener)

        #usun zadanie
        self.deleteAssignmentButton = QPushButton("Usuń zadanie")
        self.deleteAssignmentButton.setDisabled(True)
        self.deleteAssignmentButton.clicked.connect(self.deleteAssignmentButtonListener)

        self.addWidget(self.assignmentList)
        self.addLayout(self.nazwaLayout)
        self.addLayout(self.terminLayout)
        self.addLayout(self.opisLayout)
        self.addLayout(self.typLayout)
        self.addWidget(self.addAssignmentButton)
        self.addWidget(self.deleteAssignmentButton)

    def nazwaLineEditListener(self):
        if self.nazwaLineEdit.text().strip() != "":
            self.addAssignmentButton.setDisabled(False)
        else:
            self.addAssignmentButton.setDisabled(True)
    
    def deleteAssignmentButtonListener(self):
        self.assignmentList.takeItem(self.assignmentList.currentRow())
        self.listItemChangedListener()

    def loadFormData(self):
        self.dataTemplate["nazwa"] = self.nazwaLineEdit.text().strip()
        self.dataTemplate["opis"] = self.opisTextEdit.toPlainText().strip()
        self.dataTemplate["termin"] = self.terminLineEdit.text().strip()
        self.dataTemplate["typ"] = self.typComboBox.currentText()
    
    def addAssignmentButtonListener(self):
        self.loadFormData()
        newItem = None
        newItem = assignmentListWidgetItem(self.dataTemplate.copy())
        self.assignmentList.addItem(newItem)

        # dodawanie customowego itemu
        # item = QListWidgetItem()
        # newItem = assignmentListWidgetItem(self.dataTemplate)
        # item.setSizeHint(newItem.sizeHint())

        # self.assignmentList.addItem(item)
        # self.assignmentList.setItemWidget(item, newItem)
        
        self.nazwaLineEdit.clear()
        self.terminLineEdit.clear()
        self.opisTextEdit.clear()
        self.typComboBox.setCurrentIndex(0)
    
    def listItemChangedListener(self):
        if self.assignmentList.count() == 0:
            self.deleteAssignmentButton.setDisabled(True)
        else:
            self.deleteAssignmentButton.setDisabled(False)
    
    def getDictData(self):
        data = []
        listItems = []
        if self.assignmentList.count() == 0:
            return []
        for x in range(self.assignmentList.count()):
            listItems.append(self.assignmentList.item(x))
        for item in listItems:
            data.append(item.variables)
        return data

class assignmentListWidgetItem(QListWidgetItem):
    def __init__(self, data):
        super().__init__(data["nazwa"])
        self.variables = data

# class assignmentListWidgetItem(QWidget):
#     def __init__(self, data):
#         super().__init__()
#         self.layout = QHBoxLayout()
#         self.nazwaLabel = QLabel(data["nazwa"])
#         self.data = data
#         self.deleteButton = QPushButton("X")
#         self.deleteButton.clicked.connect(self.deleteButtonListener)
#         self.layout.addWidget(self.nazwaLabel)
#         self.layout.addWidget(self.deleteButton)
#         self.setLayout(self.layout)
