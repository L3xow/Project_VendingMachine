import math
from threading import Thread

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
import PoseModule as pm
import configparser as cp
import cv2
from time import *


# ToDo: Motor.py muss noch komplett gecodet werden, brauche aber erst einen funktionierenden RasPi

# ToDo: Designfragen klären, Farben, usw.
from src.errorwindow import errorwindow
from src.motor import start


class QTCore:
    pass





class Ui_Dialog(QWidget):
    fileGIF = ''

    def __init__(self, file2, fileGIF, ID, id_sweets, unit_time, rfid, parent=None):
        """
        Konstruktor für das DialogFenster das ebenfalls die Kameraauswertung vornimmt.

        :param file2: (path) : Ist die Einverständnisfrage an den Benutzer, ob er alles verstanden hat.
        :param fileGIF: (path) : Ist der Pfad der Animationen die nochmals in der Mitte des Fensters angezeigt werden.
        :param ID: (int) : ID der gewählten Übung ( 1-4 ) um diese nochmals in der Mitte anzuzeigen.
        :param id_sweets: (int) : ID der gewählten Süßigkeit in der ersten Maske, um damit die Motoren anzusteuern.
        :param unit_time: (int) : Vorgegebene Zeit in Minuten, die der Benutzer hat um das Ziel zu erreichen.
        :param rfid: (string) : RFID Code zum abziehen des Geldwertes.
        :param parent:
        """
        super().__init__(parent)
        self.label_GIF = QLabel
        self.label_txt = QLabel
        self.label_Time = QLabel
        self.unitCheck = 0
        self.countrunning = 0
        self.timerrunning = 0
        self.cap = cv2.VideoCapture(0)
        self.cdtime = 10000  # Countdown-Timer in ms           # ToDo: Zeit auf 10000 ändern, nur aufgrund Debugging

        # Initialisiert sämtliche Variablen des Konstruktors
        self.fileGIF = fileGIF
        self.fileText2 = open(file2, encoding='utf-8', mode="r").read()
        self.trainingID = ID
        self.id_sweets = id_sweets
        self.unit_time = unit_time  # Zeit in s für Übung
        self.rfid = rfid

        # Initialisiert die Timer für die Zeitvorgabe an den Benutzer
        # MyCount ist in dem Fall der Countdown von 10s
        # self.myCount = QTimer()
        # self.myCount.timeout.connect(self.countdown)
        # MyTime ist die Zeit für die Übung
        # self.myTime = QTimer()
        # self.myTime.timeout.connect(self.timer)

    def setupUI(self, w, h):
        """
        Funktion zum initialisieren und erstellen des Fensters der Süßigkeitenauswahl. Aufruf und Init aller
        Labels und Elemente die anzuzeigen sind.

        :param w: (int) : Weite des Fensters
        :param h: (int) : Höhe des Fensters
        :return:
        """
        self.setObjectName("Dialog")
        self.setWindowTitle("Help Automat")
        self.resize(w, h)
        self.setStyleSheet("background-color: rgb(0, 0, 0)")  # 49 49 51
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # Funktionsaufruf um den Button OK zu erstellen
        self.buttonOK()
        # Funktionsaufruf um den Button Back zu erstellen
        self.buttonBack()
        # Funktionsaufruf des Text Labels
        self.labelTXT(self.fileText2)
        # Funktionsaufruf zum erstellen der Timer Label
        self.labelTimer()
        # Funktionsaufruf zum erstellen des GIFs/der Animation in der mitte des Fensters
        self.labelGIF()
        print(self.id_sweets, self.trainingID)
        print(self.rfid)

    def labelGIF(self):
        """
        Initialisiert und erstellt das Animierte Label.

        :return:
        """
        self.label_GIF = QLabel("label_GIF", self)
        self.label_GIF.setGeometry(QtCore.QRect(600, 210, 300, 300))  # x y width height
        self.label_GIF.setText("")
        self.movie = QMovie(self.fileGIF)
        self.label_GIF.setMovie(self.movie)
        self.movie.start()

    def buttonOK(self):
        """
        Initialisiert und erstellt den Button OK.

        :return:
        """
        self.button_ok = QPushButton(self)
        self.button_ok.setText("Bestätigen")
        self.button_ok.clicked.connect(self.ok)
        self.button_ok.setGeometry(600, 600, 150, 75)  # x y
        self.button_ok.setStyleSheet(
            "color: rgba(255,255,255,1);  font: bold;  border-style: solid;  border-width: 1px;  "
            "border-color: grey; background-color: rgb(54, 73, 78); font-size: 20px; ")

    def buttonBack(self):
        """
        Initialisiert und erstellt den Button Back.

        :return:
        """
        self.button_back = QPushButton(self)
        self.button_back.setText("Abbruch")
        self.button_back.clicked.connect(lambda: self.close())
        self.button_back.clicked.connect(self.back)
        self.button_back.setGeometry(800, 600, 150, 75)  # x y
        self.button_back.setStyleSheet(
            "color: rgba(255,255,255,1);  font: bold;  border-style: solid;  border-width: 1px;  "
            "border-color: grey; background-color: rgb(54, 73, 78); font-size: 20px; ")

    def labelTXT(self, fileText1):
        """
        Initialisiert und erstellt das Text Label für die Einverständniserklärung.

        :param fileText1: (str) : Text, ausgelesen aus der von oben übergebenen File.
        :return:
        """
        self.label_txt = QtWidgets.QLabel(self)
        self.label_txt.setGeometry(QtCore.QRect(100, 10, 400, 440))  # x, y, width, height
        self.label_txt.setWordWrap(True)
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: rgba(255, 255, 255, 1); font: bold; font-size: 32px")
        self.label_txt.setText(str(fileText1))

    def labelTimer(self):
        """
        Initialisiert und erstellt das Timer Label für den Countdown und den Übungstimer

        :return:
        """
        self.label_Time = QLabel("label_Time", self)
        self.label_Time.move(550, 400)
        #        self.label_Time.setGeometry(QtCore.QRect(650, 400, 300, 120))
        self.label_Time.setObjectName("label_Time")
        self.label_Time.setStyleSheet("color: rgba(255, 0, 0, 1); font: bold; font-size: 200px")
        self.label_Time.setText(str("10.00") + " s")  # ToDo: Zeit auf 10s ändern, nur aufgrund Debugging
        self.label_Time.adjustSize()
        self.label_Time.hide()

    def ok(self):
        """
        Diese Funktion versteckt und zeigt die benötigten Label für die Kameraauswertungs-Maske.
        Hier findet ebenfalls die Kameraauswertung statt. lmList ( Array ) enthält alle LandmarkIDs, deren x, y, und z
        Koordinaten in einem 3 dimensionalen Array.
        Hier werden lediglich die IDs und die Positionen mit programmierten Bereichen verglichen und ein Zähler inkrementiert.

        :return:
        """

        # Sämtliche Anzeigen des Fensters verstecken
        self.label_txt.hide()
        self.label_GIF.setVisible(False)
        self.button_ok.hide()
        self.button_back.hide()

        self.label_Time.show()
        # Init for Detection
        detector = pm.poseDetector()
        flipflopflag = False
        self.unitDone = False  # New
        self.unitCounter = 0  # New
        self.unitCheck = 0  # New
        while True:
            success, img = self.cap.read()
            img = detector.findPose(img, draw=True)
            lmList = detector.findPosition(img, draw=True)

            if len(lmList) != 0:
                if lmList[27][3] > 80 and lmList[28][3] > 80:
                    print("started")
                    if not self.countrunning:
                        print("asdf")
                        self.countstart()
            # Array lmList enthält die 32 Landmarks der PoseDetection.
            # Element 0 enthält die ID
            # Element 1 enthält die X Koordinate des Landmarks
            # Element 2 enthält die Y Koordinate des Landmarks
            # Element 3 enthält die Visibility des Landmarks
            if len(lmList) != 0:
                if self.trainingID == 1:  # Übung 1
                    self.unitCheck = 10   # Anzahl an ausführungen die gewertet werden
                    if self.unitCounter < self.unitCheck:
                        # Bereiche der Ruheposition
                        if ((lmList[27][1] - lmList[28][1]) <= 100) and (lmList[12][2] < lmList[14][2]) \
                                and (lmList[11][2] < lmList[13][2]) and not flipflopflag:
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if ((lmList[27][1] - lmList[28][1]) >= 100) and (lmList[12][2] > lmList[14][2]) \
                                and (lmList[11][2] > lmList[13][2]) and flipflopflag:
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True

                # Hier beginnt dann TrainingsID 2 Liegestützen
                elif self.trainingID == 2:  # Übung 2
                    self.unitCheck = 10
                    # Anzahl an ausführungen die gewertet werden
                    if self.unitCounter < self.unitCheck:  # Anzahl der Wiederholungen in der Übung
                        # Bereiche der Ruheposition
                        if (lmList[31][2] - lmList[11][2] >= 75) and (lmList[32][2] - lmList[12][2] >= 75) \
                                and not flipflopflag and self.myTime.isActive():
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if (lmList[31][2] - lmList[11][2] <= 75) and (lmList[32][2] - lmList[12][2] <= 75) \
                                and flipflopflag and self.myTime.isActive():  # Abstand zwischen den Beinen, flipflopflag = Verriegelung damit nicht ständig hochgezählt wird
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True

                # Hier beginnt dann TrainingsID 3 Squats
                elif self.trainingID == 3:
                    self.unitCheck = 40
                    # Anzahl an ausführungen die gewertet werden
                    if self.unitCounter < self.unitCheck:  # Anzahl der Wiederholungen in der Übung
                        # Bereiche der Ruheposition
                        if (lmList[26][2] - lmList[24][2] >= 40) and (lmList[25][2] - lmList[23][2] >= 40) \
                                and not flipflopflag and self.myTime.isActive():
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if (lmList[26][2] - lmList[24][2] <= 40) and (lmList[25][2] - lmList[23][2] <= 40) \
                                and flipflopflag and self.myTime.isActive():
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True

                # Hier beginnt dann TrainingsID 4 Ausfallschritte
                elif self.trainingID == 4:
                    self.unitCheck = 40
                    # Anzahl an ausführungen die gewertet werden
                    if self.unitCounter < self.unitCheck:  # Anzahl der Wiederholungen in der Übung
                        # Bereiche der Ruheposition
                        if (lmList[26][2] - lmList[24][2] >= 40) and (lmList[25][2] - lmList[23][2] >= 40) \
                                and not flipflopflag and self.myTime.isActive():
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if (lmList[26][1] >= lmList[12][1]) and (lmList[25][1] >= lmList[11][1]) \
                                and (lmList[14][2] >= lmList[12][2]) and (lmList[13][2] >= lmList[11][2]) \
                                and flipflopflag and self.myTime.isActive():
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True

