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
import socket



class UI_MainWindow(QMainWindow):

    width = 1920
    height = 1080

    def __init__(self, parent=None):
        """
        Konstruktor von UI_MainWindow.

        :param parent: N/A
        """
        super().__init__(parent)
        self.label_txt = QLabel
        self.label_jpg = QLabel


        # path wird als Variable angelegt, um auf den Programmpfad zurückzuverweisen. Diese macht es möglich die
        # Bilder ohne Absoluten Pfad aufzurufen.
        path = os.path.dirname(os.path.abspath(__file__))
        fileWin1 = os.path.join(path, "misc/MainwindowDescr.txt")
        self.fileexpl = open(fileWin1, encoding='utf-8', mode="r").read()

    def setupUi(self):
        """
        Funktion zum initialisieren und erstellen des Fensters der Süßigkeitenauswahl. Aufruf und Init aller
        Labels und Elemente die anzuzeigen sind.

        :param w: (int) Weite des Fensters
        :param h: (int) Höhe des Fensters
        :return:
        """
        self.setObjectName("MainWindow")
        self.resize(UI_MainWindow.width, UI_MainWindow.height)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.labelTXT("Platzhalter_Übung_1", 180, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 180, 210)
        self.labelTXT("Platzhalter_Übung_2", 810, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 810, 210)
        self.labelTXT("Platzhalter_Übung_3", 1440, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 1440, 210)
        self.labelTXT(self.fileexpl, 180, 580)

    def labelTXT(self, txt, x, y):
        """
        Funktion zur erstellung des labelTXT Elements, um einen Text anzuzeigen.

        :param txt: (string) Textstring der in dem Element angezeigt werden soll.
        :param x: (int) Position des Labels in x-Richtung.
        :param y: (int) Position des Labels in y-Richtung.
        :return:
        """
        self.label_txt = QLabel(self)
        self.label_txt.move(x, y)
        self.label_txt.setText(str(txt))
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_txt.adjustSize()

    def labelJPG(self, jpg, x, y):
        """
        Funktion zum anzeigen des Bild-Labels.

        :param jpg: (path) Bildpfad der angezeigt werden soll, Ordnerstruktur beachten.
        :param x: (int) Position des Bildes in x-Richtung.
        :param y: (int) Position des Bildes in y-Richtung.
        :return:
        """
        path = os.path.dirname(os.path.abspath(__file__))
        self.label_jpg = QLabel(self)
        self.label_jpg.setGeometry(QtCore.QRect(x, y, 300, 300))  # x y width height
        self.label_jpg.setPixmap(QtGui.QPixmap(os.path.join(path, jpg)))
        self.label_jpg.setObjectName("label_jpg")

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Funktion zur Erkennung eines MausReleaseEvents, heißt, wenn die Maus losgelassen wird, werden die Koordinaten x,
        y zurückgegeben.

        :param a0: -/-
        :return: -/-
        """
        x = a0.x()
        y = a0.y()
        # Linkes Bild
        if 180 <= x <= 480 and 210 <= y <= 510:
            self.DialogWindow(1, 1920, 1080)
        # Mittleres Bild
        if 810 <= x <= 810 + 300 and 210 <= y <= 510:
            self.DialogWindow(2, 1920, 1080)
        # Rechtes Bild
        if 1440 <= x <= 1440 + 300 and 210 <= y <= 510:
            self.DialogWindow(3, 1920, 1080)

    def DialogWindow(self, id, w, h):
        """
        Funktion zum ausführen des zweiten Fensters der Benutzeroberfläche Übungsauswahl.

        :param id: (int) Wert zwischen 1-3 bezogen auf die Süßigkeit die ausgewählt wurde.
        :param w: (int) Weite des Fensters
        :param h: (int) Höhe des Fensters
        :return: unitselectwindow Fenster wird ausgeführt
        """
        self.win = UnitSelectWindow(id)
        self.win.setupUI(w, h)
        self.win.show()



def main():
    import sys
    from time import sleep
    app = QApplication(sys.argv)
    # Erstellt Objekt win mit UI_MainWindow() und erstellt im Anschluss das User Interface und zeigt es an.
    win = UI_MainWindow()
    # Funktion SetupUI wird ausgeführt, und somit das Fenster initialisiert.
    win.setupUi()
    # Funktion show zeigt das vorher initialisierte Fenster an.
#    win.show()


    s = server()
    if s.conn:
        #s.get_data()
        s.send_data(b"Test")
        sleep(2)
        s.send_data(b"Test2")

    sys.exit(app.exec())

class server:

    def __init__(self):
        self.data = 0
        # Server erstellen
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        print("asdf")

        self.BUFF = 50

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        self.conn, self.addr = s.accept()
        print('Conn', self.addr)

    def get_data(self):
        self.data = self.conn.recv(self.BUFF)
        print(self.data)
        return self.data

    def send_data(self, data):
        print("data sent")
        self.conn.send(data)







if __name__ == "__main__":
    main()
