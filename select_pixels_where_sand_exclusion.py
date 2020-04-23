import gdal, rsgislib, os, subprocess
import numpy as np
from rsgislib import vectorutils, imagecalc
from rsgislib.imagecalc import BandDefn

# radar_in='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3.tif'
# outName='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/mask_barotseland_ltm8_20170318.tif'

# read water mask as array
print("Reading raster datasets as arrays....")
#ndvi='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/S2_composite_aug_sep_2017_ndvi_snapped.tif'
#seasonality='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif'
hand='/Users/Andy/Documents/Zambia/FloodModelling/HAND/HAND_Main_Channel_Only_120m_snapped.tif'
#ls_image='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/S2_composite_aug_sep_2017_swir_snapped.tif'
sel='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/sand_exclusion_layer/S1B_IW_GRDH_1SDV_2017_sel_2.kea'


outName='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/sand_exclusion_layer/sel_hand_sand_mask.kea'


bandDefns = []
#bandDefns.append(BandDefn('water', seasonality, 1))
bandDefns.append(BandDefn('hand', hand, 1))
#bandDefns.append(BandDefn('ndvi', ndvi, 1))
#bandDefns.append(BandDefn('swir', ls_image, 1))
bandDefns.append(BandDefn('sel', sel, 1))
# conditional statement to select semi-permanent water with high VV:VH difference 
print("Running conditional statement....")
gdalformat = 'KEA'
#imagecalc.bandMath(outName, '(ndvi>0.06)&&(ndvi<=0.12)&&(water==0)&&(hand>5)&&(swir>2000)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)
imagecalc.bandMath(outName, '(sel>60)&&(sel<94)&&(hand>5)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)

'''
file_read=gdal.Open(inFile)
mask=np.array(file_read.GetRasterBand(1).ReadAsArray())



# condition to select perm water pixels with low backscatter
print("Conditions to extract mask....")
mask[np.where(mask>3)] = 999
mask[np.where(mask<3)] = 0
mask[np.where(mask==999)] = 1

# write new dataset
# create new file
print("Writing raster result....")

driver = gdal.GetDriverByName('GTiff')
imageout = driver.Create(outName, file_read.RasterXSize , file_read.RasterYSize , 1, gdal.GDT_Byte)
imageout.GetRasterBand(1).WriteArray(mask)

# spatial ref system
proj = file_read.GetProjection()
georef = file_read.GetGeoTransform()
imageout.SetProjection(proj)
imageout.SetGeoTransform(georef)
imageout.FlushCache()

# option to vectorize the output
#rsgislib.vectorutils.polygoniseRaster(outName, outShp)

#cmd="ogr2ogr -where PXLVAL='1' '%s' '%s'" %(outShp,outShp) 
#subprocess.call(cmd, shell=True)
'''