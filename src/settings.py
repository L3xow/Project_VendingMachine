"""
PU = PushUp
JJ = JumpingJacks
SQ = Squats
LG = Lunges

RPi = Raspberry Pi

Reps = Wiederholungen.
"""

# Global Variables for managing the counters for the filling levels
actValueOne = 0
actValueTwo = 0
actValueThree = 0
actValueFour = 0
isClicked = False

# Settings to change the units
Tolerance = 0.8  # 80%

PUTime = 60             # seconds
PUReps = 20 * Tolerance

JJTime = 10
JJReps = 2 * Tolerance

SQTime = 10 # 60
SQReps = 2 * Tolerance # 30

LGTime = 30
LGReps = 20 * Tolerance

CounterReset = 15

CamID = 1

#RPiIP = "192.168.2.41" # Tobi HomePi
#RPiIP = "192.168.137.61 # Tobi LaptopPi
RPiIP = "192.168.1.103" # Tobi NurembergPi


# def errorLowCount(self, sweetid):
#     self.pixmap_warning = QPixmap("src/misc/warning.png")
#     self.smaller_pixmap_warning = self.pixmap_warning.scaled(64, 64, Qt.KeepAspectRatio, Qt.FastTransformation)
#
#     self.msg = QMessageBox()
#     self.msg.setWindowFlags(Qt.FramelessWindowHint)
#     self.msg.setIconPixmap(self.smaller_pixmap_warning)
#     self.msg.setText("Vorrat neigt sich dem Ende! Bitte auffüllen.")
#     self.msg.setInformativeText("Vorrat Süßigkeit Nr.: " + str(sweetid))
#     # self.msg.setDetailedText("Detailed Text")
#     self.msg.setWindowTitle("Warning")
#     self.msg.setStandardButtons(QMessageBox.Ok)
#     self.msg.setStyleSheet("QMessageBox {background-color: rgb(200,200,200); color: grey;}"
#                            "QPushButton {width: 120px; height: 50px; border: 2px solid white; font-size: 10px; font-weight: bold;"
#                            "background-color: DimGrey; color: white;}"
#                            "QPushButton::pressed { border: 3px solid grey; }"
#                            "QLabel {font-size: 16px; font-weight: bold; color: black;}")
#     self.msg.show()
#     return