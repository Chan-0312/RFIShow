"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RfiFeatures.py

@Time    :  2021.4.9

@Desc    :

"""

import os
import sys
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm
from .ArPRS.mitigation import arpls_mask, st_mask


# 读取数据header
class FastArg():
    def __init__(self, hdu):
        """
        读取fast文件的参数
        :param hdu: 文件头
        """
        self.NAXIS2 = hdu[1].header['NAXIS2']       # 数据块数量(每个数据块时间轴是连续的)
        self.NSBLK = hdu[1].header['NSBLK']         # 一个数据块的时间采集量(即矩阵宽)
        self.NPOL = hdu[1].header['NPOL']           # 极化数(我们默认选择第二个)
        self.NCHAN = hdu[1].header['NCHAN']         # 一个数据块频率通道数(即矩阵高)
        self.TBIN = hdu[1].header['TBIN']           # 采样时间间隔
        self.DAT_FREQ = hdu[1].data["DAT_FREQ"][0]  # 频率数据

    def print(self):
        """
        打印所有参数
        :return:
        """
        print("NAXIS2:", self.NAXIS2)
        print("NSBLK:", self.NSBLK)
        print("NPOL:", self.NPOL)
        print("NCHAN:", self.NCHAN)
        print("TBIN:", self.TBIN)
        print("DAT_FREQ:", self.DAT_FREQ)

class RfiFeatures():

    def __init__(self, file_path):
        """

        :param file_path: FAST文件路径(目前仅支持fits文件格式)
        """

        hdu = fits.open(file_path)

        self.fits_args = FastArg(hdu)
        self.fits_data = hdu[1].data['DATA']

        self.mask = None        # 完整的RFI mask矩阵
        self.line_mask = None   # 带状RFI mask矩阵
        self.blob_mask = None   # 点团状RFI mask矩阵

        self.rfi_line_features = []     # RFI带状特征list
        self.rfi_blob_features = []     # RFI点状特征list

    def get_mask(self, block_num, mask_mode=arpls_mask, **kwargs):
        """
        获取单个数据块的RFI mask矩阵

        :param block_num: 第几个数据块
        :param mask_mode: RFI检测的算法模型
        :param kwargs: mask_mode需要的参数
        :return:
            mask: 完整的RFI mask矩阵
            line_mask: 带状RFI mask矩阵
            blob_mask: 点团状RFI mask矩阵
        """

        assert block_num < self.fits_args.NAXIS2

        data = self.fits_data[block_num, :, 1, :, 0].T[::-1]

        mask, line_mask, blob_mask = mask_mode(data, **kwargs)

        self.mask = mask
        self.line_mask = line_mask
        self.blob_mask = blob_mask

        return mask, line_mask, blob_mask

    def get_line_feature(self):









    def _continuation_merge(mask_list):
        """
        对连续的数据合并成组。
        例如：
            输入：[0,0,1,2,3,5,6,8,8,9]
            返回：[[0,0,1,2,3],[5,6],[8,8,9]

        :param mask_list: 输入序列
        :return: 返回合并序列
        """
        mask_groups = []
        if len(mask_list) > 0:
            group = [mask_list[0]]
            for i in range(1, len(mask_list)):
                if mask_list[i] - mask_list[i - 1] <= 1:
                    group.append(mask_list[i])
                else:
                    mask_groups.append(group)
                    group = [mask_list[i]]
            mask_groups.append(group)
        return mask_groups




