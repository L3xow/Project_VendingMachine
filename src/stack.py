import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mainwindow import *




class stackExample(QWidget):

    def __init__(self):
        super(stackExample, self).__init__()
        self.Stack = QStackedWidget(self)
        self.Stack1 = QWidget()
        self.Stack2 = QWidget()

        self.StackUi1()


        self.Stack.addWidget(self.Stack1)
        self.Stack.addWidget(self.Stack2)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
#        self.setStyleSheet("background-color: rgb(255,255,255)")
        self.show()



    def display(self, i):
        self.Stack.setCurrentIndex(i)


    def StackUi1(self):
        pic = QPixmap("src/misc/PlaceHolder.jpg")
        layout  = QBoxLayout(0)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setSpacing(50)
        label = QLabel("TestLabel")
        label1 = QLabel("TestLabel2")
        label2 = QLabel("TEstLabel3")
        labelpic = QLabel()
        labelpic.setPixmap(pic)
        label1.setObjectName("Label2tochange")
        label.setObjectName("Labeltochange")
        layout.addWidget(label)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(labelpic)
        layout.addWidget(QCheckBox("Test"))

#        self.label_txt = QLabel(self)
#        self.label_txt.move(500, 500)
#        self.label_txt.setText("Platzhalter")
#        self.label_txt.setObjectName("label_txt")
#        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
#        self.label_txt.adjustSize()
        self.Stack1.setLayout(layout)

    def StackUi2(self):
        self.label_txt = QLabel(self)
        self.label_txt.move(700, 500)
        self.label_txt.setText("Platzhalter_5")
        self.label_txt.setObjectName("label_txt")
#        self.label_txt.setStyleSheet("color: black; font: bold; font-size: 22px")
        self.label_txt.adjustSize()




def main():
    app = QApplication(sys.argv)
    win = stackExample()


    win.display(0)
    win.show()

    with open("misc/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()