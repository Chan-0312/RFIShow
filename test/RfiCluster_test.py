"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RfiCluster_test.py

@Time    :  2021.4.9

@Desc    : 对RfiCluster.py文件的测试代码

"""


from core.rif_cluster import RfiCluster
import pickle

rfi_c = RfiCluster(csv_path="./rfi_feature_data_ok.csv", sample=500)
# rfi_c.rfi_features.to_csv("./rfi_feature_data_10000.csv", index=False)

# test 1: dim_reduction, cluster_show ok
X_reduction = rfi_c.dim_reduction(perplexity=250)
# pickle.dump(X_reduction, open('./X_reduction_10000.pkl', 'wb'))
rfi_c.cluster_show(show_est_label=False, point_size=10)

# test 2: rfi_cluster, cluster_show ok
labels = rfi_c.rfi_cluster(cluster_mode="AgglomerativeClustering",
                           n_clusters=16,
                           affinity='euclidean',
                           linkage='ward')
# pickle.dump(labels, open('./cluster_labels_10000.pkl', 'wb'))
rfi_c.cluster_show(show_est_label=True, save_fig="./cluster_image.png")

labels = rfi_c.rfi_cluster(cluster_mode="KMeans",
                           n_clusters=16,
                           init='k-means++',
                           n_init=10,
                           max_iter=1000)
rfi_c.cluster_show(show_est_label=True)

labels = rfi_c.rfi_cluster(cluster_mode="GaussianMixture",
                           n_components=16,
                           covariance_type='full')
rfi_c.cluster_show(show_est_label=True)




# test 3: rfi_cluster, cluster_show ok
labels = rfi_c.rfi_cluster(cluster_mode="AgglomerativeClustering",
                           n_clusters=16,
                           affinity='euclidean',
                           linkage='ward')
rfi_c.cluster_save("./cluster_rfi_features.csv")


