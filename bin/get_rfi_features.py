"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  get_rfi_features.py

@Time    :  2021.4.23

@Desc    : 批量获取RFI特征

"""

import sys
sys.path.append('..')
from core import get_rfi_features
from conf import args


if __name__ == '__main__':
    """
    批量获取RFI特征, mask模型参数参考rfishow.cfg, 结果数据保存在fits_dir/output_data/下
    
    :param fits_dir: fits文件路径
    """
    assert len(sys.argv) == 3, "Usage：python get_rfi_features.py fits_dir csv_name"

    # 读取参数
    fits_dir = sys.argv[1]
    csv_name = sys.argv[2]

    if args["rfishow_page"]["mask_kwargs"] == "None":
        mask_kwargs = {}
    else:
        mask_kwargs = dict(s.split("=") for s in args["rfishow_page"]["mask_kwargs"].split("|"))

    get_rfi_features(fits_dir,
                     npol_num=args["rfishow_page"]["npol_num"],
                     connectivity=args["rfishow_page"]["connectivity"],
                     mask_mode=args["rfishow_page"]["mask_mode"],
                     save_csv_name=csv_name,
                     **mask_kwargs)

