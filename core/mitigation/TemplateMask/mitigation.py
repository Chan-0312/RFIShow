"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  mitigation.py

@Time    :  2021.4.15

@Desc    : RFI提取的模板案例，供参考

"""

import numpy as np

def template_mask(data, **kwargs):
    """
    这个是一个RFI提取的模板，供参考

    :param data: 原始数据
    :param kwargs: 相关参数
    :return: 返回mask矩阵
    """

    print("kwargs:", kwargs)

    return np.full(data.shape, False)

