'''

Das ist unser Code für die Projektarbeit "nachhaltiger Süßigkeitenautomat" an der Rudolf Diesel
Fachschule in Nürnberg.
Es wird eine Grafikoberfläche angezeigt, auf der man eine von drei Süßigkeiten auswählen muss.
Anschließend darf der Benutzer sich eine Übung aussuchen, die er absolvieren möchte.
Die gewählte Übung wird anschließend mittels Kameraüberwachung ausgewertet. Dies geschieht mit dem Algorithmus von
Mediapipe.
Im Anschluss wird entweder die gewählte Süßigkeit ausgegeben, oder wenn die Übung nicht erfolgreich war,
eine Bestrafung in Form eines gesunden Snacks ausgegeben.

Weitere Systeme die im Hintergrund aktiv sind:
RFID-Scanner, durch auswählen einer Süßigkeit wird mittels TCP-IP Verbindung auf einen Raspberry Pi verbunden und
mitgeteilt dass dieser den RFID Scan vorbereiten soll. Wenn die Lesung eines RFID Codes erfolgreich war, wird dieser
an das Mainprogramm gesendet und ausgewertet. Es wird überwacht, ob der Code genügend Guthaben vorhanden hat und
ob dieser im System angelegt ist.
In der Admin-Maske, die mittels Klick auf das Logo in der unteren Rechten Ecke zu öffnen ist, können RFID Codes angelegt
und Geldwert hinzugefügt und ausgegeben werden.
Die Admin-Maske bietet ebenfalls die Möglichkeit die Füllstände der Süßigkeiten einzusehen und zu ändern.

Diverse Sensoren des Automaten ermöglichen einen störfreien Ablauf, dies wird überwacht mittels eines ErrorHandler-
Prozesses, welcher jede Sekunde die Zustände der GPIO-Inputs des RasPis anfordert. Ist zum Beispiel die Platte zum
nachfüllen geöffnet, darf keiner der Aktoren anlaufen. Um dem Benutzer diese Art der Fehler mitzuteilen wird ein Fehler
auf dem Tablet ausgegeben. Ebenfalls werden verschiedene Status mit LEDs kenntlich gemacht. Mit beheben des Fehlers
und bestätigen per "Okay" wird nochmals überprüft ob der Fehler behoben wurde. Wurde dieser behoben, wird der Automat
für die Benutzung freigegeben.

'''
# ToDo: GPIOs einbauen und fertig machen
# ToDo: Kommentare anpassen/übersetzen, Code Refactoren um Warnungen zu entfernen.
import errno
import os
import socket
import configparser as cp
from time import *

from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

import errorwindow
import adminwindow
import unitselectwindow
import settings

from src.motor import start
from src import gpiocontrol



