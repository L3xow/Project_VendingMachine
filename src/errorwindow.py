from PyQt5 import Qt, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt



class errorwindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ErrorMsg")
        self.setObjectName("ErrorMsg")
        self.resize(400, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.buttonOk = QPushButton("Ok", self)
        self.textlabel = QLabel(self)
        self.pixlabel = QLabel(self)

    def setupUI(self, ErrID, SweetID):
        self.sweets = SweetID
        self.buttonOk.resize(120, 50)
        self.buttonOk.move((400-120)/2, 300-50)
        self.buttonOk.clicked.connect(self.butOK)

        self.textlabel.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.textlabel.move(40, 20)
        self.textlabel.setStyleSheet("color: black; font-weight: bold; font-size: 16px")
        self.textlabel.setWordWrap(True)
        self.textlabel.resize(300, 200)

        self.pixmap_error = QPixmap("src/misc/error.png")
        self.smaller_pixmap_error = self.pixmap_error.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.pixmap_warning = QPixmap("src/misc/warning.png")
        self.smaller_pixmap_warning = self.pixmap_warning.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.pixlabel.setPixmap(self.smaller_pixmap_error)
        self.pixlabel.move(10, 10)
        self.pixlabel.show()



        self.setStyleSheet(
            "QDialog { background-color: rgb(200,200,200); }"
            "QPushButton { border: 2px solid white; font-size: 10px; font-weight: bold; "
            "background-color: DimGrey; color: white;} "
            "QPushButton::pressed { border: 3px solid grey; }")


        self.show()
        
        # ToDo: LEDs nach farben einfügen
        if ErrID == 1:
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
#            self.pixlabel.setPixmap(QtGui.QPixmap("error.png"))
            self.textlabel.setText("Error: RFID Code nicht angelegt oder nicht genügend Guthaben!")
            self.textlabel.show()
        elif ErrID == 2:
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: RFID noch einmal scannen!")
            self.textlabel.show()
        elif ErrID == 3:
            self.pixlabel.setPixmap(self.smaller_pixmap_warning)
            self.textlabel.setText("Warnung: Füllstand " + str(self.sweets) + ". Süßigkeit zu niedrig")
            self.show()
        elif ErrID == 4:
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: Plexiglas Platte nicht ordnungsgemäß befestigt!")
            self.show()
        elif ErrID == 5:
            self.pixlabel.setPixmap(self.smaller_pixmap_error)
            self.textlabel.setText("Error: Wartungsschalter an der Rückseite ist ausgeschalten!")
            self.show()

    def butOK(self):
        # ToDo: LED GREEN and RESET other LEDS
        self.close()