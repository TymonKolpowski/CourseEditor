from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QScrollArea
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
import os, json

class courseDisplayWidget(QVBoxLayout):
    def __init__(self, pathToCms, courseTag):
        super().__init__()
        scrollArea = QScrollArea()
        scrollWidget = QWidget()

        #zgrywanie danych
        courseData = {}
        with open(os.path.join(pathToCms, courseTag, "metadata.json"), "r") as dataFile:
            courseData = json.load(dataFile)
        
        #nazwa:
        if "nazwa" in courseData.keys():
            nazwa = courseData["nazwa"]
        else:
            nazwa = "Data corrupted"
        nazwaLabel = QLabel(f"Nazwa: {nazwa}")

        #kategoria:
        if "kategoria" in courseData.keys():
            kategoria = courseData["kategoria"]
        else:
            kategoria = "Data corrupted"
        kategoriaLabel = QLabel(f"Kategoria: {kategoria}")

        #godziny:
        if "godziny" in courseData.keys():
            godziny = courseData["godziny"]
        else:
            godziny = "Data corrupted"
        godzinyLabel = QLabel(f"Godziny: {godziny}")

        #banner:
        bannerPath = os.path.join(pathToCms, courseTag, courseData["banner"])
        print(bannerPath)
        bannerImage = QPixmap(bannerPath)
        bannerImage.scaled(200,100)
        bannerImage.isNull()
        if "banner" in courseData.keys():
            bannerLabel = QLabel()
            if bannerImage.isNull():
                bannerLabel.setText("Banner: Error while looking for file")
            else:
                bannerLabel.setPixmap(bannerImage)
                bannerLabel.setScaledContents(True)
                bannerLabel.resize(200,100)
        else:
            banner = "Data corrupted"
            bannerLabel = QLabel(f"Banner: {banner}")

        #tag:
        if "tag" in courseData.keys():
            tag = courseData["tag"]
        else:
            tag = "Data corrupted"
        tagLabel = QLabel(f"Tag: {tag}")

        #pliki:
        plikiLabel = QLabel("Pliki:")
        plikiList = QListWidget()
        plikiLabel.setMinimumWidth(320)
        plikiLabel.setMaximumWidth(320)

        if "pliki" in courseData.keys():
            if courseData["pliki"] == []:
                pliki = "Nie dodano plików"
            else:
                pliki = []
                for plik in courseData["pliki"]:
                    pliki.append(plik)
        else:
            pliki = "Data corrupted"
        
        if type(pliki) == type("str"):
            plikiList.addItem(pliki)
        elif type(pliki) == type([]):
            plikiList.addItems(pliki)

        #tematy:
        tematyLabel = QLabel("Tematy:")
        tematyList = QListWidget()
        tematyLabel.setMinimumWidth(320)
        tematyLabel.setMaximumWidth(320)

        #addToLayout
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(nazwaLabel)
        tempLayout.addWidget(kategoriaLabel)
        tempLayout.addWidget(godzinyLabel)
        tempLayout.addWidget(bannerLabel)
        tempLayout.addWidget(tagLabel)
        tempLayout.addWidget(plikiLabel)
        tempLayout.addWidget(plikiList)
        tempLayout.addWidget(tematyLabel)
        tempLayout.addWidget(tematyList)
        scrollWidget.setLayout(tempLayout)
        scrollArea.setWidget(scrollWidget)
        self.addWidget(scrollArea)