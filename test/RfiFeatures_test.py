from core.RfiFeatures import RfiFeatures

rfi_f = RfiFeatures('../data/FAST_data/G88.94-1.44_snapshot-M18_0001.fits')

data, mask, line_mask, blob_mask = rfi_f.get_mask(block_num=0)

rfi_features = rfi_f.get_rfi_features()
rfi_f.rfi_show(rfi_features[-1], edge_size=10, save_fig='./')
rfi_f.rfi_show(rfi_features[-1], edge_size=3)
