import configparser as cp
import math
import os
from threading import Thread
from time import *

import cv2
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget

import PoseModule as pm
import motor
import settings
import mainwindow


class Ui_Dialog(QWidget):
    """
    Dient zum anzeigen der Maske zum bestätigen oder Abbrechen der gewählten Optionen und bereitet die Kameraauswertung
    vor. Sobald der Benutzer bestätigt, wird ein 10s Countdown Timer angezeigt. Dieser wird auf einem extra Thread aus-
    geführt um Performance zu sparen. Der Timer fängt an zu zählen, wenn der Benutzer sich vor der Kamera aufgestellt
    hat und diese ihn erkannt hat. Sobald der Countdown null erreicht hat, startet ein variabler Minuten Timer. Von da
    an werden die Ausführungen der Übungen des Benutzers ausgewertet und überwacht. Er muss nun über den gesamten Zeitraum
    die Übung ausführen. Am ende des Timers erfährt er, ob er erfolgreich war oder nicht.
    Nach der Übungsauswertung wird der Geldwert des RFID-Codes angepasst und die vorher gewählte Süßigkeit ausgegeben.
    Anschließend befindet sich der Automat wieder in Ausgangsstellung.

    """
    fileGIF = ''

    def __init__(self, parent=None):
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
        self.cdtime = 5000  # Countdown-Timer in ms           # ToDo: Zeit auf 10000 ändern, nur aufgrund Debugging
        self.txt = "Wie auf dem Bild gezeigt vor der Kamera aufstellen!"
        self.notSucceededbit = False

    def setupUI(self, w, h, file2, fileGIF, ID, id_sweets, unit_time, rfid, ):
        """
        Funktion zum initialisieren und erstellen des Fensters der Süßigkeitenauswahl. Aufruf und Init aller
        Labels und Elemente die anzuzeigen sind.

        :param w: (int) : Weite des Fensters
        :param h: (int) : Höhe des Fensters
        :return:
        """
        # Initialisiert sämtliche Variablen des Konstruktors
        self.fileGIF = fileGIF
        self.fileText2 = open(file2, encoding='utf-8', mode="r").read()
        self.trainingID = ID
        self.id_sweets = id_sweets
        self.unit_time = unit_time  # Zeit in s für Übung
        self.rfid = rfid
        self.cap = cv2.VideoCapture(settings.CamID, cv2.CAP_DSHOW)

        self.setObjectName("Dialog")
        self.setWindowTitle("Help Automat")
        self.resize(w, h)
        self.move(1920 / 2 - 1600 / 2, 1080 / 2 - 900 / 2)
        self.setStyleSheet("background-color: rgb(49, 49, 51)")  # 49 49 51
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
        if self.trainingID == 1:
            self.labelJPG("misc/Frontansicht_mspaint.jpg", (1600/2) - (285/2), (750/2) - (719/2), 285, 719)
        elif self.trainingID == 2:
            self.labelJPG("misc/Liegestütz.jpg", (1600/2) - (654/2), (750/2) - (386/2), 654, 386)
        elif self.trainingID == 3 or self.trainingID == 4:
            self.labelJPG("misc/Seitenansicht.jpg", (1600/2) - (285/2), (750/2) - (731/2), 285, 731)


    def labelJPG(self, jpg, x, y, w, h):
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
        self.label_jpg.setGeometry(QtCore.QRect(x, y, w, h))  # x y width height
        self.label_jpg.setPixmap(QtGui.QPixmap(os.path.join(path, jpg)))
        self.label_jpg.setObjectName("label_jpg")

    def buttonOK(self):
        """
        Initialisiert und erstellt den Button OK.

        :return:
        """
        self.button_ok = QPushButton(self)
        self.button_ok.setText("Bestätigen")
        self.button_ok.clicked.connect(self.ok)
        self.button_ok.setGeometry(600, 800, 150, 75)  # x y
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
        # Wenn der Button betätigt wird, schließt sich das Fenster.
        self.button_back.clicked.connect(lambda: self.close())
        # Wenn der Button betätigt wird, wird ebenfalls die Methode "back" ausgeführt.
        self.button_back.clicked.connect(self.back)
        self.button_back.setGeometry(850, 800, 150, 75)  # x y
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
        self.label_txt.setGeometry(QtCore.QRect(80, 10, 400, 440))  # x, y, width, height
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
        #        self.label_Time.setGeometry(QtCore.QRect(650, 400, 300, 120))
        self.label_Time.setObjectName("label_Time")
        self.label_Time.setStyleSheet("color: rgba(255, 0, 0, 1); font: bold; font-size: 200px")
        self.label_Time.setText(str("05.00") + " s")  # ToDo: Zeit auf 10s ändern, nur aufgrund Debugging
        self.label_Time.adjustSize()
        # Die Position des Timer-Labels wird anhand der unten stehenden Formel berechnet, damit
        # diese immer mittig im Bild zu sehen ist.
        x = self.label_Time.width()
        y = self.label_Time.height()
        self.label_Time.move(1600 / 2 - x / 2, 900 / 2 - y / 2)
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
        settings.isClicked = False  # Rücksetzen des Speichers für die Warnung "... zu niedrig"
        self.label_txt.hide()
        self.button_ok.hide()
        self.button_back.hide()
        self.label_jpg.hide()

        self.label_Time.show()
        # Init for Detection
        detector = pm.poseDetector()
        flipflopflag = False
        # UnitDone überwacht, ob die Übung erfolgreich ausgeführt wurde.
        self.unitDone = False  # New
        # UnitCounter ist der Ist-Wert der ausgeführten Übungen.
        self.unitCounter = 0  # New
        while not self.notSucceededbit:
            success, img = self.cap.read()
            img = detector.findPose(img, draw=True)
            lmList = detector.findPosition(img, draw=True)
            # Überwachung ob der Benutzer sich ordnungsgemäß vor der Kamera aufgestellt hat.
            if len(lmList) != 0:
                # Es werden die Knöchel überwacht, ob diese zu mind. 80% sichtbar sind.
                if lmList[27][3] > 90 or lmList[28][3] > 90:
                    if not self.countrunning:
                        # Prozess des Countdown Timers wird gestartet.
                        self.countstart()

            # ___________________ Übung 1: Hampelmann ___________________
            if len(lmList) != 0 and self.timerrunning:
                # TrainingID = 1 = Hampelmann
                if self.trainingID == 1:
                    self.unitCheck = round(settings.JJReps * 2)
                    if self.unitCounter < round(settings.JJReps * 2):
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
                        break


                # ___________________ Übung 2: Liegestütz ___________________
                # TrainingID = 2 = Liegestütz
                elif self.trainingID == 2:
                    self.unitCheck = round(settings.PUReps * 2)
                    if self.unitCounter < settings.PUReps*2:
                        # Bereiche der Ruheposition
                        if (lmList[31][2] - lmList[11][2] >= 75) and (lmList[32][2] - lmList[12][2] >= 75) \
                                and not flipflopflag:
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if (lmList[31][2] - lmList[11][2] <= 75) and (lmList[32][2] - lmList[12][2] <= 75) \
                                and flipflopflag:
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True
                        break


                # ___________________ Übung 3: Kniebeugen ___________________
                # TrainingID = 3 = Kniebeugen
                elif self.trainingID == 3:
                    self.unitCheck = round(settings.SQReps * 2)
                    if self.unitCounter < settings.SQReps * 2:
                        # Bereiche der Ruheposition
                        if (lmList[26][2] - lmList[24][2] >= 40) and (lmList[25][2] - lmList[23][2] >= 40) \
                                and not flipflopflag:
                            flipflopflag = True
                            self.unitCounter += 1

                        # Bereiche der Arbeitsposition
                        if (lmList[26][2] - lmList[24][2] <= 40) and (lmList[25][2] - lmList[23][2] <= 40) \
                                and flipflopflag:
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True
                        break


                # ___________________ Übung 4: Ausfallschritt ___________________
                # TrainingID = 4 = Ausfallschritt
                elif self.trainingID == 4:
                    leftAngle = precalcs(28, 26, 24, lmList)
                    rightAngle = precalcs(27, 25, 23, lmList)
                    self.unitCheck = round(settings.LGReps * 2)
                    if self.unitCounter < settings.LGReps * 2:
                        # Bereiche der Ruheposition
                        if leftAngle >= 130 and rightAngle >= 130 \
                                and not flipflopflag:
                            flipflopflag = True
                            self.unitCounter += 1
                            print("counted")
