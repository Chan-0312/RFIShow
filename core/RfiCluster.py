"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RfiCluster_test.py

@Time    :  2021.4.11

@Desc    : 对提取的RFI特征进行聚类分析

"""

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering


class RfiCluster():

    def __init__(self, csv_path, sample=None, random_state=0):
        """
        对RFI进行降维，聚类可视化

        :param csv_path: RFI特征csv文件路径
        :param sample: 分析样本数量
        :param random_state: 随机种子器
        """

        self.csv_path = csv_path
        self.random_state = random_state
        self.rfi_features = pd.read_csv(csv_path)
        if sample != None and sample < self.rfi_features.shape[0] and sample > 0:
            self.rfi_features = self.rfi_features.sample(n=sample, random_state=self.random_state)

        self.X = self.rfi_features[['y', 'bandwidth', 'duration', 'data_mean', 'data_var']].values
        self.X_std = StandardScaler().fit_transform(self.X)
        self.y_refer = self.rfi_features['noise_type'].values
        self.X_reduce = None
        self.y_est = None

    def dim_reduction(self, mode=TSNE, **kwargs):
        """
        对RFI特征进行降维

        :param mode: 降维方法，默认mode
        :param kwargs: mode降维方法的参数
        :return: 降维后的数据
        """

        dim_mode = mode(n_components=2, random_state=self.random_state, **kwargs)

        self.X_reduce = dim_mode.fit_transform(self.X_std)

        return self.X_reduce

    def rfi_cluster(self, mode=AgglomerativeClustering, **kwargs):
        """
        对RFI特征进行聚类

        :param mode: 聚类方法，默认AgglomerativeClustering
        :param kwargs: mode聚类方法的参数
        :return: 聚类标签
        """

        cluster_mode = mode(**kwargs)

        self.y_est = cluster_mode.fit_predict(self.X_std)

        return self.y_est

    def cluster_show(self, show_cluster_list=None, show_est_label=True, save_fig=None):
        """
        显示聚类结果(降至二维)

        :param show_cluster_list: 显示的聚类的编号，None显示全部
        :param show_est_label: 显示参考标签(False)，还是聚类标签(True)
        :param save_fig: 保存路径(save_fig+cluster_image.png)，None不保存立即显示
        :return:
        """
        if self.X_reduce is None:
            self.dim_reduction()

        # 显示图像尺寸
        plt.figure(figsize=(10, 8), dpi=128)
        if show_est_label and self.y_est is not None:
            y = self.y_est
        else:
            y = self.y_refer

        if show_cluster_list is None:
            show_cluster_list = set(np.unique(y))

        cmap = plt.get_cmap('gnuplot')
        colors = [cmap(i) for i in np.linspace(0, 1, len(show_cluster_list))]
        count = 0
        for i in show_cluster_list:
            if i not in np.unique(y):
                continue
            plt.text(self.X_reduce[y == i, 0][0], self.X_reduce[y == i, 1][0], '%d' % i, color=colors[count], size=15)
            plt.scatter(self.X_reduce[y == i, 0], self.X_reduce[y == i, 1],
                        color=colors[count], label="num=%d" % i, s=2.5)
            count += 1

        plt.title('Cluster Show\n', size=15)
        plt.xlabel('Dim_1', size=15)
        plt.ylabel('Dim_2', size=15)
        plt.tight_layout()

        if save_fig != None:
            plt.savefig(save_fig+'cluster_image.png')
        else:
            plt.show()
