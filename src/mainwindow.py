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
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from adminwindow import *
import os

from src import gpioread
from src.errorwindow import errorwindow
from unitselectwindow import UnitSelectWindow
import socket
from threading import Thread
from time import *

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
        self.addr = None
        self.conn = None
        self.startScan = 0
        self.gotData = False
        self.error = errorwindow()
        self.errorTime = QTimer()
        self.errorTime.timeout.connect(self.errorHandler)
#        self.errorTime.start(1000)

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
            self.startScan = 1 # Eigene Variable zum merken des Starts
            self.admin.fromAdminGo = 1  # Globale Variable zum Scanauftrag schicken
            while self.startScan != 0: # Wenn StartScan != 0 dann Schleife laufen lassen
                if self.gotData:
                    if getConfigCodes(self.admin.rfid) and int(getConfigValue(self.admin.rfid)) >= -5:
                        print(self.admin.rfid)
                        self.DialogWindow(1, 1920, 1080)
                        self.startScan = 0
                        self.gotData = False
                        break
                    else:
                        self.error.setupUI(1)
                        break
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
            self.admin.setupUI()
            self.admin.show()

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

    def socket_thread(self):
        print("thread started..")
        self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 9999
        self.ls.bind(('', port))
        print("Server listening on port %s" % port)
        self.ls.listen(2)
        self.ls.settimeout(15)
        while self.running != 0:
            if self.conn is None:
                try:
                    (self.conn, self.addr) = self.ls.accept()
                    print("client is at", self.addr[0], "on port", self.addr[1])

                except socket.timeout as e:
                    print("Waiting for Connection...")

                except Exception as e:
                    print("Connect exception: " + str(e))

            if self.conn != None and self.admin.fromAdminGo:
                self.admin.fromAdminGo = 0
                print("connected to " + str(self.conn) + "," + str(self.addr))
                self.conn.settimeout(15)
                self.rc = ""
                connect_start = time()  # actually, I use this for a timeout timer
                if self.rc != "done":
                    self.rc = ''
                    try:
                        self.conn.send(b"scan")
                        print("sent")
                        self.rc = self.conn.recv(1000).decode('utf-8')
                        print("rcvd")
                        self.admin.rfid = self.rc
                        self.admin.updateEdit()
                    except Exception as e:
                        # we can wait on the line if desired
                        print("socket error: " + repr(e))

                    if len(self.rc):
                        print("got data", self.rc)
                        self.gotData = True
                        connect_start = time()  # reset timeout time
                    elif (self.running == 0) or (time() - connect_start > 30):
                        print("Tired of waiting on connection!")
                        self.rc = "done"

                # print("closing connection")
                # self.conn.close()
                # self.conn = None
                # print("connection closed.")

        print("closing listener...")
        # self running became 0
        self.ls.close()

    def startc(self):
        if self.running == 0:
            print("Starting thread")
            self.running = 1
            self.thread = Thread(target=self.socket_thread)
            self.thread.start()
        else:
            print("thread already started.")

    def stopc(self):
        if self.running:
            print("stopping thread...")
            self.running = 0
            self.thread.join()
        else:
            print("thread not running")

    def errorHandler(self):
        if gpioread.readInput(6):
            self.error.setupUI(5, 0)
        elif gpioread.readInput(23):
            self.error.setupUI(4, 0)


def getConfigCodes(searchstring):
    config = cp.ConfigParser()
    config.read("config.ini")
    for option in config.options("RFID"):
        if option == searchstring:
            del config
            return True

def getConfigValue(searchstring):
    config = cp.ConfigParser()
    config.read("config.ini")
    ret = config["RFID"][searchstring]
    del config
    return ret

def main():
    import sys
    from time import sleep
    app = QApplication(sys.argv)
    # Erstellt Objekt win mit UI_MainWindow() und erstellt im Anschluss das User Interface und zeigt es an.
    win = MainWindow()
    win.startc()
    # Funktion SetupUI wird ausgeführt, und somit das Fenster initialisiert.
    win.setupUi()
    # Funktion show zeigt das vorher initialisierte Fenster an.
    win.show()






    sys.exit(app.exec())

'''
class server:

    def __init__(self):
        self.data = 0
        # Server erstellen
        TCP_IP = socket.gethostname()
        TCP_PORT = 5005
        print("Server")

        self.BUFF = 50

        s = socket.socket()
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
        while True:
            self.conn, self.addr = s.accept()
            print_lock.acquire()
            print('Conn', self.addr)
            print(self.conn)
            start_new_thread(threaded,(self.conn,))
            print("asdf")
        s.close()


    def get_data(self):
        self.data = self.conn.recv(self.BUFF)
        print(self.data)
        return self.data.decode('utf-8')

    def send_data(self, data):
        print("data sent")
        self.conn.send(data)


print_lock = threading.Lock()

def threaded(c):
    while True:
        #data recv
        data = c.recv(50)
        print("asdddd")
        if not data:
            print("Bye")

            print_lock.release()
            break
        c.send(data)
    c.close()


'''

if __name__ == "__main__":
    main()
