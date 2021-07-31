'''

Das ist unser Code für die Projektarbeit "nachhaltiger Süßigkeitenautomat" an der Rudolf Diesel
Fachschule in Nürnberg.
Es wird eine Grafikoberfläche angezeigt, die eine Auswahl einer Süßigkeit von dreien ermöglichen
soll. Anschließend darf der Benutzer sich eine Übung aussuchen, die er absolvieren möchte.
Dies wird mittels des Algorithmus von Mediapipe überwacht und ausgewertet.
Im Anschluss wird entweder die gewählte Süßigkeit ausgegeben, oder wenn die Übung nicht erfolgreich war,
eine Bestrafung in Form eines gesunden Snacks ausgegeben.

Es werden Störungen überwacht und Füllstände ausgewertet.
Ebenfalls gibt es ein RFID System damit die Süßigkeit auch bezahlt werden kann.

'''
# ToDo: GPIOs einbauen und fertig machen
# ToDo: Kommentare anpassen/übersetzen, Code Refactoren um Warnungen zu entfernen.
import errno

from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QRunnable, QThreadPool, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow
from adminwindow import *
import os

from src import gpiocontrol
from src.errorwindow import errorwindow
import socket
from threading import Thread
from time import *

from src.unitselectwindow import UnitSelectWindow


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
        self.admin = adminwindow()
        self.label_txt = QLabel
        self.label_jpg = QLabel
        self.errorLabel = QLabel(self)
        self.running = 0  # not listening
        self.runningerr = 0 # error thread not started
        self.addr = None
        self.conn = None
        self.startScan = 0
        self.gotData = False
        self.TESTBIT = True
        self.error = errorwindow()
        self.error_monitor = ErrorMonitor()
        self.thread = QtCore.QThread(self)
        self.error_monitor.error_signal.connect(self.callError)
        self.error_monitor.moveToThread(self.thread)
        self.thread.started.connect(self.error_monitor.monitor_errors)
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
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.labelTXT("Platzhalter_Übung_1", 180, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 180, 210)
        self.labelTXT("Platzhalter_Übung_2", 810, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 810, 210)
        self.labelTXT("Platzhalter_Übung_3", 1440, 180)
        self.labelJPG("misc/PlaceHolder.jpg", 1440, 210)
        self.labelJPG("misc/Logo3.png", 1729, 980)
        self.label_jpg.adjustSize()
        self.labelTXT(self.fileexpl, 180, 580)

    @QtCore.pyqtSlot(int)
    def callError(self, ErrID):
        self.error.setupUI(ErrID, 0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.ERRORBIT = True
        elif event.key() == Qt.Key_Space and self.ERRORBIT:
            self.ERRORBIT = False

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
            self.client = client()
            self.client.send_data("scan")
            self.data = self.client.get_data()
            self.admin.rfid = self.data
            if self.data:
                if getConfigCodes(self.admin.rfid) and int(getConfigValue(self.admin.rfid)) >= -5:
                    self.DialogWindow(1, 1920, 1080)
                else:
                    self.error.setupUI(1)
            # while self.startScan != 0: # Wenn StartScan != 0 dann Schleife laufen lassen
            #     if self.gotData:
            #         if getConfigCodes(self.admin.rfid) and int(getConfigValue(self.admin.rfid)) >= -5:
            #             print(self.admin.rfid)
            #             self.DialogWindow(1, 1920, 1080)
            #             self.startScan = 0
            #             self.gotData = False
            #             break
            #         else:
            #             print("error")
            #             self.error.setupUI(1)
            #             break
        # Mittleres Bild
        if 810 <= x <= 810 + 300 and 210 <= y <= 510:
            self.startScan = 1  # Eigene Variable zum merken des Starts
            self.admin.fromAdminGo = 1  # Globale Variable zum Scanauftrag schicken
            while self.startScan != 0:  # Wenn StartScan != 0 dann Schleife laufen lassen
                if self.gotData:
                    if getConfigCodes(self.admin.rfid) and int(getConfigValue(self.admin.rfid)) >= -5:
                        print(self.admin.rfid)
                        self.DialogWindow(2, 1920, 1080)
                        self.startScan = 0
                        self.gotData = False
                        break
                    else:
                        self.error.setupUI(1)
                        break
        # Rechtes Bild
        if 1440 <= x <= 1440 + 300 and 210 <= y <= 510:
            self.startScan = 1  # Eigene Variable zum merken des Starts
            self.admin.fromAdminGo = 1  # Globale Variable zum Scanauftrag schicken
            while self.startScan != 0:  # Wenn StartScan != 0 dann Schleife laufen lassen
                if self.gotData:
                    if getConfigCodes(self.admin.rfid) and int(getConfigValue(self.admin.rfid)) >= -5:
                        print(self.admin.rfid)
                        self.DialogWindow(3, 1920, 1080)
                        self.startScan = 0
                        self.gotData = False
                        break
                    else:
                        self.error.setupUI(1)
                        break
        if 1729 <= x <= 1900 and 980 <= y <= 1060:
            self.client = client()
            self.client.send_data("scan")
            self.data = self.client.get_data()
            self.admin.rfid = self.data
            if self.data:
                if self.admin.rfid == "670621518554" or self.admin.rfid == "admincode2" or self.admin.rfid == "rfidcode":
                    print(type(self.admin.rfid))
                    self.admin.setupUI()
                    self.admin.show()
                else:
                    self.error.setupUI(6)


    def DialogWindow(self, id, w, h):
        """
        Funktion zum ausführen des zweiten Fensters der Benutzeroberfläche Übungsauswahl.

        :param id: (int) Wert zwischen 1-3 bezogen auf die Süßigkeit die ausgewählt wurde.
        :param w: (int) Weite des Fensters
        :param h: (int) Höhe des Fensters
        :return: unitselectwindow Fenster wird ausgeführt
        """
        self.win = UnitSelectWindow(id, self.admin.rfid)
        self.win.setupUI(w, h)
        self.win.show()

    # def client_thread(self):
    #     """
    #     Stellt den Server Prozess als Thread dar. Verwaltet sämtliche TCP Angelegenheiten
    #     mit dem Raspberry Pi, um einen Scanbefehl zu erteilen und um den gescannten RFID
    #     Code zurückzugeben.
    #
    #     :return:
    #     """
    #     print("thread started..")
    #     self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     port = 9999
    #     self.ls.bind(('', port))
    #     print("Server listening on port %s" % port)
    #     self.ls.listen(1)
    #     self.ls.settimeout(15)
    #     while self.running != 0:
    #         if self.conn is None:
    #             try:
    #                 (self.conn, self.addr) = self.ls.accept()
    #                 print("client is at", self.addr[0], "on port", self.addr[1])
    #
    #             except socket.timeout as e:
    #                 print("Waiting for Connection...")
    #
    #             except Exception as e:
    #                 print("Connect exception: " + str(e))
    #
    #         if self.conn != None and self.admin.fromAdminGo:
    #             sleep(1)
    #             self.admin.fromAdminGo = 0
    #             print("connected to " + str(self.conn) + "," + str(self.addr))
    #             self.conn.settimeout(15)
    #             self.rc = ""
    #             connect_start = time()  # actually, I use this for a timeout timer
    #             if self.rc != "done":
    #                 self.rc = ''
    #                 try:
    #                     self.conn.send(b"scan")
    #                     print("sent")
    #                     self.rc = self.conn.recv(20).decode('utf-8')
    #                     print("rcvd")
    #                     self.admin.rfid = self.rc
    #                     self.admin.updateEdit()
    #                 except Exception as e:
    #                     # we can wait on the line if desired
    #                     print("socket error: " + repr(e))
    #
    #                 if len(self.rc):
    #                     print("got data", self.rc)
    #                     self.gotData = True
    #                     connect_start = time()  # reset timeout time
    #                 elif (self.running == 0) or (time() - connect_start > 30):
    #                     print("Tired of waiting on connection!")
    #                     self.rc = "done"
    #
    #             # print("closing connection")
    #             # self.conn.close()
    #             # self.conn = None
    #             # print("connection closed.")
    #
    #     print("closing listener...")
    #     # self running became 0
    #     self.ls.close()

    # def startc(self):
    #     """
    #     Startet den Server Thread.
    #
    #     :return:
    #     """
    #     if self.running == 0:
    #         print("Starting thread")
    #         self.running = 1
    #         self.thread = Thread(target=self.client_thread)
    #         self.thread.start()
    #     else:
    #         print("thread already started.")
    #
    # def stopc(self):
    #     """
    #     Stoppt den Server Thread.
    #
    #     :return:
    #     """
    #     if self.running:
    #         print("stopping thread...")
    #         self.running = 0
    #         self.thread.join()
    #     else:
    #         print("thread not running")


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
        print(option)
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


class ErrorMonitor(QObject):
    error_signal = QtCore.pyqtSignal(int)

    @QtCore.pyqtSlot()
    def monitor_errors(self):
        while True:
            sleep(1)
            if gpiocontrol.readInput(23):
                print("errordetected")
                #self.error_signal.emit(4)
            elif gpiocontrol.readInput(6):
                print("errordetected")
                #self.error_signal.emit(5)


class client():

    def __init__(self):
        print("Trying to connect")
        TCP_IP = '192.168.2.41' # IP RasPi
        TCP_PORT = 9999
        self.data = 0
        self.BUFF = 10

        self.s = socket.socket()
        self.s.connect((TCP_IP, TCP_PORT))

    def get_data(self):
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
        self.s.send(data.encode())
        print("data sent")


def main():
    import sys
    app = QApplication(sys.argv)
    # Erstellt Objekt win mit UI_MainWindow() und erstellt im Anschluss das User Interface und zeigt es an.
    win = MainWindow()
#    win.errorstart()
#    win.startc()
    # Funktion SetupUI wird ausgeführt, und somit das Fenster initialisiert.
    win.setupUi()
    # Funktion show zeigt das vorher initialisierte Fenster an.
    win.show()






    sys.exit(app.exec())


if __name__ == "__main__":
    main()
