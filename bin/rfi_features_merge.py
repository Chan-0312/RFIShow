"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  rfi_features_merge.py

@Time    :  2021.5.17

@Desc    : 合并RFI特征

"""

import sys
import os
import pandas as pd


if __name__ == '__main__':
    """
    合并rfi特征csv文件

    :param csv_dir: csv文件路径
    """
    assert len(sys.argv) == 2, "Usage：python rfi_features_merge.py csv_dir"

    # 读取参数
    csv_dir = sys.argv[1]

    dir_list = os.listdir(csv_dir)
    cols_name = ["fits_name", "block_num", "npol_num", "noise_type", "x_index", "y_index", "bandwidth_unit",
                 "duration_unit",
                 "x", "y", "bandwidth", "duration", "data_mean", "data_var"]
    rfi_feature_all = pd.DataFrame(data=None, columns=cols_name)
    for csv_name in dir_list:
        if csv_name.split("_")[-1] == "feature.csv":
            df = pd.read_csv(csv_dir+"/"+csv_name)
            rfi_feature_all = rfi_feature_all.append(df)
            print(csv_name, rfi_feature_all.shape)

    rfi_feature_all.to_csv(csv_dir+"/rfi_feature_all.csv",index=False)



