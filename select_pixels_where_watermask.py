import gdal, rsgislib, subprocess
import numpy as np
from rsgislib import vectorutils


water_in='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_snapped_20170318.tif'
radar_in='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3.tif'
outName='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_m18dB_20170318.tif'
outShp='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_m18dB_20170318.shp'

# read water mask as array
print("Reading raster datasets as arrays....")

water_read=gdal.Open(water_in)
watermask=np.array(water_read.GetRasterBand(1).ReadAsArray())

# read radar stack as array

radar_read=gdal.Open(radar_in)
# read VV band
vv_radar=np.array(radar_read.GetRasterBand(1).ReadAsArray())


# condition to select perm water pixels with low backscatter
print("Conditions to extract permanent water....")
watermask[np.where(watermask!=1)] = 0
watermask[np.where(watermask==1)] = 1
# watermask[np.ma.masked_where(np.isnan(vv_radar) > -18)]=0 # masked to handle nan values

vv_radar=np.where(np.isfinite(vv_radar),vv_radar,999)
watermask[np.where(vv_radar>-18)]=0
# watermask[np.where(vv_radar<-8)]=0

# write new dataset
# create new file
print("Writing raster result....")

driver = gdal.GetDriverByName('GTiff')
imageout = driver.Create(outName, water_read.RasterXSize , water_read.RasterYSize , 1, gdal.GDT_Byte)
imageout.GetRasterBand(1).WriteArray(watermask)

# spatial ref system
proj = water_read.GetProjection()
georef = water_read.GetGeoTransform()
imageout.SetProjection(proj)
imageout.SetGeoTransform(georef)
imageout.FlushCache()

'''
# option to vectorize the output
inputImg=outName

rsgislib.vectorutils.polygoniseRaster(inputImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)

cmd="ogr2ogr -where PXLVAL='1' '%s' '%s'" %(outShp,outShp) 
subprocess.call(cmd, shell=True)
'''