from core.RfiCluster import RfiCluster

rfi_c = RfiCluster(csv_path="./rfi_feature_data_ok.csv", sample=500)

rfi_c.dim_reduction(perplexity=250)
rfi_c.rfi_cluster(n_clusters=16,
                  affinity='euclidean',
                  linkage='ward')
rfi_c.cluster_show(show_cluster_list=[0,1,5], show_est_label=True)
