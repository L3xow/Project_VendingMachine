
'''
Das ist unser Code für die Projektarbeit an der Rudolf Diesel Fachschule in Nürnberg.
Der Code ist hauptsächlich zur Steuerung unseres nachhaltigen Süßigkeitenautomaten.

Die Hierarchie des Programms ist wiefolgt:
mainwindow.py
    unitselectwindow.py
        dialog_test.py
            motor.py
            PoseModule.py

mainwindow.py
    Pick Sweets, one out of three. If one is picked, we open unitselectwindow.py and save the picked ID.
unitselectwindow.py
    Pick 1 out of four Units to do. From there we open the dialog_test.py where we explain the Unit and do the exercise recognition.

'''



from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from dialog_test import Ui_Dialog
from unitselectwindow import UnitSelectWindow
# import sys


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

# Konfiguration des Fensters (Name, Größe, Hintergrundfarbe)
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(Qt.FramelessWindowHint)

# Bild Links
        self.label = QLabel("label", self)
        self.label.setGeometry(QtCore.QRect(180, 210, 300, 300))  # x y width height
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("src/misc/PlaceHolder.jpg"))
        self.label.setObjectName("label")
        self.label.mouseReleaseEvent = self.DialogWindowOne

# Überschrift Bild Links tlinks = text links
        self.label_tlinks = QLabel("label_tlinks", self)
        self.label_tlinks.move(180, 180)
        self.label_tlinks.setText("Übung1_Placeholder")
        self.label_tlinks.setObjectName("label_tlinks")
        self.label_tlinks.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_tlinks.adjustSize()

# Bild Links Mitte
        self.label_1 = QLabel("label_1", self)
        self.label_1.setGeometry(QtCore.QRect(620, 210, 300, 300))  # x y width height
        self.label_1.setText("")
        self.label_1.setPixmap(QtGui.QPixmap("src/misc/PlaceHolder.jpg"))
        self.label_1.setObjectName("label_1")
        self.label_1.mouseReleaseEvent = self.DialogWindowTwo

# Überschrift Bild Links Mitte tlinksm = text links mitte
        self.label_tlinksm = QLabel("label_tlinksm", self)
        self.label_tlinksm.move(620, 180)
        self.label_tlinksm.setText("Übung2_Placeholder")
        self.label_tlinksm.setObjectName("label_tlinksm")
        self.label_tlinksm.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_tlinksm.adjustSize()

# Bild Rechts Mitte
        self.label_2 = QLabel("label_2", self)
        self.label_2.setGeometry(QtCore.QRect(1060, 210, 300, 300))  # x y width height
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("src/misc/PlaceHolder.jpg"))
        self.label_2.setObjectName("label_2")
        self.label_2.mouseReleaseEvent = self.DialogWindowThree

# Überschrift Bild Rechts Mitte trechtsm = text rechts mitte
        self.label_trechtsm = QLabel("label_trechtsm", self)
        self.label_trechtsm.move(1060, 180)
        self.label_trechtsm.setText("Übung3_placeholder")
        self.label_trechtsm.setObjectName("label_trechtsm")
        self.label_trechtsm.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_trechtsm.adjustSize()

# Bild Rechts
        self.label_3 = QLabel("label_3", self)
        self.label_3.setGeometry(QtCore.QRect(1500, 210, 300, 300))  # x y width height
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("src/misc/PlaceHolder.jpg"))
        self.label_3.setObjectName("label_3")
#        self.label_3.mouseReleaseEvent = self.DialogWindowFour

# Überschrift Bild Rechts Mitte trechts = text rechts
        self.label_trechts = QLabel("label_trechts", self)
        self.label_trechts.move(1500, 180)
        self.label_trechts.setText("Übung3_placeholder")
        self.label_trechts.setObjectName("label_trechts")
        self.label_trechts.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_trechts.adjustSize()

# Um die erzeugten Objekte anzeigen zu lassen
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            app.quit()

    def DialogWindowOne(self, event):         # Function des ganz linken GIFs
        id_sweets = 1
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
        self.win = UnitSelectWindow(id_sweets)
        self.win.show()

    def DialogWindowTwo(self, event):         # Function des 2. GIFS von Links
        id_sweets = 2
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
        self.win = UnitSelectWindow(id_sweets)
        self.win.show()

    def DialogWindowThree(self, event):       # Function des 3. GIFS von Links
        id_sweets = 3
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
        self.win = UnitSelectWindow(id_sweets)
        self.win.show()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    sys.exit(app.exec())
