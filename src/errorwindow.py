from PyQt5 import Qt
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

    def setupUI(self, ErrID):
        self.buttonOk.resize(120, 50)
        self.buttonOk.move((400-120)/2, 300-50)
        self.buttonOk.clicked.connect(self.butOK)

        self.textlabel.setAlignment(Qt.AlignmentFlag(Qt.AlignCenter))
        self.textlabel.move(40, 20)
        self.textlabel.setStyleSheet("color: red; font-weight: bold; font-size: 16px")
        self.textlabel.setText("asdf")
        self.show()

        if ErrID == 1:
            self.textlabel.setText("Error: RFID Code nicht angelegt oder nicht genügend Guthaben!")
            self.textlabel.resize(300, 200)
            self.textlabel.setWordWrap(True)
            self.textlabel.show()
        elif ErrID == 2:
            self.textlabel.setText("Error: RFID noch einmal scannen!")
            self.textlabel.show()

    def butOK(self):
        self.close()