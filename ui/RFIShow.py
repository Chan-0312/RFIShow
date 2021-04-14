import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PIL import Image


from core.RfiFeatures import RfiFeatures
import pandas as pd
import pickle


class MainPage(QtWidgets.QWidget):
    def __init__(self, Stack):
        super(MainPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('MainPage')

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
            self.Stack.setCurrentIndex(2)
        elif pb.objectName() == "pb_to_p3":
            print("pb_to_p3")
            self.Stack.setCurrentIndex(1)


class ClusterPage(QtWidgets.QWidget):
    def __init__(self, Stack):
        super(ClusterPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.rfi_feature_data = pd.read_csv("../data/temp_data/rfi_feature_data_10000.csv")
        self.X_reduction = pickle.load(open("../data/temp_data/X_reduction_10000.pkl", 'rb'))
        self.cluster_labels = pickle.load(open("../data/temp_data/cluster_labels_10000.pkl", 'rb'))
        # 归一化
        self.X_reduction = self.X_reduction - self.X_reduction.min(axis=0)
        self.X_reduction = self.X_reduction / self.X_reduction.max(axis=0)

        self.Rfi_F = None
        self.show_index_num = 0

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('ClusterPage')

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("RFI聚类分析")
        self.lb_title.setGeometry(QtCore.QRect(0, 0, 1920, 100))
        font.setPointSize(48)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)

        self.pb_return = QtWidgets.QPushButton(self)
        self.pb_return.setGeometry(QtCore.QRect(0, 0, 100, 100))
        font.setPointSize(16)
        self.pb_return.setFont(font)
        self.pb_return.setText("返回")
        self.pb_return.setObjectName("pb_return")
        self.pb_return.clicked.connect(self.pb_return_action)

        self.image_1 = QtWidgets.QLabel(self)
        self.image_1.setGeometry(QtCore.QRect(20, 120, 900, 720))
        self.image_1.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_1.setAlignment(QtCore.Qt.AlignCenter)
        self.image_1.setObjectName("image_1")
        self.image_1.setScaledContents(True)
        img = Image.open("../test/cluster_image.png")
        pix = img.toqpixmap()
        self.image_1.setPixmap(pix)

        self.image_2 = QtWidgets.QLabel(self)
        self.image_2.setGeometry(QtCore.QRect(1000, 120, 900, 720))
        self.image_2.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.image_2.setObjectName("image_2")
        self.image_2.setScaledContents(True)
        img = Image.open("../test/rfi_feature_image.png")
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)

        self.lb_cluster_num = QtWidgets.QLabel(self)
        self.lb_cluster_num.setGeometry(QtCore.QRect(1000, 120, 50, 50))
        font.setPointSize(24)
        self.lb_cluster_num.setFont(font)
        self.lb_cluster_num.setText("X")

        self.pb_set = QtWidgets.QPushButton(self)
        self.pb_set.setGeometry(QtCore.QRect(20, 880, 900, 100))
        font.setPointSize(48)
        self.pb_set.setFont(font)
        self.pb_set.setText("参数设置")
        self.pb_set.setObjectName("pb_set")

        self.pb_start = QtWidgets.QPushButton(self)
        self.pb_start.setGeometry(QtCore.QRect(1000, 880, 900, 100))
        font.setPointSize(48)
        self.pb_start.setFont(font)
        self.pb_start.setText("启动分析")
        self.pb_start.setObjectName("pb_start")

        self.hs_edge_size = QtWidgets.QSlider(self)
        self.hs_edge_size.setGeometry(QtCore.QRect(1400, 50, 500, 50))
        self.hs_edge_size.setMaximum(100)
        self.hs_edge_size.setProperty("value", 2)
        self.hs_edge_size.setOrientation(QtCore.Qt.Horizontal)
        self.hs_edge_size.setObjectName("hs_edge_size")
        self.hs_edge_size.valueChanged.connect(self.hs_valuechange_action)

    def hs_valuechange_action(self):
        edge_size = self.hs_edge_size.value()

        show_num = self.show_index_num

        self.show_RFIfeatures(show_num, edge_size=edge_size)


    def pb_return_action(self):
        self.Stack.setCurrentIndex(0)

    def mousePressEvent(self, event):  # 鼠标键按下时调用(任意一个键,按一下调一次)，这些方法是许多控件自带的，这里来自于QWidget。
        if event.button() == 1:
            xy = event.pos() - QtCore.QPoint(92, 176)  # 返回鼠标坐标 (92,176), (814,606)
            x = xy.x() / 814
            y = xy.y() / 606
            if x < 0 or x > 1 or y < 0 or y > 1:
                return
            y = 1 - y
            import numpy as np

            distance = (self.X_reduction[:,0] - x) ** 2 + (self.X_reduction[:,1] - y) ** 2
            if distance.min() < 0.0001:
                index_num = np.where(distance == distance.min())[0][0]
                self.show_index_num = index_num
                self.show_RFIfeatures(index_num)

    def show_RFIfeatures(self, show_num, edge_size=2):
        self.Stack.setCurrentIndex(2)
        QtWidgets.QApplication.processEvents()
        rfi_feature = self.rfi_feature_data.iloc[show_num].values

        if self.Rfi_F is not None and self.Rfi_F.fits_path == rfi_feature[0]:
            pass
        else:
            self.Rfi_F = RfiFeatures(rfi_feature[0])

        self.Rfi_F.part_rfi_show(rfi_feature, edge_size=edge_size, save_fig="../data/temp_data/")
        img = Image.open("../data/temp_data/rfi_feature_image.png")
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)

        self.lb_cluster_num.setText(str(self.cluster_labels[show_num]))
        self.Stack.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()



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





class RFIShow(QtWidgets.QWidget):
    def __init__(self):
        super(RFIShow, self).__init__()

        self.setGeometry(0, 0, 1920, 1024)
        self.setMaximumSize(QtCore.QSize(1920, 1024))
        self.setMinimumSize(QtCore.QSize(1920, 1024))
        self.setWindowTitle('RFIShow_v0.1---by 熊盛春')
        self.setObjectName('RFIShow')

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.setGeometry(QtCore.QRect(0, 0, 1920, 1024))

        self.main_page = MainPage(self.Stack)
        self.Stack.addWidget(self.main_page)

        self.cluster_page = ClusterPage(self.Stack)
        self.Stack.addWidget(self.cluster_page)

        self.info_page = InfoPage(self.Stack)
        self.Stack.addWidget(self.info_page)

        self.Stack.setCurrentWidget(self.main_page)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    demo = RFIShow()
    demo.show()
    sys.exit(app.exec_())