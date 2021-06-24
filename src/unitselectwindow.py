from PyQt5.QtGui import QMovie, QMouseEvent
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import QtCore, Qt, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from dialog_test import Ui_Dialog


class UnitSelectWindow(QWidget):
    def __init__(self, id_sweets, parent=None):
        super().__init__(parent)

        # to save chosen sweet from first window
        self.id_sweets = id_sweets

        # Configuration of created Window
        self.setObjectName("UnitSelectWindow")
        self.resize(1920, 1080)
        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Width and Height for GIF´s for easier use
        self.width = 300
        self.height = 300

        # Call Labels
        self.labelGIF("src/misc/Hampelmann.gif", 180, 210, 0)
        self.labelGIF("src/misc/squats.gif", 620, 210, 1)
        self.labelGIF("src/misc/pushup.gif", 1060, 210, 2)
        self.labelGIF("src/misc/burpees.gif", 1500, 210, 3)

        # Label configuration
        # GIF Label

    def labelGIF(self, fileGIF, x, y, i):
        self.label_GIF = QLabel("", self)
        self.label_GIF.setGeometry(QtCore.QRect(x, y, self.width, self.height))  # x y width height
        self.label_GIF.setText("")
        self.movie = QMovie(fileGIF)
        self.label_GIF.setMovie(self.movie)
        self.movie.start()

    # Selfwritten MouseReleaseEvent with correct areas to recognize a click on the GIFs in the window

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        x = a0.x()
        y = a0.y()
        # Leftmost GIF
        if 180 <= x <= 480 and 210 <= y <= 510:
            self.Unit_One()
        # 2nd leftmost GIF
        if 620 <= x <= 620+300 and 210 <= y <= 510:
            self.Unit_Two()
        # 3rd leftmost GIF
        if 1060 <= x <= 1060+300 and 210 <= y <= 510:
            self.Unit_Three()
        # 4th leftmost GIF
        if 1500 <= x <= 1500+300 and 210 <= y <= 510:
            self.Unit_Four()

    # Functions to call the dialog and explanation Window
    def Unit_One(self):
        # First and most important explanation, filler txt-file, GIF File, Exercise ID, saved sweet id which was
        # chosen in first Window from User
        self.w = Ui_Dialog("src/misc/Mainwindowdescr.txt", "src/misc/Dialogwindowdescr.txt", "src/misc/Hampelmann.gif", 1, self.id_sweets)
        self.w.show()
        self.close()

    def Unit_Two(self):
        # First and most important explanation, filler txt-file, GIF File, Exercise ID, saved sweet id which was
        # chosen in first Window from User
        self.w = Ui_Dialog("src/misc/Mainwindowdescr.txt", "src/misc/Dialogwindowdescr.txt", "src/misc/squats.gif", 2, self.id_sweets)
        self.w.show()
        self.close()

    def Unit_Three(self):
        # First and most important explanation, filler txt-file, GIF File, Exercise ID, saved sweet id which was
        # chosen in first Window from User
        self.w = Ui_Dialog("src/misc/Mainwindowdescr.txt", "src/misc/Dialogwindowdescr.txt", "src/misc/pushup.gif", 3, self.id_sweets)
        self.w.show()
        self.close()

    def Unit_Four(self):
        # First and most important explanation, filler txt-file, GIF File, Exercise ID, saved sweet id which was
        # chosen in first Window from User
        self.w = Ui_Dialog("src/misc/Mainwindowdescr.txt", "src/misc/Dialogwindowdescr.txt", "src/misc/pushup.gif", 4, self.id_sweets)
        self.w.show()
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = UnitSelectWindow()
    sys.exit(app.exec_())
