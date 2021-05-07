"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RFIShow.py

@Time    :  2021.4.16

@Desc    : RFIShow中的QStackedWidget界面

"""

from PyQt5 import QtGui, QtCore, QtWidgets
from ui.main_page import MainPage
from ui.rfi_detect_page import RfiDetectPage
from ui.rfi_cluster_page import RfiClusterPage
from ui.info_page import InfoPage

from conf.settings import args

class RFIShow(QtWidgets.QWidget):

    def __init__(self):
        super(RFIShow, self).__init__()

        self.setGeometry(0, 0, 1920, 1024)
        self.setMaximumSize(QtCore.QSize(1920, 1024))
        self.setMinimumSize(QtCore.QSize(1920, 1024))
        self.setWindowTitle('RFIShow_%s---by %s'%(args["version"], args["author"]))
        self.setObjectName('RFIShow')

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.setGeometry(QtCore.QRect(0, 0, 1920, 1024))

        self.main_page = MainPage(self.Stack)
        self.Stack.addWidget(self.main_page)

        self.rfishow_page = RfiDetectPage(self.Stack)
        self.Stack.addWidget(self.rfishow_page)

        self.cluster_page = RfiClusterPage(self.Stack)
        self.Stack.addWidget(self.cluster_page)

        self.info_page = InfoPage(self.Stack)
        self.Stack.addWidget(self.info_page)

        self.Stack.setCurrentWidget(self.main_page)