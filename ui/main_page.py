"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  main_page.py

@Time    :  2021.4.16

@Desc    : RFIShow主界面

"""


from PyQt5 import QtGui, QtCore, QtWidgets
from conf.settings import args



class MainPage(QtWidgets.QWidget):
    def __init__(self, Stack):
        super(MainPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('MainPage')

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_gif = QtWidgets.QLabel(self)
        self.lb_gif.setGeometry(QtCore.QRect(40, 160, 1300, 560+240)) # 500,280
        self.lb_gif.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_gif.setScaledContents(True)
        self.gif = QtGui.QMovie(args["project_path"]+'/resource/main_dynamic.gif')
        self.lb_gif.setMovie(self.gif)
        self.gif.start()

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("RFIShow")
        self.lb_title.setGeometry(QtCore.QRect(0, 0, 1920, 100))
        font.setPointSize(48)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)

        self.pb_to_p1 = QtWidgets.QPushButton(self)
        self.pb_to_p1.setGeometry(QtCore.QRect(1400, 200, 480, 100))
        font.setPointSize(16)
        self.pb_to_p1.setFont(font)
        self.pb_to_p1.setText("RFI检测")
        self.pb_to_p1.setObjectName("pb_to_p1")

        self.pb_to_p2 = QtWidgets.QPushButton(self)
        self.pb_to_p2.setGeometry(QtCore.QRect(1400, 500, 480, 100))
        font.setPointSize(16)
        self.pb_to_p2.setFont(font)
        self.pb_to_p2.setText("RFI特征提取")
        self.pb_to_p2.setObjectName("pb_to_p2")

        self.pb_to_p3 = QtWidgets.QPushButton(self)
        self.pb_to_p3.setGeometry(QtCore.QRect(1400, 800, 480, 100))
        font.setPointSize(16)
        self.pb_to_p3.setFont(font)
        self.pb_to_p3.setText("RFI聚类分析")
        self.pb_to_p3.setObjectName("pb_to_p3")

        self.pb_to_p1.clicked.connect(lambda : self.pb_action(self.pb_to_p1))
        self.pb_to_p2.clicked.connect(lambda : self.pb_action(self.pb_to_p2))
        self.pb_to_p3.clicked.connect(lambda : self.pb_action(self.pb_to_p3))

    def pb_action(self, pb):
        if pb.objectName() == "pb_to_p1":
            self.Stack.setCurrentIndex(1)
        elif pb.objectName() == "pb_to_p2":
            self.Stack.setCurrentIndex(2)
        elif pb.objectName() == "pb_to_p3":
            self.Stack.setCurrentIndex(3)

