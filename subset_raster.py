import rsgislib
from rsgislib import imageutils

# inputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3.kea'
inputImage='/Users/Andy/Documents/TEACHING/Dissertations/2017_18/robbie/Outputs/LS5TM_20060719_lat53lon351_r23p204_vmsk_rad_sref.tif'

# outputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_testAOI2.kea'
outputImage='/Users/Andy/Documents/TEACHING/Dissertations/2017_18/robbie/Outputs/LS5TM_20060719_lat53lon351_r23p204_vmsk_rad_sref_clip.tif'

# inputVector='/Users/Andy/Documents/Misc/zambia_test_aoi_2.shp'
inputVector='/Users/Andy/Documents/TEACHING/Dissertations/2017_18/robbie/AOI.shp'

gdalformat = 'GTiff'
datatype = rsgislib.imageutils.getRSGISLibDataType(inputImage)

imageutils.subset(inputImage, inputVector, outputImage, gdalformat, datatype)