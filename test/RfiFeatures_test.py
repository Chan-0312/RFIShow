from core.RfiFeatures import RfiFeatures

rfi_f = RfiFeatures('../data/FAST_data/G88.94-1.44_snapshot-M18_0001.fits')

mask, line_mask, blob_mask = rfi_f.get_mask(block_num=0, eta_i=[0.5, 0.55, 0.62, 0.75, 1])