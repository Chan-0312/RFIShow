"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rfi_cluster_page.py

@Time    :  2021.4.16

@Desc    : rfi聚类可视化界面

"""

from PIL import Image
import pickle
from PyQt5 import QtGui, QtCore, QtWidgets
from conf import args, save_sttings
from core.rfi_features import RfiFeatures


class SettingsPage(QtWidgets.QWidget):
    """
    参数设置界面
    """

    def __init__(self):
        """
        参数设置界面
        """
        super(SettingsPage, self).__init__()

        self.setWindowTitle("参数设置")
        self.setObjectName("SettingsPage")
        self.resize(800, 530)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 70 - 50, 80, 20))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("文件设置")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 80 - 50, 20, 121))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(780, 80 - 50, 20, 121))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(10, 190 - 50, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setGeometry(QtCore.QRect(90, 70 - 50, 701, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 150 - 50, 130, 40))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("分析样本数量")
        self.le_select_csv = QtWidgets.QLineEdit(self)
        self.le_select_csv.setEnabled(False)
        self.le_select_csv.setGeometry(QtCore.QRect(160, 100 - 50, 620, 40))
        self.le_select_csv.setFont(font)
        self.le_select_csv.setObjectName("le_select_csv")
        self.pb_select_csv = QtWidgets.QPushButton(self)
        self.pb_select_csv.setGeometry(QtCore.QRect(20, 100 - 50, 130, 40))
        self.pb_select_csv.setFont(font)
        self.pb_select_csv.setObjectName("pb_select_csv")
        self.pb_select_csv.setText("文件选择")
        self.sb_sample_num = QtWidgets.QSpinBox(self)
        self.sb_sample_num.setGeometry(QtCore.QRect(160, 150 - 50, 620, 40))
        self.sb_sample_num.setFont(font)
        self.sb_sample_num.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_sample_num.setAccelerated(True)
        self.sb_sample_num.setMaximum(10000)
        self.sb_sample_num.setMinimum(500)
        self.sb_sample_num.setSingleStep(500)
        self.sb_sample_num.setObjectName("sb_sample_num")


        self.line_5 = QtWidgets.QFrame(self)
        self.line_5.setGeometry(QtCore.QRect(0, 220 - 50, 20, 111-50))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self)
        self.line_6.setGeometry(QtCore.QRect(10, 320 - 50 - 50, 781, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 210 - 50, 120, 20))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("TSNE降维设置")
        self.line_7 = QtWidgets.QFrame(self)
        self.line_7.setGeometry(QtCore.QRect(90 + 40, 210 - 50, 701-40, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self)
        self.line_8.setGeometry(QtCore.QRect(780, 220 - 50, 20, 111-50))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 230 - 50, 130, 40))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setText("混乱度")
        self.label_5.setObjectName("label_5")
        self.sb_tsne_perplexity = QtWidgets.QSpinBox(self)
        self.sb_tsne_perplexity.setGeometry(QtCore.QRect(160, 230 - 50, 620, 40))
        self.sb_tsne_perplexity.setFont(font)
        self.sb_tsne_perplexity.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_tsne_perplexity.setAccelerated(True)
        self.sb_tsne_perplexity.setMaximum(500)
        self.sb_tsne_perplexity.setMinimum(10)
        self.sb_tsne_perplexity.setSingleStep(10)
        self.sb_tsne_perplexity.setObjectName("sb_tsne_perplexity")



        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(20, 340 - 50-50, 80, 20))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("聚类设置")
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.setGeometry(QtCore.QRect(20, 260, 130, 40))
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setText("聚类方法")
        self.label_1.setObjectName("label_1")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(410, 360 - 50-50, 130, 40))
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("聚类类别数")
        self.line_9 = QtWidgets.QFrame(self)
        self.line_9.setGeometry(QtCore.QRect(0, 350 - 50-50, 20, 61+50))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self)
        self.line_10.setGeometry(QtCore.QRect(90, 340 - 50-50, 701, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self)
        self.line_11.setGeometry(QtCore.QRect(780, 350 - 50-50, 20, 61+50))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.line_12 = QtWidgets.QFrame(self)
        self.line_12.setGeometry(QtCore.QRect(10, 400 - 50, 781, 16))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.sb_n_clusters = QtWidgets.QSpinBox(self)
        self.sb_n_clusters.setGeometry(QtCore.QRect(520, 360 - 50 - 50, 260, 40))
        self.sb_n_clusters.setFont(font)
        self.sb_n_clusters.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_n_clusters.setAccelerated(True)
        self.sb_n_clusters.setMaximum(20)
        self.sb_n_clusters.setMinimum(2)
        self.sb_n_clusters.setSingleStep(2)
        self.sb_n_clusters.setObjectName("sb_n_clusters")
        self.cbb_cluster_mode = QtWidgets.QComboBox(self)
        self.cbb_cluster_mode.setGeometry(QtCore.QRect(160, 260, 260, 40))
        self.cbb_cluster_mode.setFont(font)
        self.cbb_cluster_mode.setObjectName("cbb_cluster_mode")
        self.cbb_cluster_mode.addItem("AgglomerativeClustering")
        self.cbb_cluster_mode.addItem("KMeans")
        self.cbb_cluster_mode.addItem("GaussianMixture")





        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(20, 340 + 30, 120, 20))
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setText("特征提取设置")
        self.line_13 = QtWidgets.QFrame(self)
        self.line_13.setGeometry(QtCore.QRect(0, 350 + 30, 20, 61))
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(self)
        self.line_14.setGeometry(QtCore.QRect(90 + 40, 340 + 30, 701 - 40, 20))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.line_15 = QtWidgets.QFrame(self)
        self.line_15.setGeometry(QtCore.QRect(780, 350 + 30, 20, 61))
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.line_16 = QtWidgets.QFrame(self)
        self.line_16.setGeometry(QtCore.QRect(10, 400 + 30, 781, 16))
        self.line_16.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")





        self.pb_confirm = QtWidgets.QPushButton(self)
        self.pb_confirm.setGeometry(QtCore.QRect(10, 420 + 30, 780, 70))
        font.setPointSize(24)
        self.pb_confirm.setFont(font)
        self.pb_confirm.setObjectName("pb_confirm")
        self.pb_confirm.setText("保存")

        self.pb_select_csv.clicked.connect(self._pb_select_csv_action)
        self.pb_confirm.clicked.connect(self._pb_confirm_action)

        self.retranslateUi()

    def retranslateUi(self):
        rfi_cluster_page_args = args["rfi_cluster_page"]
        self.le_select_csv.setText(rfi_cluster_page_args["csv_path"])
        self.sb_sample_num.setValue(rfi_cluster_page_args["sample_num"])
        self.sb_tsne_perplexity.setValue(rfi_cluster_page_args["tsne_perplexity"])


    def _pb_select_csv_action(self):
        absolute_path = QtWidgets.QFileDialog.getOpenFileName(self, '请选择rfi特征文件',
                                                              '.', "csv files (*.csv)")
        if absolute_path[0] != "":
            self.le_select_csv.setText(absolute_path[0])

    def _pb_confirm_action(self):
        if self.le_select_csv.text() == "":
            return
        args["rfi_cluster_page"]["csv_path"] = self.le_select_csv.text()
        args["rfi_cluster_page"]["sample_num"] = self.sb_sample_num.value()
        args["rfi_cluster_page"]["tsne_perplexity"] = self.sb_tsne_perplexity.value()

        # 保存环境参数
        save_sttings(args, args["save_dict_list"])
        # 关闭界面
        self.close()


class RfiClusterPage(QtWidgets.QWidget):
    """
    RFI 特征聚类分析界面
    """

    def __init__(self, Stack):
        """

        :param Stack: Stack界面类
        """

        super(RfiClusterPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('RfiDetectPage')

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

        self.image_1 = QtWidgets.QLabel(self)
        self.image_1.setGeometry(QtCore.QRect(20, 120, 1100, 880))
        self.image_1.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_1.setAlignment(QtCore.Qt.AlignCenter)
        self.image_1.setObjectName("image_1")
        self.image_1.setScaledContents(True)

        self.image_2 = QtWidgets.QLabel(self)
        self.image_2.setGeometry(QtCore.QRect(1140, 120, 750, 600))
        self.image_2.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.image_2.setObjectName("image_2")
        self.image_2.setScaledContents(True)

        self.pb_set = QtWidgets.QPushButton(self)
        self.pb_set.setGeometry(QtCore.QRect(1140, 720, 375, 140))
        self.pb_set.setFont(font)
        self.pb_set.setText("参数设置")
        self.pb_set.setObjectName("pb_set")

        self.pb_save_result = QtWidgets.QPushButton(self)
        self.pb_save_result.setGeometry(QtCore.QRect(1515, 720, 375, 140))
        self.pb_save_result.setFont(font)
        self.pb_save_result.setText("保存结果")
        self.pb_save_result.setObjectName("pb_save_result")

        self.pb_rfi_reduction = QtWidgets.QPushButton(self)
        self.pb_rfi_reduction.setGeometry(QtCore.QRect(1140, 860, 375, 140))
        self.pb_rfi_reduction.setFont(font)
        self.pb_rfi_reduction.setText("特征降维")
        self.pb_rfi_reduction.setObjectName("pb_rfi_reduction")

        self.pb_rfi_cluster = QtWidgets.QPushButton(self)
        self.pb_rfi_cluster.setGeometry(QtCore.QRect(1515, 860, 375, 140))
        self.pb_rfi_cluster.setFont(font)
        self.pb_rfi_cluster.setText("特征聚类")
        self.pb_rfi_cluster.setObjectName("pb_rfi_cluster")

        # 信号连接
        self.pb_return.clicked.connect(self._pb_return_action)
        self.pb_set.clicked.connect(self._pb_set_action)

        # img = Image.open(args["project_path"]+args["temp_data"]+"cluster_image.png")
        # pix = img.toqpixmap()
        # self.image_1.setPixmap(pix)

        # 页面状态
        """
        0 - None
        1 - RFI reduction
        2 - RFI cluster
        """
        self.page_state = 0

    def _pb_return_action(self):
        self.Stack.setCurrentIndex(0)

    def _pb_set_action(self):
        self.setting_page = SettingsPage()
        self.setting_page.show()

