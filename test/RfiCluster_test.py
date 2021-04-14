from core.RfiCluster import RfiCluster
import pickle

rfi_c = RfiCluster(csv_path="./rfi_feature_data_ok.csv", sample=10000)
rfi_c.rfi_features.to_csv("./rfi_feature_data_10000.csv", index=False)

X_reduction = rfi_c.dim_reduction(perplexity=250)
pickle.dump(X_reduction, open('./X_reduction_10000.pkl', 'wb'))

labels = rfi_c.rfi_cluster(n_clusters=16,
                          affinity='euclidean',
                          linkage='ward')

pickle.dump(labels, open('./cluster_labels_10000.pkl', 'wb'))
rfi_c.cluster_show(show_est_label=True, save_fig='./')
