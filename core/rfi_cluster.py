"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rfi_cluster.py

@Time    :  2021.4.11

@Desc    : 对提取的RFI特征进行聚类分析

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KNeighborsClassifier


from core.utils import fig2data



class RfiCut:

    def __init__(self, standard):

        self.knn_list = []
        self.C_list = []
        self.cut_info = []
        self.standard = standard

    def add_cut(self, X, Y, C, n_neighbors=5):
        knn_model = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, Y)
        self.knn_list.append(knn_model)
        self.C_list.append(C)
        self.cut_info.append(C)

    def cut(self, rfi_features):

        X_input = self.standard.transform(rfi_features[['y', 'bandwidth', 'duration', 'data_mean', 'data_var']].values)

        for knn, C in zip(self.knn_list, self.C_list):

            y_pred = knn.predict(X_input)

            cut_index = set()
            for c in C:
                cut_index = cut_index | set(np.where(y_pred == c)[0])

            cut_index = list(cut_index)

            rfi_features = rfi_features.drop(rfi_features.index[cut_index])
            rfi_features.reset_index(drop=True, inplace=True)

        return rfi_features

    def get_info(self):

        return self.cut_info



class RfiCluster:

    def __init__(self, csv_path):
        """
        对RFI进行降维，聚类可视化

         :param csv_path: RFI特征csv文件路径
        """
        self.init(csv_path=csv_path,
                  rfi_cut=None,
                  sample_num=500)

    def init(self, csv_path, rfi_cut=None, sample_num=None):
        """
        对RfiCluster类进行初始化

        :param csv_path: RFI特征csv文件路径
        :param rfi_cut: rfi样本剔除类
        :param sample_num: 分析样本数量
        """
        self.csv_path = csv_path
        self.random_state = 123
        self.rfi_features = pd.read_csv(csv_path)
        self.standard = StandardScaler().fit(self.rfi_features[['y', 'bandwidth', 'duration', 'data_mean', 'data_var']].values)
        self.sample_num = sample_num
        self.cut_info = []

        # 根据knn剔除rfi
        if rfi_cut is not None:
            self.cut_info = rfi_cut.get_info()
            print("cut_info:\n", self.cut_info)
            self.standard = rfi_cut.standard
            self.rfi_features = rfi_cut.cut(self.rfi_features)
            del rfi_cut

        # 随机采样
        if self.sample_num is not None and self.rfi_features.shape[0] > self.sample_num > 0:
            self.rfi_features = self.rfi_features.sample(n=self.sample_num, random_state=self.random_state)

        self.X = self.rfi_features[['y', 'bandwidth', 'duration', 'data_mean', 'data_var']].values
        self.X_std = self.standard.transform(self.X)
        self.y_refer = self.rfi_features['noise_type'].values

        self.X_reduce = None
        self.y_est = None
        self.n_clusters = np.unique(self.y_refer).shape[0]
        self.tsne_perplexity = None
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
        self.tsne_perplexity = perplexity
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
            - 'DBSCAN': DBSCAN算法
            - 用户也可以直接传入自定义算法函数
        :param kwargs: cluster_mode聚类方法的参数
        :return: 聚类标签
        """
        self.cluster_name = cluster_mode

        if cluster_mode == "AgglomerativeClustering":
            mode = AgglomerativeClustering(n_clusters=n_clusters,
                                           **kwargs)
        elif cluster_mode == "KMeans":
            mode = KMeans(n_clusters=n_clusters,
                          random_state = self.random_state,
                          **kwargs)
        elif cluster_mode == "GaussianMixture":
            mode = GaussianMixture(n_components=n_clusters,
                                   random_state=self.random_state,
                                   **kwargs)
        elif cluster_mode == "DBSCAN":
            mode = DBSCAN(**kwargs)
        else:
            mode = cluster_mode(n_clusters=n_clusters,
                                **kwargs)

        self.n_clusters = n_clusters
        self.y_est = mode.fit_predict(self.X_std)

        return self.y_est

    def cut_label(self, cut_list, refer_cluster=False):

        if refer_cluster and self.y_est is not None:
            y = self.y_est
        else:
            y = self.y_refer

        cut_index = set()
        for c in cut_list:
            cut_index = cut_index | set(np.where(y == c)[0])

        cut_index = list(cut_index)

        self.rfi_features = self.rfi_features.drop(self.rfi_features.index[cut_index])
        self.rfi_features.reset_index(drop=True, inplace=True)

        self.X = np.delete(self.X, cut_index, axis=0)
        self.X_std = np.delete(self.X_std, cut_index, axis=0)
        self.y_refer = np.delete(self.y_refer, cut_index, axis=0)

        if self.y_est is not None:
            self.y_est = np.delete(self.y_est, cut_index, axis=0)
        if self.X_reduce is not None:
            self.X_reduce = np.delete(self.X_reduce, cut_index, axis=0)
        self.n_clusters = np.unique(self.y_refer).shape[0]




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

        if cluster_name == "None":
            n_clusters = np.unique(y).shape[0]
        else:
            n_clusters = self.n_clusters

        plt.title('tsne_perplexity=%d,cluster_model=%s,n_clusters=%d'%
                  (self.tsne_perplexity, cluster_name, n_clusters), size=15)
        plt.xlim([-1.1, 1.1])
        plt.ylim([-1.1, 1.1])
        plt.xticks([])
        plt.yticks([])
        # plt.xlabel('Dim_1', size=15)
        # plt.ylabel('Dim_2', size=15)
        plt.tight_layout()

        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
        #     plt.show()
        return fig2data(fig)

    def histogram_show(self, cluster_label=None, refer_cluster=False, save_fig=None):
        """

        :param cluster_label: 统计分析的标签号,如果为None则统计分析全部数据
        :param refer_cluster: 标签参考的对象，True表示参考聚类后的标签，False表示参考原始标签
        :param save_fig: 保存图像路径，None不保存
        :return: PIL图像格式
        """
        # 显示图像尺寸
        fig = plt.figure(figsize=(10, 8), dpi=128)

        if refer_cluster and self.y_est is not None:
            y = self.y_est
        else:
            y = self.y_refer

        if cluster_label is not None:
            index_list = np.where(y==cluster_label)[0]
            rfi_features = self.rfi_features.iloc[index_list]
            fig.suptitle("cluster_label=%d, num_samples=%d"%(cluster_label, len(index_list)), size=15)
        else:
            rfi_features = self.rfi_features
            fig.suptitle("cluster_label=all, num_samples=%d"%(rfi_features.shape[0]), size=15)


        label_name = ['x', 'y', 'bandwidth', 'duration', 'data_mean', 'data_var']
        bins = [50, 50, 50, 50, 50, 50]
        for i in range(6):
            ax = plt.subplot(2, 3, i + 1)
            rfi_features[label_name[i]].hist(histtype='stepfilled', bins=bins[i])
            ax.set_xlabel(label_name[i], fontsize=15)
            if i % 3 == 0:
                ax.set_ylabel('Num.', fontsize=15)

        plt.tight_layout()
        if save_fig is not None:
            plt.savefig(save_fig)
        # else:
        #     plt.show()

        return fig2data(fig)