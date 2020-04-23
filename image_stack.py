import rsgislib
from rsgislib import imageutils, rastergis

img1='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VV_dB.tif'
img2='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VH_dB.tif'
img3='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VVdivVH.tif'
# img4='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_testAOI2_prob_snap.tif'


inputImages=[img1,img2,img3]
bandList=['VV','VH','VVdivVH']
outFolder='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/'
outputImage = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_stack_lee3.kea'

gdalformat = 'KEA'
gdaltype = rsgislib.TYPE_32FLOAT
rsgislib.imageutils.stackImageBands(inputImages, bandList, outputImage, None, 0, gdalformat, gdaltype)
rsgislib.imageutils.setBandNames(outputImage, bandList)
rastergis.populateStats(outputImage, True, True, True, 1)

