import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator, QIntValidator
from PyQt5.QtWidgets import QDialog, QInputDialog, QWidget, QLineEdit, QLabel, QPushButton
import configparser as cp





class adminwindow(QDialog):
    fromAdminGo = 0
    rfid = ""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdminWindow")
        self.setObjectName("AdminWindow")
        self.resize(1600, 900)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.changeMoneyRFID = QLineEdit(self)
        self.moneylabel = QLabel(self)

    def setupUI(self):
        #ButtonINIT
        buttonSweetsOne = QPushButton("Save", self)
        buttonSweetsTwo = QPushButton("Save", self)
        buttonSweetsThree = QPushButton("Save", self)
        buttonSweetsFour = QPushButton("Save", self)
        buttonSweetsReset = QPushButton("Reset all", self)
        buttonScan = QPushButton("Scan RFID", self)
        buttonSet = QPushButton("Set", self)


        #ConfigINIT
        self.config = cp.ConfigParser()
        self.config.read("config.ini")
        self.valOne = self.config['DEFAULT']['SweetCountOne']
        self.valTwo = self.config['DEFAULT']['SweetCountTwo']
        self.valThree = self.config['DEFAULT']['SweetCountThree']
        self.valFour = self.config['DEFAULT']['SweetCountFour']

        #LineEditINIT
        self.inputSweetsOne = QLineEdit(self)
        self.inputSweetsTwo = QLineEdit(self)
        self.inputSweetsThree = QLineEdit(self)
        self.inputSweetsFour = QLineEdit(self)
        self.inputMoney = QLineEdit(self)

        #TxtLabelINIT
        self.textlabel("Anzahl erster Süßigkeit", 30, 55)
        self.textlabel("Anzahl zweiter Süßigkeit", 30, 105)
        self.textlabel("Anzahl dritter Süßigkeit", 30, 155)
        self.textlabel("Anzahl Bestrafung Gesundes", 30, 205)
        self.textlabel("Guthaben:", 500, 400)
        self.textlabel("Set Guthaben:", 700, 400)


        self.moneylabel.resize(50, 40)
        self.moneylabel.move(700, 450)
        self.moneylabel.setAlignment(Qt.AlignmentFlag(Qt.AlignRight))
        self.moneylabel.show()

        #LineEditConfig
        self.inputSweetsOne.resize(50, 30)
        self.inputSweetsTwo.resize(50, 30)
        self.inputSweetsThree.resize(50, 30)
        self.inputSweetsFour.resize(50, 30)
        self.changeMoneyRFID.resize(200, 20)
        self.inputMoney.resize(50, 30)

        self.inputSweetsOne.move(300, 50)
        self.inputSweetsTwo.move(300, 100)
        self.inputSweetsThree.move(300, 150)
        self.inputSweetsFour.move(300, 200)
        self.changeMoneyRFID.move(250, 465)
        self.inputMoney.move(900, 450)

        self.inputSweetsOne.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.inputSweetsTwo.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.inputSweetsThree.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.inputSweetsFour.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.changeMoneyRFID.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.inputMoney.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))

        #LineEditValidator (MinWert 0, MaxWert 10)
        self.inputSweetsOne.setValidator(QIntValidator(0, 10, self))
        self.inputSweetsTwo.setValidator(QIntValidator(0, 10, self))
        self.inputSweetsThree.setValidator(QIntValidator(0, 10, self))
        self.inputSweetsFour.setValidator(QIntValidator(0, 10, self))
        self.inputMoney.setValidator(QIntValidator(0, 50, self))
        #LineEditSetText
        self.inputSweetsOne.setText(str(self.valOne))
        self.inputSweetsTwo.setText(str(self.valTwo))
        self.inputSweetsThree.setText(str(self.valThree))
        self.inputSweetsFour.setText(str(self.valFour))

        #ButtonConfig
        buttonSweetsOne.resize(80, 30)
        buttonSweetsOne.move(350, 50)
        buttonSweetsOne.clicked.connect(self.saveone)

        buttonSweetsTwo.resize(80, 30)
        buttonSweetsTwo.move(350, 100)
        buttonSweetsTwo.clicked.connect(self.savetwo)

        buttonSweetsThree.resize(80, 30)
        buttonSweetsThree.move(350, 150)
        buttonSweetsThree.clicked.connect(self.savethree)

        buttonSweetsFour.resize(80, 30)
        buttonSweetsFour.move(350, 200)
        buttonSweetsFour.clicked.connect(self.savefour)

        buttonSweetsReset.resize(80, 30)
        buttonSweetsReset.move(460, 100)
        buttonSweetsReset.clicked.connect(self.reset)

        buttonScan.resize(120, 50)
        buttonScan.move(500, 450)
        buttonScan.clicked.connect(self.scanrfid)

        buttonSet.resize(80, 30)
        buttonSet.move(1000, 450)
        buttonSet.clicked.connect(self.set)

        self.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255); font-weight: bold; font-size: 12px; border: 2px solid white;}"
                           "QDialog { background-color: rgb(200,200,200); }"
                           "QLabel { font-size: 18px; font-weight: bold; color: black;}"
                           "QPushButton { border: 2px solid white; font-size: 10px; font-weight: bold; "
                           "background-color: DimGrey; color: white;} "
                           "QPushButton::pressed { border: 3px solid grey; }")


    def textlabel(self, text, x, y):
        """
        "UniversalLabel"

        :param text: (str) : Text der angezeigt werden soll.
        :param x: (int) : x-Koordinate
        :param y: (int) : y-Koordinate
        :return:
        """
        label = QLabel(self)
        label.setText(str(text))
        label.resize(250, 40)
        label.move(x, y)
        label.setAlignment(Qt.AlignmentFlag(Qt.AlignRight))
        label.show()

    def saveone(self):
        """
        Speichert den Wert des ersten Feldes in die config.ini.

        :return:
        """
        self.config.set("DEFAULT", "SweetCountOne", self.inputSweetsOne.text())
        cfgfile = open("config.ini", "w")
        self.config.write(cfgfile)
        cfgfile.close()

    def savetwo(self):
        """
        Speichert den Wert des zweiten Feldes in die config.ini.

        :return:
        """
        self.config.set("DEFAULT", "SweetCountTwo", self.inputSweetsTwo.text())
        cfgfile = open("config.ini", "w")
        self.config.write(cfgfile)
        cfgfile.close()

    def savethree(self):
        """
        Speichert den Wert des dritten Feldes in die config.ini.

        :return:
        """
        cfgfile = open("config.ini", "w")
        self.config["DEFAULT"]["SweetCountThree"] = self.inputSweetsThree.text()
        self.config.write(cfgfile)
        cfgfile.close()

    def savefour(self):
        """
        Speichert den Wert des dritten Feldes in die config.ini.

        :return:
        """
        cfgfile = open("config.ini", "w")
        self.config["DEFAULT"]["SweetCountFour"] = self.inputSweetsFour.text()
        self.config.write(cfgfile)
        cfgfile.close()

    def reset(self):
        """
        Setzt alle Werte auf Standardwert (20), speichert diese im Anschluss und aktualisiert
        diese in den Feldern.

        :return:
        """
        self.config.set("DEFAULT", "SweetCountOne", "20")
        self.config.set("DEFAULT", "SweetCountTwo", "20")
        self.config.set("DEFAULT", "SweetCountThree", "20")
        self.config.set("DEFAULT", "SweetCountThree", "20")

        self.valOne = self.config['DEFAULT']['SweetCountOne']
        self.valTwo = self.config['DEFAULT']['SweetCountTwo']
        self.valThree = self.config['DEFAULT']['SweetCountThree']
        self.valFour = self.config['DEFAULT']['SweetCountFour']

        self.inputSweetsOne.setText(str(self.valOne))
        self.inputSweetsTwo.setText(str(self.valTwo))
        self.inputSweetsThree.setText(str(self.valThree))
        self.inputSweetsFour.setText(str(self.valFour))

        cfgfile = open("config.ini", "w")
        self.config.write(cfgfile)
        cfgfile.close()

    def scanrfid(self):
        self.fromAdminGo = 1

    def updateEdit(self):
        self.changeMoneyRFID.setText(str(self.rfid))

        self.config = cp.ConfigParser()
        self.config.read("config.ini")

        if self.config.has_option("RFID", self.rfid):
            print(self.rfid)
            print(self.config["RFID"][self.rfid])
            self.moneylabel.setText(self.config["RFID"][self.rfid])
            self.moneylabel.show()
            self.readRFID = self.config["RFID"][self.rfid]
            print("asdfsad")
        else:
            cfgfile = open("config.ini", "w")
            self.config.set("RFID", self.rfid, "0")
            self.config.write(cfgfile)
            cfgfile.close()


    def set(self):
        self.config["RFID"][self.rfid] = self.inputMoney.text()
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)