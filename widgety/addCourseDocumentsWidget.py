from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QPushButton, QFileDialog
class addCourseDocumentsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.fileList = QListWidget()

        buttonLayout = QHBoxLayout()

        self.addFileButton = QPushButton("Dodaj pliki")
        self.addFileButton.clicked.connect(self.addFileButtonListener)

        self.deleteFileButton = QPushButton("Usuń plik")
        self.deleteFileButton.setDisabled(True)
        self.deleteFileButton.clicked.connect(self.deleteFileButtonListener)

        buttonLayout.addWidget(self.addFileButton)
        buttonLayout.addWidget(self.deleteFileButton)

        layout.addWidget(self.fileList)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
    def addFileButtonListener(self):
        fileDialog = QFileDialog()
        fileUrls = fileDialog.getOpenFileUrls()
        for fileUrl in fileUrls[0]:
            if fileUrl.url() != "":
                self.fileList.addItem(fileListItem(fileUrl.fileName(), fileUrl.path().replace("/","",1)))
        if self.fileList.count() != 0:
            self.deleteFileButton.setDisabled(False)
        #print(self.getFileNames())
        #print(self.getFilePaths())

    def deleteFileButtonListener(self):
        self.fileList.takeItem(self.fileList.currentRow())
        if self.fileList.count() == 0:
            self.deleteFileButton.setDisabled(True)

    def getFileNames(self) -> list:
        if self.fileList.count() == 0:
            return []
        returnList = []
        for row in range(self.fileList.count()):
            returnList.append(self.fileList.item(row).text())
        return returnList
    
    def getFilePaths(self) -> list:
        if self.fileList.count() == 0:
            return []
        returnList = []
        for row in range(self.fileList.count()):
            returnList.append(self.fileList.item(row).filePath)
        return returnList

class fileListItem(QListWidgetItem):
    def __init__(self, label:str, filePath:str):
        super().__init__(label)
        self.filePath = filePath