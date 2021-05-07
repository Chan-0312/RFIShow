"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rif_cluster.py

@Time    :  2021.4.11

@Desc    : 对提取的RFI特征进行聚类分析

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture

from core.utils import fig2data


class RfiCluster:

    def __init__(self, csv_path, sample=None):
        """
        对RFI进行降维，聚类可视化

        :param csv_path: RFI特征csv文件路径
        :param sample: 分析样本数量
        """

        self.csv_path = csv_path
        self.random_state = 123
        self.rfi_features = pd.read_csv(csv_path)

        # 随机采样
        if sample is not None and self.rfi_features.shape[0] > sample > 0:
            self.rfi_features = self.rfi_features.sample(n=sample, random_state=self.random_state)

        self.X = self.rfi_features[['y', 'bandwidth', 'duration', 'data_mean', 'data_var']].values
        self.X_std = StandardScaler().fit_transform(self.X)
        self.y_refer = self.rfi_features['noise_type'].values

        self.X_reduce = None
        self.y_est = None
        self.cluster_name = "None"

    def dim_reduction(self, perplexity=250):
        """
        对RFI特征进行TSNE降维

        :param perplexity: 混乱度
        :return: 降维后的数据
        """

        dim_mode = TSNE(n_components=2,
                        perplexity=perplexity,
                        random_state=self.random_state,
                        n_jobs=-1)

        self.X_reduce = dim_mode.fit_transform(self.X_std)
        self.X_reduce = MinMaxScaler().fit_transform(self.X_reduce)*2 - 1
        return self.X_reduce

    def rfi_cluster(self, n_clusters=16, cluster_mode="AgglomerativeClustering", **kwargs):
        """
        对RFI特征进行聚类
        :param n_clusters: 聚类类别数
        :param cluster_mode: 聚类方法，可选参数
            - 'AgglomerativeClustering': AgglomerativeClustering算法
            - 'KMeans': KMeans算法
            - 'GaussianMixture': GaussianMixture
            - 用户也可以直接传入自定义算法函数
        :param kwargs: cluster_mode聚类方法的参数
        :return: 聚类标签
        """
        self.cluster_name = cluster_mode
        if cluster_mode == "AgglomerativeClustering":
            cluster_mode = AgglomerativeClustering
        elif cluster_mode == "KMeans":
            cluster_mode = KMeans
        elif cluster_mode == "GaussianMixture":
            cluster_mode = GaussianMixture

        if self.cluster_name != "AgglomerativeClustering":
            mode = cluster_mode(random_state=self.random_state,
                                **kwargs)
        else:
            mode = cluster_mode(**kwargs)

        self.y_est = mode.fit_predict(self.X_std)

        return self.y_est

    def cluster_show(self, show_cluster_list=None, show_est_label=True, point_size=3, save_fig=None):
        """
        显示聚类结果(降至二维)

        :param show_cluster_list: 显示的聚类的编号，None显示全部
        :param show_est_label: 显示参考标签(False)，还是聚类标签(True)
        :param point_size: 散点绘制大小
        :param save_fig: 保存图像路径，None不保存
        :return: PIL图像格式
        """
        if self.X_reduce is None:
            self.dim_reduction()

        # 显示图像尺寸
        fig = plt.figure(figsize=(10, 8), dpi=128)
        if show_est_label and self.y_est is not None:
            y = self.y_est
            cluster_name = self.cluster_name
        else:
            y = self.y_refer
            cluster_name = "None"

        if show_cluster_list is None:
            show_cluster_list = set(np.unique(y))

        cmap = plt.get_cmap('gnuplot')
        colors = [cmap(i) for i in np.linspace(0, 1, len(show_cluster_list))]
        count = 0
        for i in show_cluster_list:
            if i not in np.unique(y):
                continue
            # plt.text(self.X_reduce[y == i, 0][0], self.X_reduce[y == i, 1][0], '%d' % i, color=colors[count], size=15)
            plt.scatter(self.X_reduce[y == i, 0], self.X_reduce[y == i, 1],
                        color=colors[count], label="num=%d" % i, s=point_size)
            count += 1

        plt.title('Cluster Show\ncluster_model=%s'%cluster_name, size=15)
        # plt.xlim([self.X_reduce[:, 0].min(), self.X_reduce[:, 0].max()])
        # plt.ylim([self.X_reduce[:, 1].min(), self.X_reduce[:, 1].max()])
        plt.xlim([-1.1, 1.1])
        plt.ylim([-1.1, 1.1])
        plt.xlabel('Dim_1', size=15)
        plt.ylabel('Dim_2', size=15)
        plt.tight_layout()

        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
        #     plt.show()
        return fig2data(fig)

    def cluster_save(self, save_csv_name="./rfi_feature_data.csv"):
        """
        保存降维与聚类的结果

        :param save_csv_name: csv文件保存路径
        :return: 对self.rfi_features添加降维数据和聚类标签
        """

        assert self.y_est is not None

        if self.X_reduce is None:
            self.dim_reduction()

        cluster_rfi_features = self.rfi_features.copy(deep=True)
        cluster_rfi_features["Dim_1"] = self.X_reduce[:, 0]
        cluster_rfi_features["Dim_2"] = self.X_reduce[:, 1]
        cluster_rfi_features["cluster_label"] = self.y_est

        cluster_rfi_features.to_csv(save_csv_name, index=False)

        return cluster_rfi_features