# lmList[26][2] - lmList[24][2] >= 40) and (lmList[25][2] - lmList[23][2] >= 40

#lmList[26][1] >= lmList[12][1]) and (lmList[25][1] >= lmList[11][1]) \
                                # and (lmList[14][2] >= lmList[12][2]) and (lmList[13][2] >= lmList[11][2]
                        # Bereiche der Arbeitsposition
                        if leftAngle <= 80 and rightAngle <= 80 \
                                and flipflopflag:
                            flipflopflag = False
                            self.unitCounter += 1
                    else:
                        self.unitDone = True
                        break


            #            cv2.putText(img, str(int(self.unitCounter)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            #cv2.imshow("Image", img)  # ToDo: Zeit ändern + Image auskommentieren
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
                self.cdtime -= 200
                sleep(0.2)
                self.label_Time.setText(str(self.cdtime / 1000) + " s")
                self.label_Time.adjustSize()
                x = self.label_Time.width()
                y = self.label_Time.height()
                self.label_Time.move(1600 / 2 - x / 2, 900 / 2 - y / 2)
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
                # Label resize da Minuten Timer relativ groß
                self.label_Time.setGeometry(
                    QtCore.QRect(650, 400, 250, 80))
                # Sekundenweise decrement
                self.unit_time -= 1
                # Sekunden-Wert in Minuten wandeln
                num = self.unit_time / 60
                # Dezimalzahl trennen in Int + Decimal
                separate = math.modf(num)
                # Timer String zusammenbauen, zfill um "0" vor der Zahl zu setzen
                new_string = str(int(separate[1])).zfill(2) + ":" + str(round(separate[0] * 60)).zfill(
                    2) + " min"
                self.label_Time.setText(new_string)
                self.label_Time.adjustSize()
                x = self.label_Time.width()
                y = self.label_Time.height()
                self.label_Time.move(1600 / 2 - x / 2, 900 / 2 - y / 2)
            else:
                if self.unitDone:
                    print("succeded")
                    self.Succeeded(self.id_sweets)
                    break
                else:
                    self.notSucceededbit = True
                    self.notSucceeded()
                    break

    def back(self):  # ToDo: Funktion überprüfen, ob überhaupt nötig
        settings.isClicked = False  # Rücksetzen des Speichers für die Warnung ".. zu niedrig"
        print("Button Pressed back")
        self.cap.release()

    def notSucceeded(self):
        """
        Diese Funktion wird aufgerufen wenn der Benutzer nicht erfolgreich in seiner Aufgabe war.
        Hier werden dann die Timer Label angepasst und ein Text ausgegeben, der den Benutzer darauf hinweist, dass er
        nicht erfolgreich war, und ihm ebenfalls sagt warum.
        Im Anschluss wird der 4. Motor mit dem Gesunden Nahrungsmittel angesteuert.

        :return:
        """
        self.decrementMoney()
        self.decrementCounterPunishment()
        print("noSuccess")
        self.label_Time.setStyleSheet("color: red; font-size: 54px; font: bold")
        self.label_Time.setText("Es scheint als wäre das Ziel nicht erreicht!\n"
                                "Das Ziel wären gewesen: " + str(self.unitCheck) + "\n"
                                                                                   "Davon wurden erreicht: " + str(
            self.unitCounter))  # ToDo: Evtl /2 wegen Anzahl
        self.label_Time.adjustSize()
        self.label_Time.move(300, 400)
        self.label_Time.show()
        motor.start(4)  # Motor 4 für Gesunde Mahlzeit
        settings.errorFour = False
        settings.warningFour = False
        self.cap.release()
        self.deleteLater()
        return

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
        self.label_Time.setText("Das Ziel wurde erreicht!")
        self.label_Time.adjustSize()
        self.label_Time.move(300, 400)
        self.label_Time.show()
        motor.start(id_sweets)  # id_sweets
        settings.errorFour = False
        settings.warningFour = False
        self.cap.release()
        self.deleteLater()
        return

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
        value = float(value)
        print(value)
        value -= 0.5
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
            # Globale Zähler Variable
            settings.actValueOne -= 1
            config["DEFAULT"]["SweetCountOne"] = str(counter)
            config.write(cfgfile)
            cfgfile.close()
            del config
        elif self.id_sweets == 2:
            counter = config["DEFAULT"]["SweetCountTwo"]
            counter = int(counter)
            counter -= 1
            settings.actValueTwo -= 1
            config["DEFAULT"]["SweetCountTwo"] = str(counter)
            config.write(cfgfile)
            cfgfile.close()
