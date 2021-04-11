from core.RfiFeatures import RfiFeatures, get_rfi_features

rfi_f = RfiFeatures('../data/FAST_data/G88.94-1.44_snapshot-M18_0001.fits')

data, mask, line_mask, blob_mask = rfi_f.get_mask(block_num=0)

# rfi_features = rfi_f.get_rfi_features()

rfi_features = ['../data/FAST_data/G88.94-1.44_snapshot-M18_0001.fits',0,4,0,141,2,1023,0.0,1017.27295,0.24414062,0.050282497,2.0221355,1.2156558]

rfi_f.part_rfi_show(rfi_features, edge_size=10, save_fig='./')
rfi_f.part_rfi_show(rfi_features, edge_size=3)
rfi_f.rfi_show(block_num=0,  save_fig='./')

# get_rfi_features(fits_dir='../data/FAST_data/')
