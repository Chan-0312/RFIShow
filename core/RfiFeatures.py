"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RfiFeatures.py

@Time    :  2021.4.9

@Desc    : 提取FAST文件的RFI特征，并显示局部图像信息

"""

import os
import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm
from skimage import measure
from .ArPRS.mitigation import arpls_mask, st_mask
import matplotlib.pyplot as plt
import matplotlib.patches as patches



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

    def __init__(self, fits_path):
        """
        提取FAST数据的RFI, 并显示局部图像信息。

        :param fits_path: FAST文件路径(目前仅支持fits文件格式)
        """

        hdu = fits.open(fits_path)

        self.fits_path = fits_path
        self.fits_args = FastArg(hdu)
        self.fits_data = hdu[1].data['DATA']

        # 存放临时数据，避免重复处理RFI
        self.block_num = None
        self.data = None
        self.mask = None
        self.line_mask = None
        self.blob_mask = None


    def get_mask(self, block_num, mask_mode=arpls_mask, **kwargs):
        """
        获取单个数据块的RFI mask矩阵

        :param block_num: 第几个数据块
        :param mask_mode: RFI检测的算法模型
        :param kwargs: mask_mode需要的参数
        :return:
            data: 原始强度矩阵
            mask: 完整的RFI mask矩阵
            line_mask: 带状RFI mask矩阵
            blob_mask: 点团状RFI mask矩阵
        """

        assert block_num < self.fits_args.NAXIS2

        data = self.fits_data[block_num, :, 1, :, 0].T[::-1]
        mask, line_mask, blob_mask = mask_mode(data, **kwargs)

        self.block_num = block_num
        self.data = data
        self.mask = mask
        self.line_mask = line_mask
        self.blob_mask = blob_mask

        return data, mask, line_mask, blob_mask

    def get_line_feature(self, data, line_mask):
        """
        提取带状的RFI特征。

        :param data: 强度矩阵
        :param line_mask: 带状RFI mask矩阵
        :return: line_features 线状RFI特征list
        """

        # 存放提取出的RFI条状特征list
        line_features = []
        # 带状噪声的索引
        line_index = np.where(line_mask == True)[0]
        # 将连续的单条状噪声合并成带状噪声
        line_groups = self._continuation_merge(line_index)
        for line_group in line_groups:
            select_data = data[line_group, :]

            # 起始位置
            x_index = 0
            y_index = line_group[0]

            x = 0
            y = self.fits_args.DAT_FREQ[line_group[0]]

            # 频带带宽 & 持续时间
            bandwidth_unit = len(line_group) - 1
            duration_unit = self.fits_args.NSBLK - 1

            if bandwidth_unit > 0:
                noise_type = 4  # 带状噪声
            else:
                noise_type = 3  # 单整行噪声

            bandwidth = self.fits_args.DAT_FREQ[line_group[-1]] - self.fits_args.DAT_FREQ[line_group[0]]
            duration = duration_unit * self.fits_args.TBIN

            # 强度均值和方差
            data_mean = select_data.mean()
            data_var = select_data.var()

            line_features.append([None, None, noise_type, x_index, y_index, bandwidth_unit, duration_unit,
                                  x, y, bandwidth, duration, data_mean, data_var])

        return line_features


    def get_blob_feature(self, data, blob_mask, connectivity=1):
        """
        提取点状的RFI特征。

        :param data: 强度矩阵
        :param blob_mask: 点状RFI mask矩阵
        :param connectivity: 连通方式: 1--4连通算法，2--8连通算法
        :return: blob_features 点状RFI特征list
        """

        # 存放提取出的RFI点状特征list
        blob_features = []

        mask_labels = measure.label(blob_mask,
                                   connectivity=connectivity,
                                   background=False)

        for label in np.unique(mask_labels):
            if label == 0:
                continue
            y_mask_index, x_mask_index = np.where(mask_labels == label)

            select_data = data[y_mask_index, x_mask_index]
            # 起始位置
            x_index = x_mask_index.min()
            y_index = y_mask_index.min()

            x = x_index * self.fits_args.TBIN
            y = self.fits_args.DAT_FREQ[y_index]

            # 频带带宽 & 持续时间
            bandwidth_unit = y_mask_index.max() - y_index
            duration_unit = x_mask_index.max() - x_index

            bandwidth = self.fits_args.DAT_FREQ[y_mask_index.max()] - self.fits_args.DAT_FREQ[y_index]
            duration = duration_unit * self.fits_args.TBIN

            if duration_unit == 0 and bandwidth_unit == 0:
                noise_type = 0  # 单点噪声
            elif duration_unit == 0 and bandwidth_unit > 0:
                noise_type = 1  # 单列竖状噪声
            elif duration_unit > 0 and bandwidth_unit == 0:
                noise_type = 2  # 单行噪声
            else:
                noise_type = 5  # 其他团状噪声

            # 强度均值和方差
            data_mean = select_data.mean()
            data_var = select_data.var()

            blob_features.append([None, None, noise_type, x_index, y_index, bandwidth_unit, duration_unit,
                                  x, y, bandwidth, duration, data_mean, data_var])

        return blob_features

    def get_rfi_features(self):
        """
        获取整个fits文件的全部RFI特征list
        包含：
            fits_name: fits文件名(None)
            num_block: 数据块编号(None)
            noise_type: 噪声类型：
                0 单点状噪声
                1 单列噪声
                2 单行噪声
                3 单整行噪声
                4 带状噪声
                5 其他噪声
            x_index：噪声起始位置x索引
            y_index：噪声起始位置y索引
            bandwidth_unit：噪声宽带，以矩阵采集为单位
            duration_unit：持续时间，以矩阵采集为单位
            x：噪声起始位置,时间点
            y：噪声起始位置，频率
            bandwidth：噪声带宽
            duration：持续时间
            data_mean：噪声强度均值
            data_var：噪声强度方差

        :return:
        """

        rfi_features = []
        for num_block in tqdm(range(self.fits_args.NAXIS2)):
        # for num_block in tqdm(range(3)):
            data, mask, line_mask, blob_mask = self.get_mask(num_block)

            line_feature = self.get_line_feature(data, line_mask)
            blob_feature = self.get_blob_feature(data, blob_mask)

            # 合并噪声特征
            feature = np.array(line_feature + blob_feature)

            feature[:, 1] = num_block
            feature[:, 0] = self.fits_path
            rfi_features += feature.tolist()

        return rfi_features

    def rfi_show(self, block_num, show_mask=True, save_fig=None):
        """
        显示整个数据块图像

        :param block_num: 显示fits文件的数据块的编号
        :param show_mask: 是否显示mask
        :param save_fig: 保存路径(save_fig+rfi_image.png)，None不保存立即显示
        :return: None
        """
        if self.block_num == block_num:
            data = self.data
            mask = self.mask
        else:
            data, mask, _, _ = self.get_mask(block_num)

        plt.figure(figsize=(10, 8), dpi=128)
        if show_mask:
            plt.imshow(np.ma.array(data, mask=mask), aspect='auto', cmap='jet')
        else:
            plt.imshow(data, aspect='auto', cmap='jet')

        plt.yticks(np.arange(0, data.shape[0], data.shape[0] // 5),
                   np.round(self.fits_args.DAT_FREQ[::data.shape[0] // 5][::-1], decimals=2))

        plt.title('RFI Data\n%s,block=%d' %
                  (self.fits_path.split('/')[-1], block_num), size=15)
        plt.xlabel('Time (s)', size=15)
        plt.ylabel('Frequency (MHz)', size=15)
        plt.xticks(size=15)
        plt.tight_layout()

        if save_fig != None:
            plt.savefig(save_fig+'rfi_image.png')
        else:
            plt.show()


    def part_rfi_show(self, rfi_feature, edge_size=2, save_fig=None):
        """
        显示单个RFI特征的局部图像

        :param rfi_feature: 需要显示的rfi特征
        :param edge_size: 局部显示边框
        :param save_fig: 保存路径(save_fig+rfi_feature_image.png)，None不保存立即显示
        :return: None
        """
        # 显示局部上限扩展尺寸
        edge_left = edge_size
        edge_right = edge_size
        edge_up = edge_size
        edge_down = edge_size

        # 需要用到的几个值
        fitsname = rfi_feature[0]
        num_block = rfi_feature[1]
        x_index = rfi_feature[3]
        y_index = rfi_feature[4]
        bandwidth_unit = rfi_feature[5] + 1
        duration_unit = rfi_feature[6] + 1
        y = rfi_feature[8]
        bandwidth = rfi_feature[9]
        data_mean = rfi_feature[-2]
        data_var = rfi_feature[-1]

        # 避免重复处理数据
        if self.fits_path == fitsname and self.block_num == num_block:
            data = self.data
            mask = self.mask
        else:
            data, mask, _, _ = self.get_mask(num_block)

        # 判断边界
        if x_index - edge_left < 0:
            show_x = 0
            edge_left = x_index
        else:
            show_x = x_index - edge_left

        if y_index - edge_up < 0:
            show_y = 0
            edge_up = y_index
        else:
            show_y = y_index - edge_up

        if show_x + edge_left + duration_unit + edge_right > self.fits_args.NSBLK:
            show_w = self.fits_args.NSBLK - show_x
        else:
            show_w = edge_left + duration_unit + edge_right

        if y_index + edge_up + bandwidth_unit + edge_down > self.fits_args.NCHAN:
            show_h = self.fits_args.NCHAN - show_y
        else:
            show_h = edge_up + bandwidth_unit + edge_down

        showdata = data[show_y:show_y + show_h, show_x:show_x + show_w]
        showmask = mask[show_y:show_y + show_h, show_x:show_x + show_w]

        plt.figure(figsize=(10, 8), dpi=128)
        plt.imshow(np.ma.array(showdata, mask=showmask), aspect='auto', cmap='jet')
        # 在局部图像画出矩形框
        ax = plt.gca()
        rect = patches.Rectangle((edge_left - 0.5, edge_down - 0.5), duration_unit, bandwidth_unit,
                                 linewidth=3, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # 每个像素填入强度
        if show_w <= 16 and show_h <= 32:
            for px_x in range(showdata.shape[1]):
                for px_y in range(showdata.shape[0]):
                    plt.text(px_x, px_y, str(showdata[px_y, px_x]), verticalalignment='center',
                             horizontalalignment='center', size=15)

        plt.xlabel('Time', size=15)
        plt.ylabel('Frequency (MHz)', size=15)
        plt.xticks(size=15)
        if show_h > 5:
            plt.yticks(np.arange(0, show_h, show_h // 5),
                       np.around(self.fits_args.DAT_FREQ[show_y:show_y + show_h:show_h // 5][::-1], 2), size=15)
        else:
            plt.yticks(np.arange(0, show_h),
                       np.around(self.fits_args.DAT_FREQ[show_y:show_y + show_h][::-1], 2), size=15)

        plt.title('Partial Data: %s\nblock=%d,freq=%.2f,bandwidth=%.2f,d_mean=%.2f,d_var=%.2f' %
                  (fitsname.split('/')[-1], num_block, y, bandwidth, data_mean, data_var), size=15)
        plt.tight_layout()

        if save_fig != None:
            plt.savefig(save_fig+'rfi_feature_image.png')
        else:
            plt.show()

    def _continuation_merge(self, mask_list):
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


def get_rfi_features(fits_dir):
    """
    获取整个路径下所有fits文件的RFI特征

    :param fits_dir: FAST数据路径
    :return: 返回一个DataFrame, 包含特征：
        fits_name: fits文件名(None)
        num_block: 数据块编号(None)
        noise_type: 噪声类型：
            0 单点状噪声
            1 单列噪声
            2 单行噪声
            3 单整行噪声
            4 带状噪声
            5 其他噪声
        x_index：噪声起始位置x索引
        y_index：噪声起始位置y索引
        bandwidth_unit：噪声宽带，以矩阵采集为单位
        duration_unit：持续时间，以矩阵采集为单位
        x：噪声起始位置,时间点
        y：噪声起始位置，频率
        bandwidth：噪声带宽
        duration：持续时间
        data_mean：噪声强度均值
        data_var：噪声强度方差
    """

    fits_list = os.listdir(fits_dir)

    cols_name = ["fits_name", "num_block", "noise_type", "x_index", "y_index", "bandwidth_unit", "duration_unit",
                 "x", "y", "bandwidth", "duration", "data_mean", "data_var"]

    rfi_feature_df = pd.DataFrame(data=None, columns=cols_name)

    for fits_name in tqdm(fits_list):
        rfi_f = RfiFeatures(fits_dir + fits_name)
        rfi_features = np.array(rfi_f.get_rfi_features())
        rfi_feature_df = rfi_feature_df.append(pd.DataFrame(data=rfi_features, columns= cols_name),
                                               ignore_index=True)

    # 修改数据类型
    rfi_feature_df.num_block = rfi_feature_df.num_block.astype(np.int16)
    rfi_feature_df.noise_type = rfi_feature_df.noise_type.astype(np.int16)
    rfi_feature_df.x_index = rfi_feature_df.x_index.astype(np.int16)
    rfi_feature_df.y_index = rfi_feature_df.y_index.astype(np.int16)
    rfi_feature_df.bandwidth_unit = rfi_feature_df.bandwidth_unit.astype(np.int16)
    rfi_feature_df.duration_unit = rfi_feature_df.duration_unit.astype(np.int16)
    rfi_feature_df.x = rfi_feature_df.x.astype(np.float32)
    rfi_feature_df.y = rfi_feature_df.y.astype(np.float32)
    rfi_feature_df.bandwidth = rfi_feature_df.bandwidth.astype(np.float32)
    rfi_feature_df.duration = rfi_feature_df.duration.astype(np.float32)
    rfi_feature_df.data_mean = rfi_feature_df.data_mean.astype(np.float32)
    rfi_feature_df.data_var = rfi_feature_df.data_var.astype(np.float32)

    rfi_feature_df.to_csv("./rfi_feature_data.csv", index=False)

    return rfi_feature_df