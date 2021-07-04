
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
    Pick Sweets, one out of three. If one is picked, we open unitselectwindow.py and save the picked ID.
unitselectwindow.py
    Pick 1 out of four Units to do. From there we open the userdialog.py where we explain the Unit and do the exercise recognition.

'''

# ToDo: Kommentare anpassen/übersetzen, Code Refactoren um Warnungen zu entfernen.


from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
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

    def labelTXT(self, txt, x, y):
        self.label_txt = QLabel(self)
        self.label_txt.move(x, y)
        self.label_txt.setText(str(txt))
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_txt.adjustSize()

    def labelJPG(self, jpg, x, y):
        path = os.path.dirname(os.path.abspath(__file__))
        self.label_jpg = QLabel(self)
        self.label_jpg.setGeometry(QtCore.QRect(x, y, 300, 300))  # x y width height
        self.label_jpg.setPixmap(QtGui.QPixmap(os.path.join(path, jpg)))
        self.label_jpg.setObjectName("label_jpg")

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        x = a0.x()
        y = a0.y()
        # Leftmost GIF
        if 180 <= x <= 480 and 210 <= y <= 510:
            self.DialogWindowOne()
        # 2nd leftmost GIF
        if 810 <= x <= 810 + 300 and 210 <= y <= 510:
            self.DialogWindowTwo()
        # 3rd leftmost GIF
        if 1440 <= x <= 1440 + 300 and 210 <= y <= 510:
            self.DialogWindowThree()

    def DialogWindowOne(self):  # Function des ganz linken GIFs
        self.id_sweets = 1
#        self.switch_window.emit()
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
        self.win = UnitSelectWindow(self.id_sweets)
        self.win.setupUI(1920, 1080)
        self.win.show()

    def DialogWindowTwo(self):  # Function des 2. GIFS von Links
        self.id_sweets = 2
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
        self.win = UnitSelectWindow(self.id_sweets)
        self.win.setupUI(1920, 1080)
        self.win.show()

    def DialogWindowThree(self):  # Function des 3. GIFS von Links
        self.id_sweets = 3
        # Call UnitSelectWindow with parameter id_sweets to recognize which sweet was chosen.
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
    win = UI_MainWindow()
    win.setupUi(win.width, win.height)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()