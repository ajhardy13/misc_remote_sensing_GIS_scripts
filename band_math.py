import rsgislib
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn
outputImage = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VVdivVH.tif'
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_32FLOAT
expression = 'b1/b2'
bandDefns = []
bandDefns.append(BandDefn('b1', '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VV_dB.tif', 1))
bandDefns.append(BandDefn('b2', '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_VH_dB.tif', 1))
imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)