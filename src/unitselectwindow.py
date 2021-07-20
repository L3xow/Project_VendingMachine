from time import sleep

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import QtCore, Qt, QtGui
from PyQt5.QtCore import Qt
import os

from src.adminwindow import adminwindow
from userdialog import Ui_Dialog


class UnitSelectWindow(QWidget):

    def __init__(self, id_sweets, rfid, parent=None):
        """
        Konstruktor für UnitSelectWindow.

        :param id_sweets: (int) : Speicher für gewählte Süßigkeit des Benutzers aus der ersten Maske.
        :param parent: N/A
        """
        super().__init__(parent)
        self.id_sweets = id_sweets
        self.label_txt = QLabel
        self.width = 300
        self.height = 300
        self.rfid = rfid

        path = os.path.dirname(os.path.abspath(__file__))
        fileWin1 = os.path.join(path, "misc/MainwindowDescr.txt")
        self.fileexpl = open(fileWin1, encoding='utf-8', mode="r").read()

    def setupUI(self, w, h):
        """
        Funktion zum initialisieren und erstellen des Fensters der Süßigkeitenauswahl. Aufruf und Init aller
        Labels und Elemente die anzuzeigen sind.

        :param w: (int) : Weite des Fensters
        :param h: (int) : Höhe des Fensters
        :return:
        """
        self.setObjectName("UnitSelectWindow")
        self.resize(w, h)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(Qt.FramelessWindowHint)
# ToDo: Planks GIF einfügen
        self.labelGIF("src/misc/Hampelmann.gif", 180, 210)
        self.labelGIF("src/misc/squats.gif", 620, 210)
        self.labelGIF("src/misc/pushup.gif", 1060, 210)
        self.labelGIF("src/misc/burpees.gif", 1500, 210)
        self.labelTXT(self.fileexpl, 180, 580)

        # Text Label für Erklärung
    def labelTXT(self, txt, x, y):
        """
        Funktion zum anzeigen des Text Labels, welche wie in Maske 1 die Erklärung an den Benutzer anzeigen soll.

        :param txt: (string) : String der Erklärung die aus der File "MainwindowDescr.txt" eingelesen wurde.
        :param x: (int) Position des Labels in x-Richtung.
        :param y: (int) Position des Labels in y-Richtung.
        """
        self.label_txt = QLabel(self)
        self.label_txt.move(x, y)
        self.label_txt.setText(str(txt))
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_txt.adjustSize()

        # Label configuration
        # GIF Label
    def labelGIF(self, fileGIF, x, y):
        """
        Funktion zum anzeigen des GIF Labels, welches die verfügbaren Übungen anzeigt.

        :param fileGIF: (path) : Pfad der Animation die angezeigt werden soll.
        :param x: (int) Position der Animation in x-Richtung.
        :param y: (int) Position der Animation in y-Richtung.
        :return:
        """
        self.label_GIF = QLabel("", self)
        self.label_GIF.setGeometry(QtCore.QRect(x, y, self.width, self.height))  # x y width height
        self.label_GIF.setText("")
        self.movie = QMovie(fileGIF)
        self.label_GIF.setMovie(self.movie)
        self.movie.start()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Funktion zur Erkennung eines MausReleaseEvents, heißt, wenn die Maus losgelassen wird, werden die Koordinaten x,
        y zurückgegeben.

        :param a0: -/-
        :return: -/-
        """
        x = a0.x()
        y = a0.y()
        # Leftmost GIF
        if 180 <= x <= 480 and 210 <= y <= 510:
            self.Unit_One()
        # 2nd leftmost GIF
        if 620 <= x <= 620+300 and 210 <= y <= 510:
            self.Unit_Two()
        # 3rd leftmost GIF
        if 1060 <= x <= 1060+300 and 210 <= y <= 510:
            self.Unit_Three()
        # 4th leftmost GIF
        if 1500 <= x <= 1500+300 and 210 <= y <= 510:
            self.Unit_Four()

    # Funktionen um den Dialog zum bestätigen durch den Benutzer zu öffnen, führt auch zu Kameraauswertung
    def Unit_One(self):
        """
        Funktion zum erstellen des Ui_Dialog Objekts der leftmost Übung.

        :return:
        """
        self.w = Ui_Dialog("src/misc/Dialogwindowdescr.txt", "src/misc/Hampelmann.gif", 1, self.id_sweets, 60, self.rfid)
        self.w.setupUI(1600, 900)
        self.close()
        self.w.show()

    def Unit_Two(self):
        """
        Funktion zum erstellen des Ui_Dialog Objekts der 2nd leftmost Übung.

        :return:
        """
        self.w = Ui_Dialog("src/misc/Dialogwindowdescr.txt", "src/misc/squats.gif", 2, self.id_sweets, 120, self.rfid)
        self.w.setupUI(1600, 900)
        self.w.show()
        self.close()

    def Unit_Three(self):
        """
        Funktion zum erstellen des Ui_Dialog Objekts der 3rd leftmost Übung.

        :return:
        """
        self.w = Ui_Dialog("src/misc/Dialogwindowdescr.txt", "src/misc/pushup.gif", 3, self.id_sweets, 60,self.rfid)
        self.w.setupUI(1600, 900)
        self.w.show()
        self.close()

    def Unit_Four(self):
        """
        Funktion zum erstellen des Ui_Dialog Objekts der 4th leftmost Übung.

        :return:
        """
        self.w = Ui_Dialog("src/misc/Dialogwindowdescr.txt", "src/misc/pushup.gif", 4, self.id_sweets, 60, self.rfid)
        self.w.setupUI(1600, 900)
        self.w.show()
        self.close()
