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


class SettingsPage(QtWidgets.QWidget):

    def __init__(self, insertSignal):
        super(SettingsPage, self).__init__()

        # 继承这个信号
        self.insertSignal = insertSignal

        self.setWindowTitle("参数设置")
        self.setObjectName("SettingsPage")
        self.resize(800, 500)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 10, 800, 50))
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("参数设置")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 80, 20))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("文件设置")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 80, 20, 121))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(780, 80, 20, 121))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(10, 190, 781, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setGeometry(QtCore.QRect(90, 70, 701, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self)
        self.line_5.setGeometry(QtCore.QRect(0, 220, 20, 111))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self)
        self.line_6.setGeometry(QtCore.QRect(10, 320, 781, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 210, 80, 20))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Mask设置")
        self.line_7 = QtWidgets.QFrame(self)
        self.line_7.setGeometry(QtCore.QRect(90, 210, 701, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self)
        self.line_8.setGeometry(QtCore.QRect(780, 220, 20, 111))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 130, 40))
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_4.setText("数据块编号")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 230, 130, 40))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setText("Mask算法")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 280, 130, 40))
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setText("算法参数")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(20, 340, 80, 20))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7.setText("Show设置")
        self.line_9 = QtWidgets.QFrame(self)
        self.line_9.setGeometry(QtCore.QRect(0, 350, 20, 61))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self)
        self.line_10.setGeometry(QtCore.QRect(90, 340, 701, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self)
        self.line_11.setGeometry(QtCore.QRect(780, 350, 20, 61))
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.line_12 = QtWidgets.QFrame(self)
        self.line_12.setGeometry(QtCore.QRect(10, 400, 781, 16))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")

        self.le_select_fits = QtWidgets.QLineEdit(self)
        self.le_select_fits.setEnabled(False)
        self.le_select_fits.setGeometry(QtCore.QRect(160, 100, 620, 40))
        self.le_select_fits.setFont(font)
        self.le_select_fits.setObjectName("le_select_fits")
        self.pb_select_fits = QtWidgets.QPushButton(self)
        self.pb_select_fits.setGeometry(QtCore.QRect(20, 100, 130, 40))
        self.pb_select_fits.setFont(font)
        self.pb_select_fits.setObjectName("pb_select_fits")
        self.pb_select_fits.setText("文件选择")
        self.sb_block_num = QtWidgets.QSpinBox(self)
        self.sb_block_num.setGeometry(QtCore.QRect(160, 150, 620, 40))
        self.sb_block_num.setFont(font)
        self.sb_block_num.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_block_num.setAccelerated(True)
        self.sb_block_num.setMaximum(255)
        self.sb_block_num.setObjectName("sb_block_num")

        self.le_mask_mode = QtWidgets.QLineEdit(self)
        self.le_mask_mode.setEnabled(True)
        self.le_mask_mode.setGeometry(QtCore.QRect(160, 230, 620, 40))
        self.le_mask_mode.setObjectName("cob_mask_mode")
        self.le_mask_mode.setFont(font)
        self.le_mask_mode.setText("arpls_mask")

        self.le_mask_kwargs = QtWidgets.QLineEdit(self)
        self.le_mask_kwargs.setEnabled(True)
        self.le_mask_kwargs.setGeometry(QtCore.QRect(160, 280, 620, 40))
        self.le_mask_kwargs.setFont(font)
        self.le_mask_kwargs.setObjectName("le_mask_kwargs")

        self.chb_show_mask = QtWidgets.QCheckBox(self)
        self.chb_show_mask.setGeometry(QtCore.QRect(20, 360, 130, 40))
        self.chb_show_mask.setFont(font)
        self.chb_show_mask.setObjectName("chb_show_mask")
        self.chb_show_mask.setText("是否显示Mask")

        self.chb_show_other = QtWidgets.QCheckBox(self)
        self.chb_show_other.setGeometry(QtCore.QRect(200, 360, 130, 40))
        self.chb_show_other.setFont(font)
        self.chb_show_other.setObjectName("chb_show_other")
        self.chb_show_other.setText("是否显示其他")

        self.pb_confirm = QtWidgets.QPushButton(self)
        self.pb_confirm.setGeometry(QtCore.QRect(10, 420, 781, 71))
        font.setPointSize(24)
        self.pb_confirm.setFont(font)
        self.pb_confirm.setObjectName("pb_confirm")
        self.pb_confirm.setText("确定")

        self.pb_select_fits.clicked.connect(self._pb_select_fits_action)
        self.pb_confirm.clicked.connect(self._pb_confirm_action)

        self.retranslateUi()

    def retranslateUi(self):
        rfishow_page_args = args["rfishow_page"]
        self.le_select_fits.setText(rfishow_page_args["fits_path"])
        self.le_mask_mode.setText(rfishow_page_args["mask_mode"])
        self.le_mask_kwargs.setText(rfishow_page_args["mask_kwargs"])
        self.sb_block_num.setValue(rfishow_page_args["block_num"])
        self.chb_show_mask.setChecked(rfishow_page_args["show_mask"])
        self.chb_show_other.setChecked(rfishow_page_args["show_other"])

    def _pb_select_fits_action(self):
        absolute_path = QtWidgets.QFileDialog.getOpenFileName(self, '请选择fits文件',
                                                    '.', "fits files (*.fits)")
        self.le_select_fits.setText(absolute_path[0])

    def _pb_confirm_action(self):
        args["rfishow_page"]["fits_path"] = self.le_select_fits.text()
        args["rfishow_page"]["mask_mode"] = self.le_mask_mode.text()
        args["rfishow_page"]["mask_kwargs"] = self.le_mask_kwargs.text()
        args["rfishow_page"]["block_num"] = self.sb_block_num.value()
        args["rfishow_page"]["show_mask"] = self.chb_show_mask.isChecked()
        args["rfishow_page"]["show_other"] = self.chb_show_other.isChecked()

        # 保存环境参数
        save_sttings(args, args["save_dict_list"])
        # print(args["rfishow_page"])
        # 相当于调用RfishowPage._show_image()
        self.close()
        self.insertSignal.emit()


class RfiDetectPage(QtWidgets.QWidget):
    insertSignal = QtCore.pyqtSignal()
    def __init__(self, Stack):

        super(RfiDetectPage, self).__init__()

        # 获取Stack类
        self.Stack = Stack

        self.setGeometry(0, 0, 1920, 1024)
        self.setObjectName('RfiDetectPage')

        font = QtGui.QFont()
        font.setFamily("Arial")

        self.lb_title = QtWidgets.QLabel(self)
        self.lb_title.setText("RFI检测")
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
        self.image_2.setGeometry(QtCore.QRect(1140, 120, 550, 440))
        self.image_2.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_2.setAlignment(QtCore.Qt.AlignCenter)
        self.image_2.setObjectName("image_2")
        self.image_2.setScaledContents(True)

        self.image_3 = QtWidgets.QLabel(self)
        self.image_3.setGeometry(QtCore.QRect(1140, 560, 550, 440))
        self.image_3.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.image_3.setAlignment(QtCore.Qt.AlignCenter)
        self.image_3.setObjectName("image_3")
        self.image_3.setScaledContents(True)

        self.pb_set = QtWidgets.QPushButton(self)
        self.pb_set.setGeometry(QtCore.QRect(1720, 120, 150, 80))
        self.pb_set.setFont(font)
        self.pb_set.setText("参数设置")
        self.pb_set.setObjectName("pb_set")

        self.pb_save_result = QtWidgets.QPushButton(self)
        self.pb_save_result.setGeometry(QtCore.QRect(1720, 220, 150, 80))
        self.pb_save_result.setFont(font)
        self.pb_save_result.setText("保存结果")
        self.pb_save_result.setObjectName("pb_save_result")

        self.pb_batch_deal = QtWidgets.QPushButton(self)
        self.pb_batch_deal.setGeometry(QtCore.QRect(1720, 320, 150, 80))
        self.pb_batch_deal.setFont(font)
        self.pb_batch_deal.setText("批量处理")
        self.pb_batch_deal.setObjectName("pb_batch_deal")

        self.pb_return.clicked.connect(self._pb_return_action)
        self.pb_set.clicked.connect(self._pb_set_action)
        self.pb_save_result.clicked.connect(self._pb_save_result_action)
        self.pb_batch_deal.clicked.connect(self._pb_batch_deal_action)

        self.insertSignal.connect(self._show_image)


        if args["rfishow_page"]["mask_kwargs"] == "None":
            mask_kwargs = {}
        else:
            mask_kwargs = dict(s.split("=") for s in args["rfishow_page"]["mask_kwargs"].split("|"))

        self.rfi_f = RfiFeatures(args["rfishow_page"]["fits_path"],
                                 args["rfishow_page"]["mask_mode"],
                                 **mask_kwargs)

    def _pb_return_action(self):
        self.Stack.setCurrentIndex(0)

    def _pb_set_action(self):
        self.setting_page = SettingsPage(self.insertSignal)
        self.setting_page.show()

    def _pb_save_result_action(self):
        absolute_path = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择保存路径", ".")
        if absolute_path == "":
            return

        if self.rfi_f.mask is None:
            QtWidgets.QMessageBox.information(self, "错误", "请先设置参数!")
        else:
            image_1 = self.image_1.pixmap().toImage()
            image_2 = self.image_2.pixmap().toImage()
            image_3 = self.image_3.pixmap().toImage()
            absolute_path = absolute_path + "/" + args["rfishow_page"]["fits_path"].split("/")[-1] + "_" + str(args["rfishow_page"]["block_num"])
            image_1.save(absolute_path + "_1.png")
            image_2.save(absolute_path + "_2.png")
            image_3.save(absolute_path + "_3.png")
            pickle.dump(self.rfi_f.mask, open(absolute_path + "_mask.pkl", 'wb'))
            QtWidgets.QMessageBox.information(self, "提示", "保存成功!")


    def _pb_batch_deal_action(self):
        absolute_path = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择数据路径", ".")
        if absolute_path == "":
            return
        reply = QtWidgets.QMessageBox.information(self, "提示", "是否保存图片数据?",
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            save_image_flag = True
        else:
            save_image_flag = False
            
        # print(absolute_path, save_image_flag)




    def _show_image(self):
        self.Stack.setCurrentIndex(4)
        QtWidgets.QApplication.processEvents()

        if args["rfishow_page"]["show_mask"] == False:
            show_mask = 0
        else:
            show_mask = 1

        if args["rfishow_page"]["mask_kwargs"] == "None":
            mask_kwargs = {}
        else:
            mask_kwargs = dict(s.split("=") for s in args["rfishow_page"]["mask_kwargs"].split("|"))

        # 这里有bug,输入的参数全部是字符串
        if self.rfi_f.fits_path != args["rfishow_page"]["fits_path"] or self.rfi_f.mask_mode_name != args["rfishow_page"]["mask_mode"] or self.rfi_f.mask_kwargs != mask_kwargs:
            self.rfi_f = RfiFeatures(args["rfishow_page"]["fits_path"],
                                     args["rfishow_page"]["mask_mode"],
                                     **mask_kwargs)

        img = self.rfi_f.rfi_show(args["rfishow_page"]["block_num"],
                            show_mask=show_mask,
                            show_other=args["rfishow_page"]["show_other"],
                            save_fig=None)
        pix = img.toqpixmap()
        self.image_1.setPixmap(pix)

        img = self.rfi_f.rfi_show(args["rfishow_page"]["block_num"],
                            show_mask=2,
                            show_other=False,
                            save_fig=None)
        pix = img.toqpixmap()
        self.image_2.setPixmap(pix)

        img = self.rfi_f.rfi_show(args["rfishow_page"]["block_num"],
                            show_mask=3,
                            show_other=False,
                            save_fig=None)
        pix = img.toqpixmap()
        self.image_3.setPixmap(pix)

        self.Stack.setCurrentIndex(1)
        QtWidgets.QApplication.processEvents()

