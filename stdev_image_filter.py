import rsgislib
from rsgislib import imagefilter
inputImage = '/Users/Andy/Documents/Tanzania/Sentinel/Sentinel1A_Namwawala/Out/Subset/dB/S1A_IW_GRDH_1SSV_20141014_Sigma0_VV_dB.tif'
outImgFile = '/Users/Andy/Documents/Tanzania/Sentinel/Sentinel1A_Namwawala/Out/Subset/dB/WB_prediction/test/S1A_IW_GRDH_1SSV_20141014_Sigma0_VV_dB_stdev.tif'
imagefilter.applyStdDevFilter(inputImage, outImgFile, 9, "GTiff", rsgislib.TYPE_32FLOAT)
