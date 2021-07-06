'''
Das ist unser Code für die Projektarbeit an der Rudolf Diesel Fachschule in Nürnberg.
Der Code ist hauptsächlich zur Steuerung unseres nachhaltigen Süßigkeitenautomaten.

Die Hierarchie des Programms ist wiefolgt:
mainwindow.py
    unitselectwindow.py
        userdialog.py
            motor.py
            PoseModule.py

mainwindow.py
    Wenn eine der drei Süßigkeiten ausgewählt wurde, wird das Object unitselectwindow aufgerufen und die Süßigkeit als ID übergeben und gespeichert.
unitselectwindow.py
    Wenn eine der 4 Übungen ausgewählt wurde, wird das Object userdialog aufgerufen, in dem dann die Kameraauswertung gestartet wird.

'''
# ToDo: GPIOs einbauen und fertig machen
# ToDo: Kommentare anpassen/übersetzen, Code Refactoren um Warnungen zu entfernen.


from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from gpioread import *
import os
from unitselectwindow import UnitSelectWindow


class UI_MainWindow(QMainWindow):
    width = 1920
    height = 1080

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_txt = QLabel
        self.label_jpg = QLabel

        path = os.path.dirname(os.path.abspath(__file__))
        fileWin1 = os.path.join(path, "misc/MainwindowDescr.txt")
        self.fileexpl = open(fileWin1, encoding='utf-8', mode="r").read()

    # SetupUI initialisiert die grundlegenden Fenster Eigenschaften und ruft die Funktionen der anderen Label auf um
    # diese zu erstellen und anzuzeigen.
    def setupUi(self, w, h):
        self.setObjectName("MainWindow")
        self.resize(w, h)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.labelTXT("Platzhalter_Übung_1", 180, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 180, 210)
        self.labelTXT("Platzhalter_Übung_2", 810, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 810, 210)
        self.labelTXT("Platzhalter_Übung_3", 1440, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 1440, 210)
        self.labelTXT(self.fileexpl, 180, 580)

    # LabelTXT zur Anzeige der Süßigkeiten Bezeichnungen und der Erklärung für den Benutzer.
    def labelTXT(self, txt, x, y):
        self.label_txt = QLabel(self)
        self.label_txt.move(x, y)
        self.label_txt.setText(str(txt))
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_txt.adjustSize()

    # LabelJPG zur Anzeige der Bilder der Süßigkeiten
    def labelJPG(self, jpg, x, y):
        path = os.path.dirname(os.path.abspath(__file__))
        self.label_jpg = QLabel(self)
        self.label_jpg.setGeometry(QtCore.QRect(x, y, 300, 300))  # x y width height
        self.label_jpg.setPixmap(QtGui.QPixmap(os.path.join(path, jpg)))
        self.label_jpg.setObjectName("label_jpg")

    # MouseReleaseEvent = "MausLoslassEvent", heißt: Wenn die Maus in den unten bestimmten Bereichen geklickt und die
    # Taste losgelassen wird, werden folgende Funktionen ausgelöst.
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        x = a0.x()
        y = a0.y()
        # Linkes Bild
        if 180 <= x <= 480 and 210 <= y <= 510:
            self.DialogWindowOne()
        # Mittleres Bild
        if 810 <= x <= 810 + 300 and 210 <= y <= 510:
            self.DialogWindowTwo()
        # Rechtes Bild
        if 1440 <= x <= 1440 + 300 and 210 <= y <= 510:
            self.DialogWindowThree()

    # Funktion des ersten Bildes
    def DialogWindowOne(self):
        # Eingänge der Schalter abfragen, ob der Automat überhaupt eingeschalten ist.
        if readInput(5) and readInput(6):
            self.id_sweets = 1
            # Erstellt Objekt win mit Konstruktor UnitSelectWindow und zeigt das erstellte Fenster an. Es wird die ID der
            # ausgewählten Süßigkeit übergeben.
            self.win = UnitSelectWindow(self.id_sweets)
            self.win.setupUI(1920, 1080)
            self.win.show()

    # Funktion des zweiten Bildes
    def DialogWindowTwo(self):
        # Eingänge der Schalter abfragen, ob der Automat überhaupt eingeschalten ist.
        if readInput(5) and readInput(6):
            self.id_sweets = 2
            # Erstellt Objekt win mit Konstruktor UnitSelectWindow und zeigt das erstellte Fenster an. Es wird die ID
            # der ausgewählten Süßigkeit übergeben.
            self.win = UnitSelectWindow(self.id_sweets)
            self.win.setupUI(1920, 1080)
            self.win.show()

    # Funktion des dritten Bildes
    def DialogWindowThree(self):
        # Eingänge der Schalter abfragen, ob der Automat überhaupt eingeschalten ist.
        if readInput(5) and readInput(6):
            self.id_sweets = 3
            # Erstellt Objekt win mit Konstruktor UnitSelectWindow und zeigt das erstellte Fenster an. Es wird die ID der
            # ausgewählten Süßigkeit übergeben.
            self.win = UnitSelectWindow(self.id_sweets)
            self.win.setupUI(1920, 1080)
            self.win.show()


'''
class Controller:

    def __init__(selfs):
        pass

    def show_mainwindow(self):
        self.MainWindow = UI_MainWindow()
        self.MainWindow.switch_window.connect(self.show_unit)
        self.MainWindow.show()

    def show_unit(self):
        self.UnitWindow = UnitSelectWindow(1)
        self.UnitWindow.switch_window.connect(self.show_dialog)
        self.MainWindow.close()
        self.UnitWindow.show()

    def show_dialog(self):
        self.DialogWindow = Ui_Dialog()
        self.DialogWindow.switch_window.connect(self.show_mainwindow)
        self.show_unit.close()
        self.DialogWindow.show()
'''


def main():
    import sys
    app = QApplication(sys.argv)
    # Erstellt Objekt win mit UI_MainWindow() und erstellt im Anschluss das User Interface und zeigt es an.
    win = UI_MainWindow()
    win.setupUi(win.width, win.height)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
