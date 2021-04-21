"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  info_page.py

@Time    :  2021.4.16

@Desc    : RFIShow信息提示界面

"""


from PyQt5 import QtGui, QtCore, QtWidgets

class InfoPage(QtWidgets.QWidget):
    def __init__(self, Stack):
        super(InfoPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('InfoPage')

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("程序正在运行\n请稍等...")
        self.lb_title.setGeometry(QtCore.QRect(0, 262, 1920, 500))
        font.setPointSize(48)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)

    def set_title(self, info):
        self.lb_title.setText(info)