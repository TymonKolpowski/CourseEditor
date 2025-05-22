from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QPushButton

class assignmentList(QListWidget):
    def __init__(self):
        super().__init__()

class assignmentListItem(QHBoxLayout):
    def __init__(self, text):
        super().__init__()

        self.label = QLabel(text)
        self.editButton()

