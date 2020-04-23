import rsgislib
from rsgislib import imageutils

inImg = '22-04-2016_S1_classified.kea'
inputROIimage = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/20160426T083933_20160426T134208_T34LGJ.tif'
outImg = inImg.replace('.kea','_wb_mask.kea')

gdalformat='KEA'
datatype=rsgislib.TYPE_8UINT

rsgislib.imageutils.subset2img(inImg, inputROIimage, outImg, gdalformat, datatype)
imageutils.popImageStats(outImg, True, 0.0, True)