class MainWindow(QMainWindow):
    width = 1920
    height = 1080
    adminRight = 0

    def __init__(self, parent=None):
        """
        Konstruktor von UI_MainWindow.

        :param parent: N/A
        """
        super().__init__(parent)
        self.admin = adminwindow.adminwindow()
        self.label_txt = QLabel
        self.label_jpg = QLabel
        self.errorLabel = QLabel(self)
        self.TESTBIT = False
        self.error = errorwindow.errorwindow()
        getCounterValues()

        # ErrorMonitor Objekt wird erstellt, dient zur Überwachung der Sensoriken
        self.error_monitor = ErrorMonitor()
        # Thread Objekt wird erstellt, dient als extra Prozess zum ausführen einer Dauerschleife ohne das Main-Programm
        # zu belasten.
        self.thread = QtCore.QThread(self)
        # PyQtSignal wird ausgeführt wenn im ErrorMonitor Objekt .emit ausgeführt wird.
        # CallError ist die Methode zum Anzeigen des ErrorWindows.
        self.error_monitor.error_signal.connect(self.callError)
        # Objekt von ErrorMonitor wird dem Thread Objekt "Thread" zugewiesen.
        self.error_monitor.moveToThread(self.thread)
        # Wenn der Thread "Thread" gestartet ist, wird die Methode "monitor_errors" im Objekt "error_monitor" ausgeführt.
        self.thread.started.connect(self.error_monitor.monitor_errors)
        # Thread wird gestartet
        self.thread.start()



        # path wird als Variable angelegt, um auf den Programmpfad zurückzuverweisen. Diese macht es möglich die
        # Bilder ohne Absoluten Pfad aufzurufen.
        path = os.path.dirname(os.path.abspath(__file__))
        fileWin1 = os.path.join(path, "misc/MainwindowDescr.txt")
        self.fileexpl = open(fileWin1, encoding='utf-8', mode="r").read()

    def setupUi(self):
        """
        Funktion zum initialisieren und erstellen des Fensters der Süßigkeitenauswahl. Aufruf und Init aller
        Labels und Elemente die anzuzeigen sind.

        :return:
        """
        self.setObjectName("MainWindow")
        self.resize(MainWindow.width, MainWindow.height)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.labelTXT("hanuta RIEGEL", 180, 180)
        self.labelJPG("misc/Hanuta_new.jpg", 180, 210)
        self.labelTXT("Knoppers NussRiegel", 810, 180)
        self.labelJPG("misc/Knoppers_new.jpg", 810, 210)
        self.labelTXT("PickUp Choco+Milk", 1440, 180)
        self.labelJPG("misc/PickUp_new.jpg", 1440, 210)
        self.labelJPG("misc/Logo3.png", 1729, 980)
        self.label_jpg.adjustSize()
        self.labelTXT(self.fileexpl, 180, 560)

    @QtCore.pyqtSlot(int)
    def callError(self, ErrID):
        if ErrID == 1:
            self.error.setupUI(4)
            self.error.show()
        elif ErrID == 2:
            self.error.setupUI(5)
            self.error.show()
        elif ErrID == 3:
            self.error.setupUI(3, 4)
            self.error.show()
        elif ErrID == 4:
            self.error.setupUI(8, 4)
            self.error.show()
        # ErrorWindow UI wird vorbereitet und initialisiert
        self.error.setupUI(ErrID)
        self.error.show()

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
        self.label_jpg.setStyleSheet("border: 2px solid black")
        self.label_jpg.setGeometry(QtCore.QRect(x, y, 300, 300))  # x y width height
        self.label_jpg.setPixmap(QtGui.QPixmap(os.path.join(path, jpg)))
        self.label_jpg.setObjectName("label_jpg")

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        Funktion zur Erkennung eines MausReleaseEvents, heißt, wenn die Maus losgelassen wird, werden die Koordinaten x,
        y zurückgegeben. Hier werden ebenfalls die weiteren Fenster ausgeführt. Dazu
        wird überwacht, ob ein RFID Chip vorliegt, ob dieser in der Liste anliegt und ob
        genügend Geldwert hinterlegt ist.
        Wenn benötigt werden Fehler ausgegeben.

        :param a0: -/-
        :return: -/-
        """
        x = a0.x()
        y = a0.y()

        # Linkes Bild
        if 180 <= x <= 480 and 210 <= y <= 510:
            if settings.actValueOne == 0:
                self.error.setupUI(8, 1)
                return
            elif settings.actValueOne <= 5 and not settings.isClicked:
                self.error.setupUI(3, 1)
                settings.isClicked = True
                return
            # Verbindung zum Server wird aufgebaut.
            self.client = client()
            # Befehl an den Server(RasPi) zum vorbereiten des RFID-Scanners
            self.client.send_data("scan")
            # Auf der TCPIP Verbindung hören, ob Daten gesendet wurden und ggf. zu empfangen.
            self.data = self.client.get_data()
            # Empfangene Daten werden auf "globale" Variable gelegt zur Verwendung in mehreren Klassen.
            self.admin.rfid = self.data
            # Wenn Daten vorhanden sind
            if self.data:
                # Prüfe, ob gescannter Code schon im System angelegt ist und ob dessen Wert >= -5 ist.
                if getConfigCodes(self.admin.rfid) and float(getConfigValue(self.admin.rfid)) > -5.0:
                    # Wenn obiges stimmt -> Fahre fort mit Ablauf
                    self.DialogWindow(1, 1920, 1080)
                else:
                    # Wenn obiges nicht stimmt -> Gibt Fehler ID 1 aus, Nicht angelegt bzw nicht genug Guthaben
                    self.error.setupUI(1)
                    return
        # Mittleres Bild
        if 810 <= x <= 810 + 300 and 210 <= y <= 510:
            if settings.actValueTwo == 0:
                self.error.setupUI(8, 2)
                return
            elif settings.actValueTwo <= 5 and not settings.isClicked:
                self.error.setupUI(3, 2)
                settings.isClicked = True
                return
            self.client = client()
            self.client.send_data("scan")
            self.data = self.client.get_data()
            self.admin.rfid = self.data
            if self.data:
                if getConfigCodes(self.admin.rfid) and float(getConfigValue(self.admin.rfid)) > -5.0:
                    self.DialogWindow(2, 1920, 1080)
                else:
                    self.error.setupUI(1)
                    return
        # Rechtes Bild
        if 1440 <= x <= 1440 + 300 and 210 <= y <= 510:
            if settings.actValueThree == 0:
                self.error.setupUI(8, 3)
                return
            elif settings.actValueThree <= 5 and not settings.isClicked:
                self.error.setupUI(3, 3)
                settings.isClicked = True
                return
            self.client = client()
            self.client.send_data("scan")
            self.data = self.client.get_data()
            self.admin.rfid = self.data
            if self.data:
                if getConfigCodes(self.admin.rfid) and float(getConfigValue(self.admin.rfid)) > -5.0:
                    self.DialogWindow(3, 1920, 1080)
                else:
                    self.error.setupUI(1)
                    return
        # Logo unten Rechts, Admin-Maske Aufruf
        if 1729 <= x <= 1900 and 980 <= y <= 1060:
            self.client = client()
            self.client.send_data("scan")
            self.data = self.client.get_data()
            self.admin.rfid = self.data
            print(self.admin.rfid)
            if self.data:
                # Hier werden die Admin RFID´s abgeglichen.
                if self.admin.rfid == "670621518554" or self.admin.rfid == "admincode2" or self.admin.rfid == "rfidcode":
                    print(type(self.admin.rfid))
                    # Wenn gescannter Code mit einem oben übereinstimmt, öffne Admin-Maske
                    self.admin.setupUI()
                    self.admin.show()
                else:
                    # Wenn gescannter Code mit keinem oben übereinstimmt, gib Fehler ID 6 aus -> RFID kein Admin-Code
                    self.error.setupUI(6)
                    return

    def DialogWindow(self, id, w, h):
        """
        Funktion zum ausführen des zweiten Fensters der Benutzeroberfläche Übungsauswahl.

        :param id: (int) Wert zwischen 1-3 bezogen auf die Süßigkeit die ausgewählt wurde.
        :param w: (int) Weite des Fensters
        :param h: (int) Höhe des Fensters
        :return: unitselectwindow Fenster wird ausgeführt
        """
        self.win = unitselectwindow.UnitSelectWindow(id, self.admin.rfid)
        self.win.setupUI(w, h)
        self.win.show()


def getConfigCodes(searchstring):
    """
    Funktion dient zum suchen nach RFID Codes in der Config.ini, damit überprüft
    wird, ob der gegebene RFID Code schon einmal im System aufgetaucht ist oder
    nicht.

    :param searchstring: (string) : String nach dem die Datei durchsucht werden soll.
    :return: (bool) : Gibt True/False zurück wenn Code vorhanden ist oder nicht.
    """
    config = cp.ConfigParser()
    config.read("config.ini")
    for option in config.options("RFID"):
        if option == searchstring:
            del config
            return True


def getConfigValue(searchstring):
    """
    Funktion dient zum auslesen des Geldwerts des gescannten RFID Codes. Damit
    überprüft werden kann, ob genügend Kontingent darauf vorhanden ist.

    :param searchstring: (string) : String nach dem die Datei durchsucht werden soll.
    :return: (string) : Geldwert als String
    """
    config = cp.ConfigParser()
    config.read("config.ini")
    ret = config["RFID"][searchstring]
    del config
    return ret

def getCounterValues():

    config = cp.ConfigParser()
    config.read("config.ini")
    settings.actValueOne = int(config["DEFAULT"]["SweetCountOne"])
    settings.actValueTwo = int(config["DEFAULT"]["SweetCountTwo"])
    settings.actValueThree = int(config["DEFAULT"]["SweetCountThree"])
    settings.actValueFour = int(config["DEFAULT"]["SweetCountFour"])
    del config

class ErrorMonitor(QObject):
    """
    Dient zum sekündlichen Abfragen der Sensoriken mittels Remote GPIO verbindung zum Raspi.
    Wenn ein Eingang nicht so ist wie er sein soll, wird ein Fehler mit der dazugehörigen ID ausgegeben.

    """
    error_signal = QtCore.pyqtSignal(int)
    @QtCore.pyqtSlot()
    def monitor_errors(self):
        """
        Sorgt als Error Handler Thread. Wird sekündlich aufgerufen und wird gecheckt ob Sensorik i. O. ist
        und ob der Füllstand der Bestrafung i.O. ist, da dieser anderweitig nicht ausgewertet werden kann.
        :return:
        """
        once = False
        twice = False
        counter = 0
        while True:
            sleep(1)
            if 5 >= settings.actValueFour > 1 and not once:
                settings.warningFour = True  # Global Warningbit
                once = True  # Speicherbit für einmaligen Aufruf
                self.error_signal.emit(3)  # Aufruf Error 3
            elif once and not settings.warningFour:
                once = False

            if settings.actValueFour == 0 and not twice:
                settings.errorFour = True
                self.error_signal.emit(4)
                if settings.counter > 2:
                    twice = True
            elif twice and not settings.errorFour:
                settings.counter = 0
                twice = False

            # if gpiocontrol.readInput(23):
            #     print("errordetected")
            #     self.error_signal.emit(1)
            # elif gpiocontrol.readInput(6):
            #     print("errordetected")
            #     self.error_signal.emit(2)




class client():
    """
    Dient zum Verbinden auf den Server(RasPi) zum anfragen und empfangen eines RFID-Codes.
    """

    def __init__(self):
        print("Trying to connect")
        TCP_IP = settings.RPiIP
        TCP_PORT = 9999
        self.data = 0
        self.BUFF = 20

        self.s = socket.socket()
        self.s.connect((TCP_IP, TCP_PORT))

    def get_data(self):
        """
        Versucht Daten zu empfangen, wenn etwas schief geht, wird ein interner Fehler ausgegeben damit der Programmablauf
        nicht abbricht.

        :return: (str) : Empfangener RFID Code als string, decoded in utf-8
        """
        try:
            self.data = self.s.recv(self.BUFF)
            sleep(0.5)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                print("No Data was available")
            else:
                print(e)
        return self.data.decode('utf-8')

    def send_data(self, data):
        """
        Sendet die übergebenen Daten an den Server.

        :param data: (str) : Sendet String und encodet in davor in "utf-8".
        :return:
        """
        self.s.send(data.encode())
        print("data sent")


def main():
    import sys
    app = QApplication(sys.argv)
    # Erstellt Objekt win mit UI_MainWindow() und erstellt im Anschluss das User Interface und zeigt es an.
    win = MainWindow()
    # Funktion SetupUI wird ausgeführt, und somit das Fenster initialisiert.
    win.setupUi()
    # Funktion show zeigt das vorher initialisierte Fenster an.
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