#            del config
        elif self.id_sweets == 3:
            counter = config["DEFAULT"]["SweetCountThree"]
            counter = int(counter)
            counter -= 1
            settings.actValueThree -= 1
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
        settings.actValueFour -= 1
        if settings.actValueFour <= 5:
            settings.warningFour = True
        elif settings.actValueFour == 0:
            settings.errorFour = True
        cfgfile = open("config.ini", "w")
        config["DEFAULT"]["SweetCountFour"] = str(counter)
        config.write(cfgfile)
        cfgfile.close()
        del config

    def countstart(self):
        """
        Dient zum starten des CountdownTimer Threads(Prozesses)

        :return:
        """
        if self.countrunning == 0:
            self.countrunning = True
            self.threadcount = Thread(target=self.countdown)
            self.threadcount.daemon = True
            self.threadcount.start()

    def countstop(self):
        """
        Dient zum stoppen des CountdownTimer Threads(Prozesses)

        :return:
        """
        if self.countrunning:
            self.countrunning = 0
            self.threadcount.join()

    def timerstart(self):
        """
        Dient zum starten des ÜbungsTimer Threads(Prozesses)

        :return:
        """
        if self.timerrunning == 0:
            self.timerrunning = True
            self.threadtimer = Thread(target=self.timer)
            self.threadtimer.daemon = True
            self.threadtimer.start()

    def timerstop(self):
        """
        Dient zum stoppen des ÜbungsTimer Threads(Prozesses)

        :return:
        """
        if self.timerrunning:
            self.timerrunning = 0
            self.threadtimer.join()

