"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rfi_features.py

@Time    :  2021.4.9

@Desc    : 提取FAST文件的RFI特征，并显示局部图像信息

"""

import os
import numpy as np
import pandas as pd
import pickle
from astropy.io import fits
from tqdm import tqdm
from skimage import measure
from core.mitigation import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from core.utils import fig2data

# 读取数据header
class FastData:

    def __init__(self, fast_path):
        """
        读取fast文件
        :param fast_path: fast文件路径
        """

        hdu = fits.open(fast_path)
        self.FAST_NAME = fast_path.split('/')[-1]   # 文件名
        self.DATA = hdu[1].data['DATA']             # 所有测量数据
        self.NAXIS2 = hdu[1].header['NAXIS2']       # 数据块数量(每个数据块时间轴是连续的)
        self.NSBLK = hdu[1].header['NSBLK']         # 一个数据块的时间采集量(即矩阵宽)
        self.NPOL = hdu[1].header['NPOL']           # 极化数(我们默认选择第二个)
        self.NCHAN = hdu[1].header['NCHAN']         # 一个数据块频率通道数(即矩阵高)
        self.TBIN = hdu[1].header['TBIN']           # 采样时间间隔
        self.DAT_FREQ = hdu[1].data["DAT_FREQ"][0][::-1]  # 频率数据


    def get_data(self, block_num, npol_num):
        """
        获取数据
        :param block_num: 数据块编号
        :param npol_num: 极化数
        :return: data
        """
        return self.DATA[block_num, :, npol_num, :, 0].T[::-1]

    def print_parameter(self):
        """
        打印所有参数
        :return:
        """
        print("--------------------")
        print("NAXIS2:", self.NAXIS2)
        print("NSBLK:", self.NSBLK)
        print("NPOL:", self.NPOL)
        print("NCHAN:", self.NCHAN)
        print("TBIN:", self.TBIN)
        print("DAT_FREQ:", self.DAT_FREQ)
        print("--------------------")




class RfiFeatures:

    def __init__(self, fits_path, mask_mode="arpls_mask", **kwargs):
        """
        提取FAST数据的RFI, 并显示局部图像信息。

        :param fits_path: 输入观测数据文件路径
        :param mask_mode: RFI检测的算法模型
            - 'arpls_mask': ArPRS算法
            - 'st_mask': sum_threshold算法
            - 'template_mask': mitigation模板函数(测试用, 用户可以在core.mitigation自行定义mitigation算法)。
            - 用户也可以直接传入自定义算法函数
        :param kwargs: mask_mode需要的参数

        """
        self.fast_data = FastData(fits_path)
        self.mask_mode_name = mask_mode

        if mask_mode == 'arpls_mask':
            mask_mode = arpls_mask
        elif mask_mode == 'st_mask':
            mask_mode = st_mask
        elif mask_mode == 'template_mask':
            mask_mode = template_mask

        self.mask_mode = mask_mode
        self.mask_kwargs = kwargs

        # 存放临时数据，避免重复处理RFI
        self.block_num = None
        self.npol_num = None
        self.data = None
        self.mask = None
        self.line_mask = None
        self.blob_mask = None
        self.rfi_features = None

    def get_mask(self, block_num, npol_num):
        """
        获取单个数据块的RFI mask矩阵

        :param block_num: 第几个数据块
        :param npol_num: 极化通道 0, 1
        :return:
            data: 原始强度矩阵
            mask: 完整的RFI mask矩阵
            line_mask: 带状RFI mask矩阵
            blob_mask: 点团状RFI mask矩阵
        """

        assert 0 <= block_num < self.fast_data.NAXIS2
        assert 0 <= npol_num < self.fast_data.NPOL

        self.block_num = block_num
        self.npol_num = npol_num
        self.data = self.fast_data.get_data(block_num=block_num, npol_num=npol_num)
        self.mask = self.mask_mode(self.data, **self.mask_kwargs)
        self.line_mask = (self.mask.sum(axis=1) == self.mask.shape[1])
        self.blob_mask = self.mask.copy()
        self.blob_mask[self.line_mask, :] = False

        return self.data, self.mask, self.line_mask, self.blob_mask

    def get_all_mask(self, npol_num=1):
        """
        获取整个数据块的RFI mask矩阵
        :param npol_num: 极化通道
        :return: mask矩阵
        """
        all_mask = np.zeros((self.fast_data.NAXIS2, self.fast_data.NCHAN, self.fast_data.NSBLK), dtype=bool)
        for i in range(self.fast_data.NAXIS2):
        # for i in range(5):
            _, mask, _, _ = self.get_mask(block_num=i, npol_num=npol_num)
            all_mask[i, :, :] = mask
            print(self.fast_data.FAST_NAME, "| nplo_num = %d"%self.npol_num, "| block_num = %d"%self.block_num, "ok!")

        return all_mask

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
            y = self.fast_data.DAT_FREQ[line_group[0]]

            # 频带带宽 & 持续时间
            bandwidth_unit = len(line_group) - 1
            duration_unit = self.fast_data.NSBLK - 1

            if bandwidth_unit > 0:
                noise_type = 4  # 带状噪声
            else:
                noise_type = 3  # 单整行噪声

            bandwidth = self.fast_data.DAT_FREQ[line_group[0]] - self.fast_data.DAT_FREQ[line_group[-1]]
            duration = duration_unit * self.fast_data.TBIN

            # 强度均值和方差
            data_mean = select_data.mean()
            data_var = select_data.var()

            line_features.append([None, None, None, noise_type, x_index, y_index, bandwidth_unit, duration_unit,
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

            x = x_index * self.fast_data.TBIN
            y = self.fast_data.DAT_FREQ[y_index]

            # 频带带宽 & 持续时间
            bandwidth_unit = y_mask_index.max() - y_index
            duration_unit = x_mask_index.max() - x_index

            bandwidth = self.fast_data.DAT_FREQ[y_index] - self.fast_data.DAT_FREQ[y_mask_index.max()]
            duration = duration_unit * self.fast_data.TBIN

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

            blob_features.append([None, None, None, noise_type, x_index, y_index, bandwidth_unit, duration_unit,
                                  x, y, bandwidth, duration, data_mean, data_var])

        return blob_features

    def get_rfi_features(self, npol_num, block_num_list=None, connectivity=1):
        """
        获取整个fits文件的全部RFI特征list
        :param npol_num: 极化通道
        :param block_num_list: 需要提取特征的block_num编号列表
        :param connectivity: 连通方式: 1--4连通算法，2--8连通算法
        :return:
         包含：
            fits_name: fits文件名(None)
            num_block: 数据块编号(None)
            npol_num: 极化通道
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

        rfi_features = []
        if block_num_list is None:
            block_num_list = np.arange(self.fast_data.NAXIS2)

        for block_num in block_num_list:
            data, mask, line_mask, blob_mask = self.get_mask(block_num, npol_num)

            line_feature = self.get_line_feature(data, line_mask)
            blob_feature = self.get_blob_feature(data, blob_mask, connectivity)

            # 合并噪声特征
            feature = np.array(line_feature + blob_feature)

            feature[:, 2] = npol_num
            feature[:, 1] = block_num
            feature[:, 0] = self.fast_data.FAST_NAME
            rfi_features += feature.tolist()
            print(self.fast_data.FAST_NAME, "| nplo_num = %d"%self.npol_num, "| block_num = %d"%self.block_num, "ok!")

        from random import shuffle
        # 打乱顺序
        shuffle(rfi_features)
        self.rfi_features = rfi_features
        return self.rfi_features

    def rfi_show(self, block_num, npol_num, show_mask=0, save_fig=None):
        """
        显示整个数据块图像

        :param block_num: 显示fits文件的数据块的编号
        :param npol_num: 极化通道
        :param show_mask: 是否显示mask
            - 0 不显示mask
            - 1 显示mask
            - 2 显示带状mask
            - 3 显示点状mask
        :param save_fig: 保存图像路径，None不保存
        :return: PIL图像格式
        """
        if self.block_num == block_num and self.npol_num == npol_num:
            data = self.data
            mask = self.mask
            line_mask = self.line_mask
            blob_mask = self.blob_mask
        else:
            data, mask, line_mask, blob_mask = self.get_mask(block_num, npol_num)

        fig, ax = plt.subplots(3, figsize=(10, 8), dpi=110, sharex=True, sharey=True)
        ax[0] = plt.subplot2grid((4, 7), (0, 0), colspan=6, rowspan=3)
        ax[1] = plt.subplot2grid((4, 7), (3, 0), colspan=6)
        ax[2] = plt.subplot2grid((4, 7), (0, 6), rowspan=3)

        if show_mask == 1:
            ax[0].imshow(np.ma.array(data, mask=mask), aspect='auto', cmap='jet')
        elif show_mask == 2:
            line_index = np.where(line_mask)[0]
            line_mask = np.zeros_like(data)
            line_mask[line_index, :] = True
            ax[0].imshow(np.ma.array(data, mask=line_mask), aspect='auto', cmap='jet')
        elif show_mask == 3:
            ax[0].imshow(np.ma.array(data, mask=blob_mask), aspect='auto', cmap='jet')
        else:
            ax[0].imshow(data, aspect='auto', cmap='jet')

        ax[0].set_yticks(np.arange(0, data.shape[0], data.shape[0] // 5))
        ax[0].set_yticklabels(np.round(self.fast_data.DAT_FREQ[np.arange(0, data.shape[0], data.shape[0] // 5)], decimals=2))
        ax[0].set_xticks([])

        ax[0].set_title('RFI Data: %s\nblock=%d, npol=%d' %
                        (self.fast_data.FAST_NAME, block_num, npol_num), size=15)
        ax[0].set_ylabel('Frequency (MHz)', size=15)

        ax[1].plot(data.sum(axis=0), 'k')
        ax[1].set_xlabel('Time', size=15)
        ax[1].set_ylabel('Intensity', size=15)
        ax[1].set_xlim([0, self.fast_data.NSBLK])
        ax[1].set_yticks([])

        ax[2].plot(data.sum(axis=1), self.fast_data.DAT_FREQ, 'k')
        ax[2].set_ylim([self.fast_data.DAT_FREQ[0], self.fast_data.DAT_FREQ[-1]])
        ax[2].set_xlim([0, data.sum(axis=1).mean()*5])
        ax[2].set_xlabel('SED', fontsize=15)
        ax[2].set_xticks([])
        ax[2].set_yticks([])

        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)

        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
            # plt.show()

        return fig2data(fig)

    def part_rfi_show(self, block_num, npol_num, box_center, edge_size=2, save_fig=None):
        """
        显示局部数据块图像

        :param block_num: 显示fits文件的数据块的编号
        :param npol_num: 极化通道
        :param box_center: 显示坐标中心
        :param edge_size: 显示视野
        :param save_fig: 保存图像路径，None不保存
        :return: PIL图像格式
        """
        # 避免重复处理数据
        if self.block_num == block_num and self.npol_num == npol_num:
            data = self.data
            mask = self.mask
        else:
            data, mask, _, _ = self.get_mask(block_num, npol_num)

        if edge_size > 100:
            edge_size = 100

        x_index = box_center[0] - edge_size
        y_index = box_center[1] - edge_size

        if x_index < 0:
            x_index = 0
        elif x_index+2*edge_size > self.fast_data.NSBLK:
            x_index = self.fast_data.NSBLK-2*edge_size
        if y_index < 0:
            y_index = 0
        elif y_index+2*edge_size > self.fast_data.NCHAN:
            y_index = self.fast_data.NCHAN-2*edge_size

        showdata = data[y_index:y_index + 2*edge_size, x_index:x_index + 2*edge_size]
        showmask = mask[y_index:y_index + 2*edge_size, x_index:x_index + 2*edge_size]

        fig = plt.figure(figsize=(10, 8), dpi=128)
        plt.imshow(np.ma.array(showdata, mask=showmask), aspect='auto', cmap='jet')

        # 每个像素填入强度
        if edge_size <= 16:
            for px_x in range(showdata.shape[1]):
                for px_y in range(showdata.shape[0]):
                    plt.text(px_x, px_y, str(showdata[px_y, px_x]), verticalalignment='center',
                             horizontalalignment='center', size=15)

        plt.xlabel('Time', size=15)
        plt.ylabel('Frequency (MHz)', size=15)
        plt.xticks(size=15)
        if edge_size*2 > 5:
            plt.yticks(np.arange(0, edge_size*2, edge_size*2 // 5),
                       np.around(self.fast_data.DAT_FREQ[y_index:y_index + edge_size*2:edge_size*2 // 5], 2), size=15)
        else:
            plt.yticks(np.arange(0, edge_size*2),
                       np.around(self.fast_data.DAT_FREQ[y_index:y_index + edge_size*2], 2), size=15)

        plt.title('Partial Data: %s\nblock=%d,npol=%d,box_center=[%d,%d],view_size=%d'%
                  (self.fast_data.FAST_NAME, block_num, npol_num, box_center[0], box_center[1], edge_size), size=15)
        plt.tight_layout()

        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
        #     plt.show()
        return fig2data(fig)


    def feature_rfi_show(self, rfi_feature, edge_size=2, recount_mask=True, label=None ,save_fig=None):
        """
        显示单个RFI特征的局部图像

        :param rfi_feature: 需要显示的rfi特征
        :param edge_size: 局部显示边框
        :param recount_mask: 是否重新计算mask，False可以减少计算量只显示局部框，True还显示RFI mask
        :param save_fig: 保存图像路径，None不保存
        :param label: 聚类标签号
        :return: PIL图像格式
        """
        # 显示局部上限扩展尺寸
        edge_left = edge_size
        edge_right = edge_size
        edge_up = edge_size
        edge_down = edge_size

        # 需要用到的几个值
        fitsname = rfi_feature[0]
        block_num = rfi_feature[1]
        npol_num = rfi_feature[2]

        x_index = rfi_feature[4]
        y_index = rfi_feature[5]
        bandwidth_unit = rfi_feature[6] + 1
        duration_unit = rfi_feature[7] + 1
        y = rfi_feature[9]
        bandwidth = rfi_feature[10]
        data_mean = rfi_feature[-2]
        data_var = rfi_feature[-1]

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

        if show_x + edge_left + duration_unit + edge_right > self.fast_data.NSBLK:
            show_w = self.fast_data.NSBLK - show_x
        else:
            show_w = edge_left + duration_unit + edge_right

        if y_index + edge_up + bandwidth_unit + edge_down > self.fast_data.NCHAN:
            show_h = self.fast_data.NCHAN - show_y
        else:
            show_h = edge_up + bandwidth_unit + edge_down

        fig = plt.figure(figsize=(10, 8), dpi=128)
        if recount_mask == True:

            # 避免重复处理数据
            if self.block_num == block_num and self.npol_num == npol_num:
                data = self.data
                mask = self.mask
            else:
                data, mask, _, _ = self.get_mask(block_num, npol_num)

            showdata = data[show_y:show_y + show_h, show_x:show_x + show_w]
            showmask = mask[show_y:show_y + show_h, show_x:show_x + show_w]
            plt.imshow(np.ma.array(showdata, mask=showmask), aspect='auto', cmap='jet')
        else:
            data = self.fast_data.get_data(block_num, npol_num)
            showdata = data[show_y:show_y + show_h, show_x:show_x + show_w]
            plt.imshow(showdata, aspect='auto', cmap='jet')

        # 在局部图像画出矩形框
        ax = plt.gca()
        rect = patches.Rectangle((edge_left - 0.5, edge_down - 0.5), duration_unit, bandwidth_unit,
                                 linewidth=3, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # 每个像素填入强度
        if show_w <= 32:
            for px_x in range(showdata.shape[1]):
                for px_y in range(showdata.shape[0]):
                    plt.text(px_x, px_y, str(showdata[px_y, px_x]), verticalalignment='center',
                             horizontalalignment='center', size=15)

        plt.xlabel('Time', size=15)
        plt.ylabel('Frequency (MHz)', size=15)
        plt.xticks(size=15)
        if show_h > 5:
            plt.yticks(np.arange(0, show_h, show_h // 5),
                       np.around(self.fast_data.DAT_FREQ[show_y:show_y + show_h:show_h // 5], 2), size=15)
        else:
            plt.yticks(np.arange(0, show_h),
                       np.around(self.fast_data.DAT_FREQ[show_y:show_y + show_h], 2), size=15)

        if label is not None:
            plt.figtext(0, 0.97, "cluster_label=%d"%label, size=20)

        plt.title('Partial Data: %s\nblock=%d,npol=%d,freq=%.2f,bandwidth=%.2f,d_mean=%.2f,d_var=%.2f' %
                  (fitsname, block_num, npol_num, y, bandwidth, data_mean, data_var), size=15)
        plt.tight_layout()

        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
        #     plt.show()
        return fig2data(fig)

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


def get_rfi_mask(fits_dir, npol_num=1, mask_mode="arpls_mask", **kwargs):
    """
    获取整个目录下所有fits文件的RFI mask数据并保存。(保存在fits_dir/output_data/下)

    :param fits_dir: fits文件路径
    :param npol_num: 极化通道
    :param mask_mode: mask算法
    :param kwargs: mask算法对应参数
    :return: None
    """

    dir_list = os.listdir(fits_dir)
    fits_list = []
    for i in dir_list:
        if os.path.splitext(i)[1] == ".fits":
            fits_list.append(i)

    if not os.path.exists(fits_dir+"output_data"):
        os.makedirs(fits_dir+"output_data")

    for fits_name in tqdm(fits_list):
        rfi_f = RfiFeatures(fits_dir+fits_name, mask_mode, **kwargs)
        mask = rfi_f.get_all_mask(npol_num=npol_num)
        pickle.dump(mask, open(fits_dir + 'output_data/' + fits_name + "_nplo_%d_"%npol_num + mask_mode + ".pkl", 'wb'))



def get_rfi_features(fits_dir, npol_num=1, connectivity=1, mask_mode="arpls_mask", **kwargs):
    """
    获取整个路径下所有fits文件的RFI特征。(保存在fits_dir/output_data/下)

    :param fits_dir: FAST数据路径
    :param npol_num: 极化通道
    :param mask_mode: RFI mask算法模型
    :param connectivity: 连通方式: 1--4连通算法，2--8连通算法
    :param **kwargs: mask算法的对应参数
    :return: 返回一个DataFrame, 包含特征：
        fits_name: fits文件名(None)
        num_block: 数据块编号(None)
        num_nplo: 极化通道
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

    dir_list = os.listdir(fits_dir)
    fits_list = []
    for i in dir_list:
        if os.path.splitext(i)[1] == ".fits":
            fits_list.append(i)

    if not os.path.exists(fits_dir+"output_data"):
        os.makedirs(fits_dir+"output_data")

    cols_name = ["fits_name", "block_num", "npol_num", "noise_type", "x_index", "y_index", "bandwidth_unit", "duration_unit",
                 "x", "y", "bandwidth", "duration", "data_mean", "data_var"]

    for fits_name in tqdm(fits_list):
        rfi_f = RfiFeatures(fits_dir + fits_name, mask_mode, **kwargs)
        rfi_features = np.array(rfi_f.get_rfi_features(npol_num=npol_num,
                                                       block_num_list=None,
                                                       connectivity=connectivity))

        rfi_feature_df = pd.DataFrame(data=rfi_features, columns=cols_name)

        # 修改数据类型
        rfi_feature_df.block_num = rfi_feature_df.block_num.astype(np.int16)
        rfi_feature_df.npol_num = rfi_feature_df.npol_num.astype(np.int16)
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

        rfi_feature_df.to_csv(fits_dir + 'output_data/'+os.path.splitext(fits_name)[0]+"_rfi_feature.csv", index=False)


