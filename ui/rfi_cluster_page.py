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
import os
import pickle
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from conf import args, save_sttings
from core.rfi_features import RfiFeatures
from core.rfi_cluster import RfiCluster, RfiCut


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
        self.sb_sample_num.setGeometry(QtCore.QRect(160, 150 - 50, 260, 40))
        self.sb_sample_num.setFont(font)
        self.sb_sample_num.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_sample_num.setAccelerated(True)
        self.sb_sample_num.setMaximum(50000)
        self.sb_sample_num.setMinimum(500)
        self.sb_sample_num.setSingleStep(500)
        self.sb_sample_num.setObjectName("sb_sample_num")
        self.chb_rfi_cut = QtWidgets.QCheckBox(self)
        self.chb_rfi_cut.setGeometry(QtCore.QRect(440, 150 - 50, 260, 40))
        self.chb_rfi_cut.setFont(font)
        self.chb_rfi_cut.setObjectName("chb_rfi_cut")
        self.chb_rfi_cut.setText("是否剔除无效rfi")


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
        self.sb_n_clusters.setSingleStep(2)
        self.sb_n_clusters.setObjectName("sb_n_clusters")
        self.cbb_cluster_mode = QtWidgets.QComboBox(self)
        self.cbb_cluster_mode.setGeometry(QtCore.QRect(160, 260, 260, 40))
        self.cbb_cluster_mode.setFont(font)
        self.cbb_cluster_mode.setObjectName("cbb_cluster_mode")
        self.cbb_cluster_mode.addItem("AgglomerativeClustering")
        self.cbb_cluster_mode.addItem("KMeans")
        self.cbb_cluster_mode.addItem("GaussianMixture")

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 280+30, 130, 40))
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("聚类参数")
        self.le_cluster_kwargs = QtWidgets.QLineEdit(self)
        self.le_cluster_kwargs.setEnabled(True)
        self.le_cluster_kwargs.setGeometry(QtCore.QRect(160, 280+30, 620, 40))
        self.le_cluster_kwargs.setFont(font)
        self.le_cluster_kwargs.setObjectName("le_cluster_kwargs")




        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(20, 340 + 30, 120, 20))
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setText("显示设置")
        self.line_13 = QtWidgets.QFrame(self)
        self.line_13.setGeometry(QtCore.QRect(0, 350 + 30, 20, 61))
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(self)
        self.line_14.setGeometry(QtCore.QRect(90, 340 + 30, 701, 20))
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
        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(20, 390, 130, 40))
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setText("局部视野")
        self.label_11.setObjectName("label_11")
        self.sb_edge_size = QtWidgets.QSpinBox(self)
        self.sb_edge_size.setGeometry(QtCore.QRect(160, 390, 260, 40))
        self.sb_edge_size.setFont(font)
        self.sb_edge_size.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_edge_size.setAccelerated(True)
        self.sb_edge_size.setMaximum(16)
        self.sb_edge_size.setMinimum(2)
        self.sb_edge_size.setSingleStep(2)
        self.sb_edge_size.setObjectName("sb_edge_size")



        self.pb_confirm = QtWidgets.QPushButton(self)
        self.pb_confirm.setGeometry(QtCore.QRect(10, 420 + 30, 780, 70))
        font.setPointSize(24)
        self.pb_confirm.setFont(font)
        self.pb_confirm.setObjectName("pb_confirm")
        self.pb_confirm.setText("保存")

        self.pb_select_csv.clicked.connect(self._pb_select_csv_action)
        self.pb_confirm.clicked.connect(self._pb_confirm_action)
        self.chb_rfi_cut.setDisabled(True)

        self.retranslateUi()

    def retranslateUi(self):
        rfi_cluster_page_args = args["rfi_cluster_page"]
        self.le_select_csv.setText(rfi_cluster_page_args["csv_path"])
        self.sb_sample_num.setValue(rfi_cluster_page_args["sample_num"])
        self.chb_rfi_cut.setChecked(rfi_cluster_page_args["rfi_cut"])
        self.sb_tsne_perplexity.setValue(rfi_cluster_page_args["tsne_perplexity"])
        self.cbb_cluster_mode.setCurrentIndex(rfi_cluster_page_args["cluster_mode"]-1)
        self.sb_n_clusters.setValue(rfi_cluster_page_args["n_clusters"])
        self.le_cluster_kwargs.setText(rfi_cluster_page_args["cluster_kwargs"])
        self.sb_edge_size.setValue(rfi_cluster_page_args["edge_size"])

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
        args["rfi_cluster_page"]["rfi_cut"] = self.chb_rfi_cut.isChecked()
        args["rfi_cluster_page"]["tsne_perplexity"] = self.sb_tsne_perplexity.value()
        args["rfi_cluster_page"]["cluster_mode"] = self.cbb_cluster_mode.currentIndex()+1
        args["rfi_cluster_page"]["n_clusters"] = self.sb_n_clusters.value()
        args["rfi_cluster_page"]["cluster_kwargs"] = self.le_cluster_kwargs.text()
        args["rfi_cluster_page"]["edge_size"] = self.sb_edge_size.value()

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

        self.image_3 = QtWidgets.QLabel(self)
        self.image_3.setGeometry(QtCore.QRect(1140, 120, 750, 600))
        self.image_3.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_3.setAlignment(QtCore.Qt.AlignCenter)
        self.image_3.setObjectName("image_3")
        self.image_3.setScaledContents(True)

        self.pb_set = QtWidgets.QPushButton(self)
        self.pb_set.setGeometry(QtCore.QRect(1140, 720, 250, 140))
        self.pb_set.setFont(font)
        self.pb_set.setText("参数设置")
        self.pb_set.setObjectName("pb_set")

        self.pb_display_switch = QtWidgets.QPushButton(self)
        self.pb_display_switch.setGeometry(QtCore.QRect(1515-125, 720, 250, 140))
        self.pb_display_switch.setFont(font)
        self.pb_display_switch.setText("切换显示")
        self.pb_display_switch.setObjectName("pb_display_switch")

        self.pb_rfi_cut = QtWidgets.QPushButton(self)
        self.pb_rfi_cut.setGeometry(QtCore.QRect(1515 - 125+250, 720, 250, 140))
        self.pb_rfi_cut.setFont(font)
        self.pb_rfi_cut.setText("类别剔除")
        self.pb_rfi_cut.setObjectName("pb_rfi_cut")

        self.pb_rfi_reduction = QtWidgets.QPushButton(self)
        self.pb_rfi_reduction.setGeometry(QtCore.QRect(1140, 860, 250, 140))
        self.pb_rfi_reduction.setFont(font)
        self.pb_rfi_reduction.setText("特征降维")
        self.pb_rfi_reduction.setObjectName("pb_rfi_reduction")

        self.pb_rfi_cluster = QtWidgets.QPushButton(self)
        self.pb_rfi_cluster.setGeometry(QtCore.QRect(1515-125, 860, 250, 140))
        self.pb_rfi_cluster.setFont(font)
        self.pb_rfi_cluster.setText("特征聚类")
        self.pb_rfi_cluster.setObjectName("pb_rfi_cluster")

        self.pb_save_result = QtWidgets.QPushButton(self)
        self.pb_save_result.setGeometry(QtCore.QRect(1515 - 125 + 250, 860, 250, 140))
        self.pb_save_result.setFont(font)
        self.pb_save_result.setText("保存结果")
        self.pb_save_result.setObjectName("pb_save_result")

        # 信号连接
        self.pb_return.clicked.connect(self._pb_return_action)
        self.pb_set.clicked.connect(self._pb_set_action)
        self.pb_rfi_reduction.clicked.connect(self._pb_rfi_reduction_action)
        self.pb_rfi_cluster.clicked.connect(self._pb_rfi_cluster_action)
        self.pb_display_switch.clicked.connect(self._pb_display_switch_action)
        self.pb_save_result.clicked.connect(self._pb_save_result_action)
        self.pb_rfi_cut.clicked.connect(self._pb_rfi_cut_action)

        self.image_2.setVisible(True)
        self.image_3.setVisible(False)

        # 页面状态
        """
        0 - None
        1 - RFI reduction
        2 - RFI cluster
        """
        self.page_state = 0

        if os.path.exists(args["project_path"]+args["temp_data"]+"rfi_cluster_class.pkl"):
            self.rfi_cluster = pickle.load(open(args["project_path"]+args["temp_data"]+"rfi_cluster_class.pkl", 'rb'))
            if self.rfi_cluster.y_est is not None:
                self.page_state = 2
                img = self.rfi_cluster.histogram_show(cluster_label=None, refer_cluster=True)
                pix = img.toqpixmap()
                self.image_2.setPixmap(pix)
            else:
                self.page_state = 1
                img = self.rfi_cluster.histogram_show(cluster_label=None, refer_cluster=False)
                pix = img.toqpixmap()
                self.image_2.setPixmap(pix)

            img = self.rfi_cluster.cluster_show()
            pix = img.toqpixmap()
            self.image_1.setPixmap(pix)
        else:
            self.rfi_cluster = RfiCluster(csv_path=args["rfi_cluster_page"]["csv_path"])

        if os.path.exists(args["project_path"]+args["temp_data"]+"rfi_cut_class.pkl"):
            self.rfi_cut = pickle.load(open(args["project_path"]+args["temp_data"]+"rfi_cut_class.pkl", 'rb'))
            print(self.rfi_cut.get_info())
        else:
            self.rfi_cut = None

    def mousePressEvent(self, event):
        """
        鼠标按下事件
        :param event:
        :return:
        """
        if (self.page_state == 1 or self.page_state == 2) and event.button() == 1:
            xy = event.pos() - QtCore.QPoint(42, 163)  # 返回鼠标坐标 (42,163), (1062,816)
            x = 2.2*(xy.x() / 1062) - 1.1
            y = 2.2*(xy.y() / 816) - 1.1
            y = -y

            if x < -1.1 or x > 1.1 or y < -1.1 or y > 1.1:
                return

            distance = (self.rfi_cluster.X_reduce[:, 0] - x) ** 2 + (self.rfi_cluster.X_reduce[:, 1] - y) ** 2
            if distance.min() < 0.0005:
                index_num = np.where(distance == distance.min())[0][0]
                feature = self.rfi_cluster.rfi_features.iloc[index_num].values
                rfi_f = RfiFeatures(args["project_path"]+args["FAST_path"]+feature[0])
                if self.page_state == 2:
                    label = self.rfi_cluster.y_est[index_num]
                    refer_cluster = True
                else:
                    label = self.rfi_cluster.y_refer[index_num]
                    refer_cluster = False

                img = self.rfi_cluster.histogram_show(cluster_label=label, refer_cluster=refer_cluster)
                pix = img.toqpixmap()
                self.image_2.setPixmap(pix)

                img = rfi_f.feature_rfi_show(rfi_feature=feature,
                                             edge_size=args["rfi_cluster_page"]["edge_size"],
                                             label=label,
                                             recount_mask=False)
                pix = img.toqpixmap()
                self.image_3.setPixmap(pix)
                QtWidgets.QApplication.processEvents()

            if self.pb_rfi_cut.text() == "保存配置":

                button = QtWidgets.QMessageBox.warning(self, "提示",
                                             "是否对%d类别进行剔除?"%label,
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                             QtWidgets.QMessageBox.No)
                if button == QtWidgets.QMessageBox.Yes:
                    self.cut_list.append(label)

    def _pb_return_action(self):
        self.Stack.setCurrentIndex(0)

    def _pb_set_action(self):
        self.setting_page = SettingsPage()
        self.setting_page.show()

    def _pb_rfi_reduction_action(self):
        self.Stack.setCurrentIndex(3)
        QtWidgets.QApplication.processEvents()

        if self.rfi_cluster.csv_path != args["rfi_cluster_page"]["csv_path"] \
                or self.rfi_cluster.sample_num != args["rfi_cluster_page"]["sample_num"] \
                or (self.rfi_cut is not None and self.rfi_cut.get_info() != self.rfi_cluster.cut_info):

            if args["rfi_cluster_page"]["rfi_cut"]:
                rfi_cut = self.rfi_cut
            else:
                rfi_cut = None
            self.rfi_cluster.init(csv_path=args["rfi_cluster_page"]["csv_path"],
                            rfi_cut=rfi_cut,
                            sample_num=args["rfi_cluster_page"]["sample_num"])
            self.rfi_cluster.dim_reduction(perplexity=args["rfi_cluster_page"]["tsne_perplexity"])

        if self.rfi_cluster.tsne_perplexity != args["rfi_cluster_page"]["tsne_perplexity"]:
            self.rfi_cluster.dim_reduction(perplexity=args["rfi_cluster_page"]["tsne_perplexity"])

        img = self.rfi_cluster.cluster_show(show_est_label=False)
        pix = img.toqpixmap()
        self.image_1.setPixmap(pix)

        img = self.rfi_cluster.histogram_show(cluster_label=None, refer_cluster=False)
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)

        pickle.dump(self.rfi_cluster, open(args["project_path"]+args["temp_data"]+'rfi_cluster_class.pkl', 'wb'))

        self.page_state = 1
        self.image_2.setVisible(True)
        self.image_3.setVisible(False)
        self.Stack.setCurrentIndex(2)
        QtWidgets.QApplication.processEvents()
        pass

    def _pb_rfi_cluster_action(self):

        self.Stack.setCurrentIndex(3)
        QtWidgets.QApplication.processEvents()

        if self.rfi_cluster.csv_path != args["rfi_cluster_page"]["csv_path"] \
                or self.rfi_cluster.sample_num != args["rfi_cluster_page"]["sample_num"] \
                or (self.rfi_cut is not None and self.rfi_cut.get_info() != self.rfi_cluster.cut_info):

            if args["rfi_cluster_page"]["rfi_cut"]:
                rfi_cut = self.rfi_cut
            else:
                rfi_cut = None
            self.rfi_cluster.init(csv_path=args["rfi_cluster_page"]["csv_path"],
                                  rfi_cut=rfi_cut,
                                  sample_num=args["rfi_cluster_page"]["sample_num"])

            self.rfi_cluster.dim_reduction(perplexity=args["rfi_cluster_page"]["tsne_perplexity"])


        if args["rfi_cluster_page"]["cluster_mode"] == 1:
            cluster_mode = "AgglomerativeClustering"
        elif args["rfi_cluster_page"]["cluster_mode"] == 2:
            cluster_mode = "KMeans"
        elif args["rfi_cluster_page"]["cluster_mode"] == 3:
            cluster_mode = "GaussianMixture"

        if args["rfi_cluster_page"]["cluster_kwargs"] == "None":
            cluster_kwargs = {}
        else:
            cluster_kwargs = dict(s.split("=") for s in args["rfi_detect_page"]["cluster_kwargs"].split("|"))

        self.rfi_cluster.rfi_cluster(n_clusters=args["rfi_cluster_page"]["n_clusters"],
                               cluster_mode=cluster_mode,
                               **cluster_kwargs)


        img = self.rfi_cluster.cluster_show(show_est_label=True)
        pix = img.toqpixmap()
        self.image_1.setPixmap(pix)

        img = self.rfi_cluster.histogram_show(cluster_label=None, refer_cluster=True)
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)

        pickle.dump(self.rfi_cluster, open(args["project_path"] + args["temp_data"] + 'rfi_cluster_class.pkl', 'wb'))

        self.page_state = 2
        self.image_2.setVisible(True)
        self.image_3.setVisible(False)
        self.Stack.setCurrentIndex(2)
        QtWidgets.QApplication.processEvents()

    def _pb_display_switch_action(self):

        if self.image_2.isVisible():
            self.image_2.setVisible(False)
            self.image_3.setVisible(True)
        else:
            self.image_2.setVisible(True)
            self.image_3.setVisible(False)


    def _pb_save_result_action(self):
        absolute_path = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择保存路径", ".")
        if absolute_path == "":
            return

        if self.page_state == 0:
            QtWidgets.QMessageBox.information(self, "错误", "请先运行模型!")
        else:
            absolute_path = absolute_path + "/"
            if self.image_1.pixmap() is not None:
                image_1 = self.image_1.pixmap().toImage()
                image_1.save(absolute_path + "rfi_cluster_image1.png")
            if self.image_2.pixmap() is not None:
                image_2 = self.image_2.pixmap().toImage()
                image_2.save(absolute_path + "rfi_cluster_image2.png")
            if self.image_3.pixmap() is not None:
                image_3 = self.image_3.pixmap().toImage()
                image_3.save(absolute_path + "rfi_cluster_image3.png")

            pickle.dump(self.rfi_cluster, open(absolute_path + 'rfi_cluster_class.pkl', 'wb'))
            if self.rfi_cut is not None:
                pickle.dump(self.rfi_cut, open(absolute_path + 'rfi_cut_class.pkl', 'wb'))
            QtWidgets.QMessageBox.information(self, "提示", "保存成功!")

    def _pb_rfi_cut_action(self):

        if self.pb_rfi_cut.text() == "类别剔除":
            if self.page_state != 2:
                QtWidgets.QMessageBox.information(self, "提示", "请先进行聚类分析!")
                return
            self.pb_rfi_cut.setText("保存配置")
            self.cut_list = []
            self.pb_rfi_reduction.setDisabled(True)
            self.pb_rfi_cluster.setDisabled(True)
        else:
            if self.rfi_cut is None:
                self.rfi_cut = RfiCut(self.rfi_cluster.standard)

            self.cut_list = list(set(self.cut_list))

            button = QtWidgets.QMessageBox.warning(self, "提示",
                                                   "是否对%s类别进行剔除?" % str(self.cut_list),
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if button == QtWidgets.QMessageBox.Yes:

                self.rfi_cut.add_cut(self.rfi_cluster.X_std, self.rfi_cluster.y_est, self.cut_list)
                self.rfi_cluster.cut_label(cut_list=self.cut_list,
                                           refer_cluster=True)

                img = self.rfi_cluster.cluster_show(show_est_label=True)
                pix = img.toqpixmap()
                self.image_1.setPixmap(pix)
                img = self.rfi_cluster.histogram_show(cluster_label=None, refer_cluster=True)
                pix = img.toqpixmap()
                self.image_2.setPixmap(pix)
                pickle.dump(self.rfi_cluster,
                            open(args["project_path"] + args["temp_data"] + 'rfi_cluster_class.pkl', 'wb'))
                pickle.dump(self.rfi_cut,
                            open(args["project_path"] + args["temp_data"] + 'rfi_cut_class.pkl', 'wb'))

            self.pb_rfi_cut.setText("类别剔除")
            self.pb_rfi_reduction.setDisabled(False)
            self.pb_rfi_cluster.setDisabled(False)





