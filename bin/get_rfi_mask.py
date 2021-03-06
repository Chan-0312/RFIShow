"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  get_rfi_mask.py

@Time    :  2021.4.20

@Desc    : 批量获取RFI mask

"""
import sys
sys.path.append('..')
from core import get_rfi_mask
from conf import args


if __name__ == '__main__':
    """
    批量处理RFI maks, mask模型参数参考rfishow.cfg, 结果数据保存在fits_dir/output_data/下
    
    :param fits_dir: fits文件路径
    """
    assert len(sys.argv) == 2, "Usage：python get_rfi_mask.py fits_dir"

    # 读取参数
    fits_dir = sys.argv[1]

    if args["rfishow_page"]["mask_kwargs"] == "None":
        mask_kwargs = {}
    else:
        mask_kwargs = dict(s.split("=") for s in args["rfishow_page"]["mask_kwargs"].split("|"))

    get_rfi_mask(fits_dir, npol_num=args["rfishow_page"]["npol_num"], mask_mode=args["rfishow_page"]["mask_mode"], **mask_kwargs)








