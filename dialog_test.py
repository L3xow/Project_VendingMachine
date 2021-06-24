#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''


Pose IDs:

16 rechtes Handgelenk
15 linkes Handgelenk
28 rechter Knöchel
27 linker Knöchel           Visibility > 95 um Genauigkeit zu Gewährleisten

24 rechte Hüfte
23 linke Hüfte
0 Nase


'''

import math
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDialogButtonBox, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt, QTimer, QTextCodec
from PyQt5.QtGui import QMovie
import PoseModule as pm
import time
import cv2
import socket


# import motor


class QTCore:
    pass


class Ui_Dialog(QWidget):
    fileWin1 = ''
    fileWin2 = ''
    fileGIF = ''
    count = 5000  # Countdown-Timer in ms
    time = 120  # Dauer der Übung in s
    x = 1600  # Width Window
    y = 900  # Height Window

    def __init__(self, file1, file2, fileGIF, ID, id_sweets, parent=None):
        super().__init__(parent)

        # Init Variables
        self.fileWin1 = file1
        self.fileWin2 = file2
        self.fileGIF = fileGIF
        fileText1 = open(self.fileWin1, encoding='utf-8', mode="r").read()
        self.trainingID = ID
        self.id_sweets = id_sweets
        self.cap = cv2.VideoCapture(0)              # (0) = ID erste Webcam

        # Init Timer
        self.myCount = QTimer()
        self.myCount.timeout.connect(self.countdown)
        self.myTime = QTimer()
        self.myTime.timeout.connect(self.timer)

        # Init WindowConfig
        self.setObjectName("Dialog")
        self.setWindowTitle("Help Automat")
        self.resize(self.x, self.y)
        self.setStyleSheet("background-color: rgb(49, 49, 51)")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.buttonOK()
        self.buttonBack()
        self.labelTXT(fileText1)
        self.labelTimer()
        self.labelGIF()
        print(id_sweets)

    def labelGIF(self):
        self.label_GIF = QLabel("label_GIF", self)
        self.label_GIF.setGeometry(QtCore.QRect(600, 210, 300, 300))  # x y width height
        self.label_GIF.setText("")
        self.movie = QMovie(self.fileGIF)
        self.label_GIF.setMovie(self.movie)
        self.movie.start()

    def buttonOK(self):
        self.button_ok = QPushButton(self)
        self.button_ok.setText("Ok")
        self.button_ok.clicked.connect(self.ok)
        self.button_ok.setGeometry(600, 600, 150, 75)  # x y
        self.button_ok.setStyleSheet(
            "color: rgba(255,255,255,1);  font: bold;  border-style: solid;  border-width: 1px;  "
            "border-color: grey; background-color: rgb(54, 73, 78); font-size: 20px; ")

    def buttonBack(self):
        self.button_back = QPushButton(self)
        self.button_back.setText("Back")
        self.button_back.clicked.connect(lambda: self.close())
        self.button_back.clicked.connect(self.back)
        self.button_back.setGeometry(800, 600, 150, 75)  # x y
        self.button_back.setStyleSheet(
            "color: rgba(255,255,255,1);  font: bold;  border-style: solid;  border-width: 1px;  "
            "border-color: grey; background-color: rgb(54, 73, 78); font-size: 20px; ")

    def labelTXT(self, fileText1):
        self.label_txt = QtWidgets.QLabel(self)
        self.label_txt.setGeometry(QtCore.QRect(100, 10, 400, 440))  # x, y, width, height
        self.label_txt.setWordWrap(True)
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: rgba(255, 255, 255, 1); font: bold; font-size: 18px")
        self.label_txt.setText(str(fileText1))

    def labelTimer(self):
        self.label_Time = QLabel("label_Time", self)
        self.label_Time.setGeometry(QtCore.QRect(650, 400, 300, 120))
        self.label_Time.setObjectName("label_Time")
        self.label_Time.setStyleSheet("color: rgba(255, 0, 0, 1); font: bold; font-size: 72px")
        self.label_Time.setText(str("05.00") + " s")
        self.label_Time.hide()

    def ok(self):
        print("Button Pressed OK")
        fileText2 = open(self.fileWin2, encoding='utf-8', mode="r").read()

        # Sämtliche Anzeigen des Fensters verstecken
        self.label_txt.setText(fileText2)
        self.label_GIF.setVisible(False)
        self.button_ok.hide()
        self.button_back.hide()

        self.label_Time.show()


        # Init for Detection
        detector = pm.poseDetector()
        flipflopflag = False
        count = 0
        while True:
            success, img = self.cap.read()
            img = detector.findPose(img, draw=False)
            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                if lmList[27][3] > 90 and lmList[28][3] > 90 and lmList[23][1] < 380 \
                        and lmList[24][1] > 270:
                    if not self.myCount.isActive():
                        self.myCount.start(100)

            # Array lmList enthält die 32 Landmarks der PoseDetection.
            # Element 0 enthält die ID
            # Element 1 enthält die X Koordinate des Landmarks
            # Element 2 enthält die Y Koordinate des Landmarks
            # Element 3 enthält die Visibility des Landmarks
            if len(lmList) != 0:
                # ID 1 = Hampelmann
                # ID 2 = Kniebeugen
                if self.trainingID == 1:
                    # Anzahl an ausführungen die gewertet werden
                    if count < 20:
                        # Bereiche der Ruheposition
                        if lmList[15][1] < 420 and lmList[15][2] > 240 and lmList[16][1] > 250 and lmList[16][2] > 240 \
                                and not flipflopflag and self.myTime.isActive():
                            flipflopflag = True
                            count += 1
                            print(count)

                        # Bereiche der Arbeitsposition
                        if lmList[15][1] > 500 and lmList[15][2] < 150 and lmList[16][1] < 150 and lmList[16][2] < 150 \
                                and flipflopflag and self.myTime.isActive():
                            flipflopflag = False
                            count += 1
                            print(count)
                    else:
                        # Ausgabe der Süßigkeit. Motor ansteuern, Timer beenden um Programm für neudurchlauf vorzubereiten
                        # motor.start(1) # id_sweets
                        self.stopTimer()
                        print("SUCCESS")
                        break
                # Hier beginnt dann TrainingsID 2
                elif self.trainingID == 2:
                    '''Hier dann weitere Auswertungen für ID 2'''

            cv2.imshow("Image", img)
            cv2.waitKey(10)

    '''
    Countdown = Function for displaying the inital Countdown before the unit.
    Timer = Function for displaying the time the user has to complete the unit.  
    StopTimer = Function to stop the QTimer-Timers
    '''

    def countdown(self):
        if self.count != 0:
            self.count -= 100
            self.label_Time.setText(str(self.count / 1000) + "s")
            if self.count == 0:  # wenn Countdown fertig, dann neuen Timer starten für Übungszeit
                self.myTime.start(1000)

    def timer(self):
        self.myCount.stop()
        if self.count == 0 and self.time != 0:
            self.label_Time.setGeometry(QtCore.QRect(650, 100, 250, 80))    # Label resize da Minuten Timer relativ groß
            self.time -= 1                                                  # Sekundenweise decrement
            num = self.time / 60                                            # 120s in Minuten wandeln
            separate = math.modf(num)                                       # Dezimalzahl trennen in Int + Decimal
            new_string = str(int(separate[1])).zfill(2) + ":" + str(round(separate[0] * 60)).zfill(
                2) + "min"                                                  # Timer String zusammenbauen, zfill um "0" vor der Zahl zu setzen
            self.label_Time.setText(new_string)
        else:
            self.myTime.stop()

    def stopTimer(self):
        self.label_Time.setText("ASDFASD")
        self.close()
        self.deleteLater()

    def back(self):
        print("Button Pressed back")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Ui_Dialog()
    sys.exit(app.exec_())
