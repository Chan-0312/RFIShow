"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  RfiFeatures_test.py

@Time    :  2021.4.9

@Desc    : 对RfiFeatures.py文件的测试代码

"""

import numpy as np
import matplotlib.pyplot as plt
from core import RfiFeatures, get_rfi_features



rfi_f = RfiFeatures('F:/xscPycharm/RFIShow/data/FAST_data/G88.94-1.44_snapshot-M18_0002.fits', mask_mode="arpls_mask")

# test 1: get_mask ok
data, mask, line_mask, blob_mask = rfi_f.get_mask(block_num=0)
plt.imshow(np.ma.array(data, mask=mask), aspect='auto', cmap='jet')
plt.show()
plt.imshow(np.ma.array(data, mask=blob_mask), aspect='auto', cmap='jet')
plt.show()

# test 2: get_line_feature ok
print(rfi_f.get_line_feature(data=data, line_mask=line_mask))

# test 3: get_blob_feature ok
print(rfi_f.get_blob_feature(data=data, blob_mask=blob_mask, connectivity=1))

# test 4: get_rfi_features ok
# print(rfi_f.get_rfi_features())

# test 5: rfi_show ok
rfi_f.rfi_show(0,show_mask=3)

# test 6: part_rfi_show ok
rfi_features = ['../data/FAST_data/G88.94-1.44_snapshot-M18_0001.fits',0,4,0,141,2,1023,0.0,1017.27295,0.24414062,0.050282497,2.0221355,1.2156558]
rfi_f.part_rfi_show(rfi_features)

# test 7: get_rfi_features ok
# get_rfi_features(fits_dir='F:/xscPycharm/RFIShow/data/FAST_data/')
