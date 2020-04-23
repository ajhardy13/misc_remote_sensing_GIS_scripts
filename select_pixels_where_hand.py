import gdal, rsgislib, subprocess
import numpy as np
from rsgislib import vectorutils, imagecalc

from rsgislib.imagecalc import BandDefn


slope='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotse_srtm_5x5_slope.tif'
hand='/Users/Andy/Documents/Zambia/FloodModelling/HAND/GEE_hand/hand90_1000.tif'

outShp='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
outShp2='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/barotseland_srtm_utm_lee_slope_gt1_5_wgs84_pxl1.shp'


#  snapping 
slopeSnap='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/srtm_arc1_barotseland_5x5_slope_snap.kea'
inRefImg=hand # base raster to snap to
gdalFormat = 'KEA'
#rsgislib.imageutils.resampleImage2Match(inRefImg, slope, slopeSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap

bandDefns = []
bandDefns.append(BandDefn('slope', slopeSnap, 1))
bandDefns.append(BandDefn('hand', hand, 1))

outName='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/srtm_arc1_barotseland_5x5_slope_gt3_and_hand_gt30.kea'

gdalformat = 'KEA'
imagecalc.bandMath(outName, '(slope>3)&&(hand>30)&&(hand<1000)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)

# option to vectorize the output
inputImg=outName

rsgislib.vectorutils.polygoniseRaster(inputImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)

cmd="ogr2ogr -where PXLVAL='1' '%s' '%s'" %(outShp,outShp2) 
subprocess.call(cmd, shell=True)
