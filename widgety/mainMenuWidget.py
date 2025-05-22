from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
class mainMenuWidget(QWidget):
	def __init__(self):
		super().__init__()
		layout = QVBoxLayout()
		#-przyciski dla main menu
		self.przegladaj_kat_button = QPushButton("Przeglądaj katalog CMS/media")
		self.dodaj_szkol_button = QPushButton("Dodaj szkolenie")
		self.wybierz_szkol_button = QPushButton("Wybierz szkolenie")
		#-dodawanie przyciskow do layoutu
		layout.addWidget(self.przegladaj_kat_button)
		layout.addWidget(self.dodaj_szkol_button)
		layout.addWidget(self.wybierz_szkol_button)
		self.setLayout(layout)