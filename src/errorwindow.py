from PyQt5 import Qt, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QDialog
from PyQt5.QtCore import Qt

from src import gpiocontrol
import settings


class errorwindow(QWidget):
    """
    Erzeugt ein ErrorFenster das den Fehler anzeigt. Kann mit Okay bestätigt werden.
    Fehler IDs:

    ID /    Art    / Beschreibung
    1  /    Error  / RFID Code nicht angelegt - nicht genug Guthaben
    2  /    Error  / RFID noch einmal Scannen
    3  /   Warnung / Füllstand x. Süßigkeit zu niedrig
    4  /    Error  / Plexiglas-Abdeckung nicht montiert
    5  /    Error  / Wartungsschalter Rückseite ausgeschalten
    6  /    Error  / RFID Code ist kein Admin Code
    7  /   Warnung / RFID Chip an Scanner legen.
    8  /    Error  / Füllstand gleich 0.

    """

    def __init__(self, parent=None):
        """
        Konstruktor für errorwindow.
        Initialisiert und erstellt alle dafür vorgesehenen Attribute und Eigenschaften.

        """
        super().__init__(parent)
        self.setWindowTitle("ErrorMsg")
        self.setObjectName("ErrorMsg")
        self.resize(400, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.buttonOk = QPushButton("Ok", self)
        self.textlabel = QLabel(self)
        self.pixlabel = QLabel(self)
        self.greenLED = 26
        self.redLED = 13
        self.yellowLED = 19
        self.sweets = 0

        self.pixmap_error = QPixmap("src/misc/error.png")
        self.smaller_pixmap_error = self.pixmap_error.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.pixmap_warning = QPixmap("src/misc/warning.png")
        self.smaller_pixmap_warning = self.pixmap_warning.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.pixmap_info = QPixmap("src/misc/info.png")
        self.smaller_pixmap_info = self.pixmap_info.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)

    def setupUI(self, ErrID, SweetID=0):
        """
        Erstellt und zeigt das Error Window mit dementsprechenden Fehlern an.

        :param ErrID: (int) : ID des Fehlers, welche im Programm hinterlegt sind.
        :param SweetID: (int) : ID der gewählten Süßigkeit, wird benötigt um anzuzeigen
        welche Süßigkeit genau einen zu niedrigen Füllstand hat.
        :return:
        """
        self.sweets = SweetID
        self.buttonOk.resize(120, 50)
        self.buttonOk.move((400-120)/2, 300-50)
        self.buttonOk.clicked.connect(self.butOK)

        self.textlabel.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.textlabel.move(40, 20)
        self.textlabel.setStyleSheet("color: black; font-weight: bold; font-size: 16px")
        self.textlabel.setWordWrap(True)
        self.textlabel.resize(300, 200)
        self.textlabel.show()

        self.pixlabel.setPixmap(self.smaller_pixmap_error)
        self.pixlabel.move(10, 10)
        self.pixlabel.show()


        self.setStyleSheet(
            "QDialog { background-color: rgb(200,200,200); }"
            "QPushButton { border: 2px solid white; font-size: 10px; font-weight: bold; "
            "background-color: DimGrey; color: white;} "
            "QPushButton::pressed { border: 3px solid grey; }")

        # LEDs werden je nach Fehler geschalten
        if ErrID == 1:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: RFID Code nicht angelegt oder nicht genügend Guthaben!")
        elif ErrID == 2:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: RFID noch einmal scannen!")
        elif ErrID == 3:
            gpiocontrol.writeOutput(self.yellowLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_warning)
            self.textlabel.setText("Warnung: Füllstand " + str(self.sweets) + ". Süßigkeit kleiner gleich 5. Bitte auffüllen.")
        elif ErrID == 4:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: Plexiglas Platte nicht ordnungsgemäß befestigt!")
        elif ErrID == 5:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: Wartungsschalter an der Rückseite ist ausgeschalten!")
        elif ErrID == 6:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: RFID ist kein AdminRFID! Zugriff Verweigert!")
        elif ErrID == 7:
            self.pixlabel.setPixmap(self.smaller_pixmap_info)
            self.textlabel.setText("RFID Chip an den Scanner legen.")
        elif ErrID == 8:
            gpiocontrol.writeOutput(self.redLED, 0)
            gpiocontrol.writeOutput(self.greenLED, 1)
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: Füllstand " + str(self.sweets) + ". Süßigkeit gleich 0.")

        self.show()


    def butOK(self):
        """
        Quittiert den Fehler und ändert die Zustände der LEDs des Automaten.

        :return:
        """
        if settings.errorFour:
            settings.counter += 1
        gpiocontrol.writeOutput(self.greenLED, 0)
        gpiocontrol.writeOutput(self.yellowLED, 1)
        gpiocontrol.writeOutput(self.redLED, 1)
        self.close()