import rsgislib
from rsgislib import imageutils

inImg = 'S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee.tif'
imgMask = 'S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee_clumps2_erf_clumptrain_mode.tif'
outImg = inImg.replace('.tif','_wb_mask.kea')

gdalformat='KEA'
datatype=rsgislib.TYPE_32FLOAT

# mask image using list of values i.e.[2,3] to be replaced by the mask value i.e. 0
rsgislib.imageutils.maskImage(inImg, imgMask, outImg, gdalformat, datatype, 0, [2,3])
imageutils.popImageStats(outImg, True, 0.0, True)
