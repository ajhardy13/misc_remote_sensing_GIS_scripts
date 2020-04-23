import gdal, rsgislib, subprocess
import numpy as np
from rsgislib import vectorutils


water_in='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif'
radar_in='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20171020T165722_Sigma0_stack_lee.tif'
outName='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/wetvegmask_barotseland_m18dB_20171020T165722.tif'
outShp='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/wetvegrmask_barotseland_m18dB_20171020T165722.shp'


#  snapping global water product to SAR image
print('Snapping watermask...')
waterSnap=water_in.split('.')[0]+'_'+inRefImg.split('_')[-2]+'.tif'
inRefImg=radar_in # base raster to snap to
gdalFormat = 'GTiff'
rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap


# read water mask as array
print("Reading raster datasets as arrays....")

water_read=gdal.Open(water_in)
watermask=np.array(water_read.GetRasterBand(1).ReadAsArray())

# read radar stack as array

radar_read=gdal.Open(radar_in)
# read VV band
vv_radar=np.array(radar_read.GetRasterBand(1).ReadAsArray())
vvDIVvh_radar=np.array(radar_read.GetRasterBand(3).ReadAsArray())


# condition to select perm water pixels with low backscatter
print("Conditions to extract permanent water....")
watermask[np.where(watermask<2)] = 0
watermask[np.where(watermask>=2)] = 1
# watermask[np.ma.masked_where(np.isnan(vv_radar) > -18)]=0 # masked to handle nan values

vvDIVvh_radar=np.where(np.isfinite(vvDIVvh_radar),vvDIVvh_radar,999)
watermask[np.where(vvDIVvh_radar>0.55)]=0
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