#            cv2.putText(img, str(int(self.unitCounter)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)  # ToDo: Zeit ändern + Image auskommentieren
            cv2.waitKey(10)

    def countdown(self):
        """
        Wird aufgerufen durch den erstellen Countdown Timer MyCount. Hier wird lediglich der Countdown auf 0 gezählt
        und ständig im 100ms Takt im Fenster aktualisiert und angezeigt.

        :return:
        """
        print("Countdown started")
        while self.countrunning != 0:
            if self.cdtime != 0:
                self.cdtime -= 500
                sleep(0.5)
                print(self.cdtime)
                self.label_Time.setText(str(self.cdtime / 1000) + " s")
                if self.cdtime == 0:  # wenn Countdown fertig, dann neuen Timer starten für Übungszeit
                    self.timerstart()
                    break


    def timer(self):
        """
        Wird aufgerufen durch den erstellten Übungstimer MyTime. Hier wird ein Minutentimer erstellt und
        so geformt, dass dieser richtig im Label Timer angezeigt werden kann.
        Wenn dieser Timer abgelaufen ist, und je nachdem die Übungsauswertung ausfiel, werden verschiedene
        Funktionen zum weiteren Ablauf aufgerufen.

        :return:
        """
        print("Timer started")
        while self.timerrunning != 0:
            if self.cdtime == 0 and self.unit_time != 0:
                sleep(1)
                self.label_Time.setGeometry(QtCore.QRect(650, 400, 250, 80))  # Label resize da Minuten Timer relativ groß
                self.unit_time -= 1  # Sekundenweise decrement
                num = self.unit_time / 60  # 120s in Minuten wandeln
                separate = math.modf(num)  # Dezimalzahl trennen in Int + Decimal
                new_string = str(int(separate[1])).zfill(2) + ":" + str(round(separate[0] * 60)).zfill(
                    2) + " min"  # Timer String zusammenbauen, zfill um "0" vor der Zahl zu setzen
                self.label_Time.setText(new_string)
                self.label_Time.adjustSize()
            else:
                print("timer stop")
                print(self.unitDone)
                if self.unitDone:
                    print("succeded")
                    self.Succeeded(self.id_sweets)
                    break
                else:
                    print("not succeeded")
                    self.notSucceeded()
                    break

    def back(self):  # ToDo: Funktion überprüfen, ob überhaupt nötig
        print("Button Pressed back")

    def notSucceeded(self):
        """
        Diese Funktion wird aufgerufen wenn der Benutzer nicht erfolgreich in seiner Aufgabe war.
        Hier werden dann die Timer Label angepasst und ein Text ausgegeben, der den Benutzer darauf hinweist, dass er
        nicht erfolgreich war, und ihm ebenfalls sagt warum.
        Im Anschluss wird der 4. Motor mit dem Gesunden Nahrungsmittel angesteuert.

        :return:
        """
        self.decrementMoney()
        self.decrementCounterPunishment
        self.myTime.stop()
        print("noSuccess")
        self.label_Time.setStyleSheet("color: red; font-size: 54px; font: bold")
        self.label_Time.setText("Es scheint als wäre das Ziel nicht erreicht!\n"
                                "Das Ziel wären gewesen: " + str(self.unitCheck) + "\n"
                                                                                   "Davon wurden erreicht: " + str(
            self.unitCounter))  # ToDo: Evtl /2 wegen Anzahl
        self.label_Time.adjustSize()
        self.label_Time.move(300, 400)
        self.label_Time.show()
        start(4)  # Motor 4 für Gesunde Mahlzeit
        self.close()

    def Succeeded(self, id_sweets):
        """
        Diese Funktion wird aufgerufen, wenn der Benutzer erfolgreich bei seiner Aufgabe war.
        Es wird der Text von Label Time angepasst zu einer vorprogrammierten Benachrichtigung und einem Glückwunsch.
        Anschließend wird der Motor mit der angegebenen ID angesteuert.

        :param id_sweets: (int) : Bezogen auf die vorher gewählte Süßigkeit.
        :return:
        """
        print("succeeded")
        self.decrementMoney()
        self.decrementCounterSweets()
        print("Success")
        self.label_Time.setStyleSheet("color: green; font-size: 88px; font: bold")
        self.label_Time.setText("Perfect you did it!")
        self.label_Time.adjustSize()
        self.label_Time.move(407, 400)
        self.label_Time.show()
        start(id_sweets)  # id_sweets
        self.close()

    def decrementMoney(self):
        """
        Funktion dient zum dekrementieren des oben übergebenen RFID Codes sobald eine Übung
        ausgeführt wurde. Config File wird geöffnet und der aktuelle Wert des RFID Codes aus-
        gelesen, anschließend zu Integer gewandelt und um mit -1 addiert. Danach wird der Wert
        des Codes in der File aktualisiert.

        :return:
        """
        config = cp.ConfigParser()
        config.read("config.ini")
        value = config["RFID"][self.rfid]
        value = int(value)
        print(value)
        value -= 1
        cfgfile = open("config.ini", "w")
        config["RFID"][self.rfid] = str(value)
        config.write(cfgfile)
        cfgfile.close()
        del config

    def decrementCounterSweets(self):
        """
        Funktion dient zum dekrementieren des Füllstandes der jeweiligen Süßigkeit.
        Zuerst wird der Ist- Wert ausgelesen, dann mit -1 addiert und anschließend wieder
        in der File aktualisiert.
        Dies geschieht für jede der drei Süßigkeiten

        :return:
        """
        config = cp.ConfigParser()
        config.read("config.ini")
        cfgfile = open("config.ini", "w")
        if self.id_sweets == 1:
            counter = config["DEFAULT"]["SweetCountOne"]
            counter = int(counter)
            counter -= 1
            if counter <= 5:
                err = errorwindow()
                err.setupUI(3, 1)
            config["DEFAULT"]["SweetCountOne"] = str(counter)
            config.write(cfgfile)
            cfgfile.close()
            del config
        elif self.id_sweets == 2:
            counter = config["DEFAULT"]["SweetCountTwo"]
            counter = int(counter)
            counter -= 1
            if counter <= 5:
                err = errorwindow()
                err.setupUI(3, 2)
            config["DEFAULT"]["SweetCountTwo"] = str(counter)
            config.write(cfgfile)
            cfgfile.close()
            del config
        elif self.id_sweets == 3:
            counter = config["DEFAULT"]["SweetCountThree"]
            counter = int(counter)
            counter -= 1
            if counter <= 5:
                err = errorwindow()
                err.setupUI(3, 3)
            config["DEFAULT"]["SweetCountThree"] = str(counter)
            config.write(cfgfile)
            cfgfile.close()
            del config

    def decrementCounterPunishment(self):
        """
        Funktion dient zum dekrementieren des Bestrafungs-Füllstandes. Ist-Wert wird
        ausgelesene, mit -1 addiert und anschließend in der Config File aktualisiert.

        :return:
        """
        config = cp.ConfigParser()
        config.read("config.ini")
        counter = config["DEFAULT"]["SweetCountFour"]
        counter = int(counter)
        counter -= 1
        if counter <= 5:
            err = errorwindow()
            err.setupUI(3, 4)
        cfgfile = open("config.ini", "w")
        config["DEFAULT"]["SweetCountFour"] = str(counter)
        config.write(cfgfile)
        cfgfile.close()
        del config

    def countstart(self):
        if self.countrunning == 0:
            self.countrunning = 1
            self.threadcount = Thread(target=self.countdown)
            self.threadcount.start()

    def countstop(self):
        if self.countrunning:
            self.countrunning = 0
            self.threadcount.join()

    def timerstart(self):
        if self.timerrunning == 0:
            self.timerrunning = 1
            self.threadtimer = Thread(target=self.timer)
            self.threadtimer.start()

    def timerstop(self):
        if self.timerrunning:
            self.timerrunning = 0
            self.threadtimer.join()

