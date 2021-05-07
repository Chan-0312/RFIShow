"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rfi_detect_page.py

@Time    :  2021.4.16

@Desc    : rfi可视化界面

"""

from PIL import Image
import pickle
from PyQt5 import QtGui, QtCore, QtWidgets
from conf import args, save_sttings
from core.rfi_features import RfiFeatures

# 特征提取的表格显示数据上限
TABLEVIEW_SIZE = 300

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
        self.label_2.setGeometry(QtCore.QRect(20, 70-50, 80, 20))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("文件设置")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 80-50, 20, 121))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(780, 80-50, 20, 121))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(10, 190-50, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setGeometry(QtCore.QRect(90, 70-50, 701, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self)
        self.line_5.setGeometry(QtCore.QRect(0, 220-50, 20, 111))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self)
        self.line_6.setGeometry(QtCore.QRect(10, 320-50, 781, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 210-50, 120, 20))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("RFI检测设置")
        self.line_7 = QtWidgets.QFrame(self)
        self.line_7.setGeometry(QtCore.QRect(90+40, 210-50, 701, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self)
        self.line_8.setGeometry(QtCore.QRect(780, 220-50, 20, 111))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 150-50, 130, 40))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("数据块编号")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(410, 150-50, 130, 40))
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("极化通道")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 230-50, 130, 40))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setText("Mask算法")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 280-50, 130, 40))
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("算法参数")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(20, 340-50, 80, 20))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("显示设置")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(410, 360 - 50, 130, 40))
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setText("局部视野")
        self.line_9 = QtWidgets.QFrame(self)
        self.line_9.setGeometry(QtCore.QRect(0, 350-50, 20, 61))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self)
        self.line_10.setGeometry(QtCore.QRect(90, 340-50, 701, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self)
        self.line_11.setGeometry(QtCore.QRect(780, 350-50, 20, 61))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.line_12 = QtWidgets.QFrame(self)
        self.line_12.setGeometry(QtCore.QRect(10, 400-50, 781, 16))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")

        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(20, 340 +30, 120, 20))
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setText("特征提取设置")

        self.line_13 = QtWidgets.QFrame(self)
        self.line_13.setGeometry(QtCore.QRect(0, 350+30, 20, 61))
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.line_14 = QtWidgets.QFrame(self)
        self.line_14.setGeometry(QtCore.QRect(90+40, 340+30, 701-40, 20))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.line_15 = QtWidgets.QFrame(self)
        self.line_15.setGeometry(QtCore.QRect(780, 350+30, 20, 61))
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.line_16 = QtWidgets.QFrame(self)
        self.line_16.setGeometry(QtCore.QRect(10, 400+30, 781, 16))
        self.line_16.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")

        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(20, 390, 130, 40))
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setText("特征连通算法")
        self.label_11.setObjectName("label_11")

        self.le_select_fits = QtWidgets.QLineEdit(self)
        self.le_select_fits.setEnabled(False)
        self.le_select_fits.setGeometry(QtCore.QRect(160, 100-50, 620, 40))
        self.le_select_fits.setFont(font)
        self.le_select_fits.setObjectName("le_select_fits")
        self.pb_select_fits = QtWidgets.QPushButton(self)
        self.pb_select_fits.setGeometry(QtCore.QRect(20, 100-50, 130, 40))
        self.pb_select_fits.setFont(font)
        self.pb_select_fits.setObjectName("pb_select_fits")
        self.pb_select_fits.setText("文件选择")
        self.sb_block_num = QtWidgets.QSpinBox(self)
        self.sb_block_num.setGeometry(QtCore.QRect(160, 150-50, 260, 40))
        self.sb_block_num.setFont(font)
        self.sb_block_num.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_block_num.setAccelerated(True)
        self.sb_block_num.setMaximum(255)
        self.sb_block_num.setObjectName("sb_block_num")

        self.sb_npol_num = QtWidgets.QSpinBox(self)
        self.sb_npol_num.setGeometry(QtCore.QRect(520, 150 - 50, 260, 40))
        self.sb_npol_num.setFont(font)
        self.sb_npol_num.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_npol_num.setAccelerated(True)
        self.sb_npol_num.setMaximum(1)
        self.sb_npol_num.setObjectName("sb_npol_num")

        self.sb_edge_size = QtWidgets.QSpinBox(self)
        self.sb_edge_size.setGeometry(QtCore.QRect(520, 360 - 50, 260, 40))
        self.sb_edge_size.setFont(font)
        self.sb_edge_size.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_edge_size.setAccelerated(True)
        self.sb_edge_size.setMaximum(16)
        self.sb_edge_size.setMinimum(2)
        self.sb_edge_size.setSingleStep(2)
        self.sb_edge_size.setObjectName("sb_edge_size")

        self.le_mask_mode = QtWidgets.QLineEdit(self)
        self.le_mask_mode.setEnabled(True)
        self.le_mask_mode.setGeometry(QtCore.QRect(160, 230-50, 620, 40))
        self.le_mask_mode.setObjectName("cob_mask_mode")
        self.le_mask_mode.setFont(font)
        self.le_mask_mode.setText("arpls_mask")

        self.le_mask_kwargs = QtWidgets.QLineEdit(self)
        self.le_mask_kwargs.setEnabled(True)
        self.le_mask_kwargs.setGeometry(QtCore.QRect(160, 280-50, 620, 40))
        self.le_mask_kwargs.setFont(font)
        self.le_mask_kwargs.setObjectName("le_mask_kwargs")

        self.chb_show_line_mask = QtWidgets.QCheckBox(self)
        self.chb_show_line_mask.setGeometry(QtCore.QRect(20, 360-50, 180, 40))
        self.chb_show_line_mask.setFont(font)
        self.chb_show_line_mask.setObjectName("chb_show_line_mask")
        self.chb_show_line_mask.setText("显示带状Mask")

        self.chb_show_blob_mask = QtWidgets.QCheckBox(self)
        self.chb_show_blob_mask.setGeometry(QtCore.QRect(200, 360-50, 180, 40))
        self.chb_show_blob_mask.setFont(font)
        self.chb_show_blob_mask.setObjectName("chb_show_blob_mask")
        self.chb_show_blob_mask.setText("显示点状Mask")

        self.cbb_connectivity = QtWidgets.QComboBox(self)
        self.cbb_connectivity.setGeometry(QtCore.QRect(160, 390, 260, 40))
        self.cbb_connectivity.setFont(font)
        self.cbb_connectivity.setObjectName("cbb_connectivity")
        self.cbb_connectivity.addItem("4连通算法")
        self.cbb_connectivity.addItem("8连通算法")

        self.pb_confirm = QtWidgets.QPushButton(self)
        self.pb_confirm.setGeometry(QtCore.QRect(10, 420+30, 780, 70))
        font.setPointSize(24)
        self.pb_confirm.setFont(font)
        self.pb_confirm.setObjectName("pb_confirm")
        self.pb_confirm.setText("保存")

        self.pb_select_fits.clicked.connect(self._pb_select_fits_action)
        self.pb_confirm.clicked.connect(self._pb_confirm_action)

        self.retranslateUi()

    def retranslateUi(self):
        rfi_detect_page_args = args["rfi_detect_page"]
        self.le_select_fits.setText(rfi_detect_page_args["fits_path"])
        self.le_mask_mode.setText(rfi_detect_page_args["mask_mode"])
        self.le_mask_kwargs.setText(rfi_detect_page_args["mask_kwargs"])
        self.sb_block_num.setValue(rfi_detect_page_args["block_num"])
        self.sb_npol_num.setValue(rfi_detect_page_args["npol_num"])
        self.sb_edge_size.setValue(rfi_detect_page_args["edge_size"])
        self.cbb_connectivity.setCurrentIndex(rfi_detect_page_args["connectivity"]-1)

        if rfi_detect_page_args["show_mask"] == 1:
            self.chb_show_line_mask.setChecked(True)
            self.chb_show_blob_mask.setChecked(True)
        elif rfi_detect_page_args["show_mask"] == 2:
            self.chb_show_line_mask.setChecked(True)
            self.chb_show_blob_mask.setChecked(False)
        elif rfi_detect_page_args["show_mask"] == 3:
            self.chb_show_line_mask.setChecked(False)
            self.chb_show_blob_mask.setChecked(True)
        else:
            self.chb_show_line_mask.setChecked(False)
            self.chb_show_blob_mask.setChecked(False)

    def _pb_select_fits_action(self):
        absolute_path = QtWidgets.QFileDialog.getOpenFileName(self, '请选择fits文件',
                                                    '.', "fits files (*.fits)")
        if absolute_path[0] != "":
            self.le_select_fits.setText(absolute_path[0])

    def _pb_confirm_action(self):
        if self.le_select_fits.text() == "":
            return
        args["rfi_detect_page"]["fits_path"] = self.le_select_fits.text()
        args["rfi_detect_page"]["mask_mode"] = self.le_mask_mode.text()
        args["rfi_detect_page"]["mask_kwargs"] = self.le_mask_kwargs.text()
        args["rfi_detect_page"]["block_num"] = self.sb_block_num.value()
        args["rfi_detect_page"]["npol_num"] = self.sb_npol_num.value()
        args["rfi_detect_page"]["edge_size"] = self.sb_edge_size.value()
        args["rfi_detect_page"]["connectivity"] = self.cbb_connectivity.currentIndex()+1


        if self.chb_show_line_mask.isChecked() and self.chb_show_blob_mask.isChecked():
            show_mask = 1
        elif self.chb_show_line_mask.isChecked() and not self.chb_show_blob_mask.isChecked():
            show_mask = 2
        elif not self.chb_show_line_mask.isChecked() and self.chb_show_blob_mask.isChecked():
            show_mask = 3
        else:
            show_mask = 0
        args["rfi_detect_page"]["show_mask"] = show_mask

        # 保存环境参数
        save_sttings(args, args["save_dict_list"])
        # print(args["rfi_detect_page"])
        # 关闭界面
        self.close()



class RfiDetectPage(QtWidgets.QWidget):
    """
    RFI 检测界面
    """
    def __init__(self, Stack):
        """

        :param Stack: Stack界面类
        """

        super(RfiDetectPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('RfiDetectPage')

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("RFI检测分析")
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

        self.pb_rfi_detect = QtWidgets.QPushButton(self)
        self.pb_rfi_detect.setGeometry(QtCore.QRect(1140, 860, 375, 140))
        self.pb_rfi_detect.setFont(font)
        self.pb_rfi_detect.setText("RFI检测")
        self.pb_rfi_detect.setObjectName("pb_rfi_detect")

        self.pb_get_feature = QtWidgets.QPushButton(self)
        self.pb_get_feature.setGeometry(QtCore.QRect(1515, 860, 375, 140))
        self.pb_get_feature.setFont(font)
        self.pb_get_feature.setText("特征提取")
        self.pb_get_feature.setObjectName("pb_get_feature")

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setGeometry(QtCore.QRect(20, 120, 1100, 880))
        # 设置数据层次结构，4行4列
        self.model = QtGui.QStandardItemModel(TABLEVIEW_SIZE, 7)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['编号','噪声类型','起始频率','噪声带宽','持续时间','强度均值','强度方差'])
        # 自动调整大小尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # 不允许编辑
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 隐藏序号
        self.tableView.verticalHeader().hide()
        # 表头排序
        self.tableView.setSortingEnabled(True)
        # 设置数据
        self.tableView.setModel(self.model)
        # 不显示
        self.tableView.setVisible(False)

        # 信号连接
        self.pb_return.clicked.connect(self._pb_return_action)
        self.pb_set.clicked.connect(self._pb_set_action)
        self.pb_rfi_detect.clicked.connect(self._pb_rfi_detect_action)
        self.pb_save_result.clicked.connect(self._pb_save_result_action)
        self.pb_get_feature.clicked.connect(self._pb_get_feature_action)
        self.tableView.clicked.connect(self._tableView_action)

        # 页面状态
        """
        0 - None
        1 - RFI mask
        2 - RFI features
        """
        self.page_state = 0

        if args["rfi_detect_page"]["mask_kwargs"] == "None":
            mask_kwargs = {}
        else:
            mask_kwargs = dict(s.split("=") for s in args["rfi_detect_page"]["mask_kwargs"].split("|"))

        if args["rfi_detect_page"]["fits_path"] != "":
            self.rfi_f = RfiFeatures(args["rfi_detect_page"]["fits_path"],
                                     args["rfi_detect_page"]["mask_mode"],
                                     **mask_kwargs)
        else:
            self.rfi_f = None


    def mousePressEvent(self, event):
        """
        鼠标按下事件
        :param event:
        :return:
        """
        if self.page_state == 1 and event.button() == 1:
            xy = event.pos() - QtCore.QPoint(140, 191)
            x = int(xy.x() / 827 * 1023)
            y = int(xy.y() / 554 * 4095)
            if x < 0 or x > 1023 or y < 0 or y > 4095:
                return

            img = self.rfi_f.part_rfi_show(block_num=args["rfi_detect_page"]["block_num"],
                                           npol_num=args["rfi_detect_page"]["npol_num"],
                                           box_center=[x, y],
                                           edge_size=args["rfi_detect_page"]["edge_size"],
                                           save_fig=None)
            pix = img.toqpixmap()
            self.image_2.setPixmap(pix)



    def _pb_return_action(self):
        self.Stack.setCurrentIndex(0)

    def _pb_set_action(self):
        self.setting_page = SettingsPage()
        self.setting_page.show()

    def _pb_save_result_action(self):
        absolute_path = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择保存路径", ".")
        if absolute_path == "":
            return

        if self.page_state == 0:
            QtWidgets.QMessageBox.information(self, "错误", "请先运行模型!")
        else:
            absolute_path = absolute_path + "/" + args["rfi_detect_page"]["fits_path"].split("/")[-1] + "_%d_%d"%(args["rfi_detect_page"]["block_num"], args["rfi_detect_page"]["npol_num"])
            if self.image_1.pixmap() is not None:
                image_1 = self.image_1.pixmap().toImage()
                image_1.save(absolute_path + "_image1.png")
            if self.image_2.pixmap() is not None:
                image_2 = self.image_2.pixmap().toImage()
                image_2.save(absolute_path + "_image2.png")
            if self.rfi_f.mask is not None:
                pickle.dump(self.rfi_f.mask, open(absolute_path + "_mask.pkl", 'wb'))
            if self.rfi_f.rfi_features is not None:
                pickle.dump(self.rfi_f.rfi_features, open(absolute_path + "_features.pkl", 'wb'))
            QtWidgets.QMessageBox.information(self, "提示", "保存成功!")

    def _pb_rfi_detect_action(self):
        if self.page_state == 2:
            self.tableView.setVisible(False)
            self.pb_get_feature.setText("特征提取")

        self.Stack.setCurrentIndex(3)
        QtWidgets.QApplication.processEvents()

        if args["rfi_detect_page"]["mask_kwargs"] == "None":
            mask_kwargs = {}
        else:
            mask_kwargs = dict(s.split("=") for s in args["rfi_detect_page"]["mask_kwargs"].split("|"))


        if self.rfi_f is None or self.rfi_f.fast_data.FAST_NAME != args["rfi_detect_page"]["fits_path"] or self.rfi_f.mask_mode_name != args["rfi_detect_page"]["mask_mode"] or self.rfi_f.mask_kwargs != mask_kwargs:
            self.rfi_f = RfiFeatures(args["rfi_detect_page"]["fits_path"],
                                     args["rfi_detect_page"]["mask_mode"],
                                     **mask_kwargs)

        img = self.rfi_f.rfi_show(block_num=args["rfi_detect_page"]["block_num"],
                                  npol_num=args["rfi_detect_page"]["npol_num"],
                                  show_mask=args["rfi_detect_page"]["show_mask"],
                                  save_fig=None)
        pix = img.toqpixmap()
        self.image_1.setPixmap(pix)
        self.page_state = 1
        self.Stack.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()

    def _pb_get_feature_action(self):
        if self.pb_get_feature.text() == "特征提取":
            # 清空数据
            self.model.clear()
            self.model.setHorizontalHeaderLabels(['编号', '噪声类型', '起始频率', '噪声带宽', '持续时间', '强度均值', '强度方差'])

            self.pb_get_feature.setText("结束分析")
            self.Stack.setCurrentIndex(3)
            QtWidgets.QApplication.processEvents()

            if args["rfi_detect_page"]["mask_kwargs"] == "None":
                mask_kwargs = {}
            else:
                mask_kwargs = dict(s.split("=") for s in args["rfi_detect_page"]["mask_kwargs"].split("|"))

            if self.rfi_f is None or self.rfi_f.fast_data.FAST_NAME != args["rfi_detect_page"][
                "fits_path"] or self.rfi_f.mask_mode_name != args["rfi_detect_page"][
                "mask_mode"] or self.rfi_f.mask_kwargs != mask_kwargs:
                self.rfi_f = RfiFeatures(args["rfi_detect_page"]["fits_path"],
                                         args["rfi_detect_page"]["mask_mode"],
                                         **mask_kwargs)

            rfi_features = self.rfi_f.get_rfi_features(npol_num=args["rfi_detect_page"]["npol_num"],
                                                       connectivity=args["rfi_detect_page"]["connectivity"],
                                                       block_num_list=[args["rfi_detect_page"]["block_num"]])
            if len(rfi_features) < TABLEVIEW_SIZE:
                row_len = len(rfi_features)
            else:
                row_len = TABLEVIEW_SIZE
            for row in range(row_len):
                self.model.setItem(row, 0, QtGui.QStandardItem(str(row).zfill(3)))
                for column in range(6):
                    if column == 0:
                        data = str(rfi_features[row][3])
                    else:
                        data = "%.4f"%rfi_features[row][column-6]
                    item = QtGui.QStandardItem(data)
                    # 设置每个位置的文本值
                    self.model.setItem(row, column+1, item)

            self.tableView.setVisible(True)
            self.page_state = 2
            self.Stack.setCurrentIndex(1)
            QtWidgets.QApplication.processEvents()
        else:
            if self.image_1.pixmap() is None:
                self.page_state = 0
            else:
                self.page_state = 1
            self.pb_get_feature.setText("特征提取")
            self.tableView.setVisible(False)



    def _tableView_action(self, clickedIndex):
        """
        点击表格数据
        :param clickedIndex:
        :return:
        """
        row = clickedIndex.row()
        if row > len(self.rfi_f.rfi_features):
            return

        row = int(self.model.index(row, 0).data())
        img = self.rfi_f.feature_rfi_show(self.rfi_f.rfi_features[row],
                                          recount_mask=True,
                                          edge_size=args["rfi_detect_page"]["edge_size"])
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)



