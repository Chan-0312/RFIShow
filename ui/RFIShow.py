import sys
from PyQt5 import  QtGui, QtCore, QtWidgets

class main_page(QtWidgets.QWidget):
    def __init__(self):
        super(main_page, self).__init__()
        self.setGeometry(0, 0, 1920, 1024)

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("RFIShow可视化软件")
        self.lb_title.setGeometry(QtCore.QRect(0, 0, 1920, 100))
        font.setPointSize(48)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)

        self.pb_to_p1 = QtWidgets.QPushButton(self)
        self.pb_to_p1.setGeometry(QtCore.QRect(700, 200, 500, 100))
        font.setPointSize(16)
        self.pb_to_p1.setFont(font)
        self.pb_to_p1.setText("RFI可视化")
        self.pb_to_p1.setObjectName("pb_to_p1")

        self.pb_to_p2 = QtWidgets.QPushButton(self)
        self.pb_to_p2.setGeometry(QtCore.QRect(700, 500, 500, 100))
        font.setPointSize(16)
        self.pb_to_p2.setFont(font)
        self.pb_to_p2.setText("RFI局部分析")
        self.pb_to_p2.setObjectName("pb_to_p2")

        self.pb_to_p3 = QtWidgets.QPushButton(self)
        self.pb_to_p3.setGeometry(QtCore.QRect(700, 800, 500, 100))
        font.setPointSize(16)
        self.pb_to_p3.setFont(font)
        self.pb_to_p3.setText("RFI聚类分析")
        self.pb_to_p3.setObjectName("pb_to_p3")

        self.pb_to_p1.clicked.connect(lambda : self.pb_action(self.pb_to_p1))
        self.pb_to_p2.clicked.connect(lambda : self.pb_action(self.pb_to_p2))
        self.pb_to_p3.clicked.connect(lambda : self.pb_action(self.pb_to_p3))

    def pb_action(self, pb):
        if pb.objectName() == "pb_to_p1":
            print("pb_to_p1")
        elif pb.objectName() == "pb_to_p2":
            print("pb_to_p2")
        elif pb.objectName() == "pb_to_p3":
            print("pb_to_p3")



class RFIShow(QtWidgets.QWidget):
    def __init__(self):
        super(RFIShow, self).__init__()

        self.setGeometry(0, 0, 1920, 1024)
        self.setMaximumSize(QtCore.QSize(1920, 1024))
        self.setWindowTitle('RFIShow_v0.1---by 熊盛春')

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.setGeometry(QtCore.QRect(0, 0, 1920, 1024))
        x = main_page()
        self.Stack.addWidget(x)
        self.Stack.setCurrentIndex(0)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    demo = RFIShow()
    demo.show()
    sys.exit(app.exec_())