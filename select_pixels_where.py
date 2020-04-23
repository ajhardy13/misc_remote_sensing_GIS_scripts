import gdal, rsgislib, os, subprocess, glob
import numpy as np
#from rsgislib import vectorutils, imagecalc
import rsgislib.imagecalc
from rsgislib.imagecalc import BandDefn

# radar_in='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3.tif'
# outName='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/mask_barotseland_ltm8_20170318.tif'

# read water mask as array
#print("Reading raster datasets as arrays....")
#inImg='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/2017/classified_stack_2017_occurrence_v2.kea'
#outName=inImg.replace('.kea','_perm_water.kea')

#list=sorted(glob.glob('*.tif'))
inImg='ESACCI_LC_Map.tif'
#for inImg in listImg:
	
bandDefns = []
bandDefns.append(BandDefn('inImg', inImg, 1))
print('Processing: ' + inImg)
# conditional statement 
#	print("Running conditional statement....")
#outName='./binary/'+inImg.replace('.tif','_water.tif')
outName='africa_wetland.kea'
gdalformat = 'KEA'
rsgislib.imagecalc.bandMath(outName, '(inImg==5)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)