def cosine_law(a, b, c):
    """
    Dient zu Berechnung des Winkels über den Kosinussatz.

    :param a: (int) Seite a
    :param b: (int) Seite b
    :param c: (int) Seite c
    :return: (int) Winkel in DEGREE
    """
    return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

def precalcs(lm1, lm2, lm3, lmList):
    """
    Dient zur Berechnung der Längen aller Seiten eines Dreiecks anhand der Landmarks der Beine.

    :param lm1: (int) ID des Knöchels
    :param lm2: (int) ID des Knies
    :param lm3: (int) ID des Beckenknochens
    :param lmList: (list) Liste aller Landmarks
    :return: (int) Winkel in DEGREE
    """
    foot_x, foot_y = lmList[lm1][1], lmList[lm1][2]
    knee_x, knee_y = lmList[lm2][1], lmList[lm2][2]
    waist_x, waist_y = lmList[lm3][1], lmList[lm3][2]

    a_shin = foot_x - knee_x
    b_shin = foot_y - knee_y
    a_shin = abs(a_shin)
    b_shin = abs(b_shin)

    shinlen = math.hypot(a_shin, b_shin)

    a_thigh = knee_x - waist_x
    b_thigh = knee_y - waist_y
    a_thigh = abs(a_thigh)
    b_thigh = abs(b_thigh)

    thighlen = math.hypot(a_thigh, b_thigh)

    a_leg = foot_x - waist_x
    b_leg = foot_y - waist_y
    a_leg = abs(a_leg)
    b_leg = abs(b_leg)

    leglen = math.hypot(a_leg, b_leg)

    return cosine_law(shinlen, thighlen, leglen)