import rsgislib
from rsgislib import imagecalc

inputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee3.kea'
maskImg='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland.tif'

# inImgBands=['VV','VH','VVdivVH']
inImgBands=[1,2,3]

maskImgVal=1

outputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee3_WB_probability.tif'

rsgislib.imagecalc.calcMaskImgPxlValProb(inputImage, inImgBands, maskImg, maskImgVal, outputImage, 'GTiff')