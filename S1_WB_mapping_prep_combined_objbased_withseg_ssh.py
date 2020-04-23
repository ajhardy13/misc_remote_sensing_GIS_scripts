#take stack_lee image > segment > add basic stats > 
#resample global water dataset to segmented image > 
#generate water mask using 'np.where' using global 
#water mask AND clump_mean data > generate wet veg mask

import rsgislib, os, gdal, subprocess, time, glob
from rsgislib import imagecalc, rastergis, imagefilter, vectorutils, imageutils
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from rsgislib.imagecalc import BandDefn, imageutils
import rsgislib.imageutils
import numpy as np
from rsgislib.rastergis import ratutils


start = time.time()


globalWater='/mnt/Data/Andy/Projects/Zambia/Supporting_data/seasonality_barotseland_snapped.tif'
slopeMask='/mnt/Data/Andy/Projects/Zambia/Supporting_data/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'

listFiles=glob.glob('*stack_lee.tif')

for inputImage in listFiles:

	#inputImage='S1B_IW_GRDH_1SDV_20170505T165715_Sigma0_stack_lee_clumps2_mean.kea'
	print('Processing: ' + inputImage)
	
	# run segmentation ---------------------------
	print('Performing the segmentation...')
	outputClumps=inputImage.split('.')[0]+'_clumps2.kea'
	outputMeanImg = inputImage.split('.')[0]+'_clumps2_mean.kea'
	
	segutils.runShepherdSegmentation(inputImage, outputClumps, outputMeanImg, minPxls=100)

	# set output band names
	bandList=['VV','VH','VVdivVH']

	rsgislib.imageutils.setBandNames(inputImage, bandList)
	rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
	# rastergis.populateStats(outputMeanImg, True, True, True, 1)


	# populate RAT with mean stats from  S1
	clumps=outputClumps # rename clumps image

	ratutils.populateImageStats(inputImage, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)

for inputImage in listFiles:	

	#  snapping global water product to SAR image
	print('Snapping watermask...')

	#waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-2]+'_new.tif'
	waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-4]+'_clump.tif'

	inRefImg=inputImage # base raster to snap to

	gdalFormat = 'GTiff'
	rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap


	def watermask(water_in, radar_in, outName, outShp):
		print("Reading raster datasets as arrays....")
		water_read=gdal.Open(water_in)
		watermask=np.array(water_read.GetRasterBand(1).ReadAsArray())

		# read radar stack as array

		radar_read=gdal.Open(radar_in)
		# read VV band
		vv_radar=np.array(radar_read.GetRasterBand(1).ReadAsArray())

		# condition to select perm water pixels with low backscatter
		print("Conditions to extract permanent water....")
		watermask[np.where(watermask<12)] = 0
		watermask[np.where(watermask==12)] = 1

		vv_radar=np.where(np.isfinite(vv_radar),vv_radar,999)
		watermask[np.where(vv_radar>-18)]=0

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


	water_in=waterSnap
	radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
	outName=waterSnap.replace('.tif','_m18dB.tif')
	outShp=waterSnap.replace('.tif','_m18dB.shp')
	print('Open water mask: ' +outShp)

	watermask(water_in, radar_in, outName, outShp)

	# vectorize the result
	rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)

	# remove zero values from shapefile
	cmd="ogr2ogr -where PXLVAL='1'  -t_srs EPSG:4326 '%s' '%s'" %(outShp,outShp) 
	subprocess.call(cmd, shell=True)



	#  select wet veg pixels defined as global water layer >2 and low ratio (<0.45) between VV and VH

	def wetvegmask(water_in, radar_in, outName, outShp):
		print("Reading raster datasets as arrays....")
		water_read=gdal.Open(water_in)
		watermask=np.array(water_read.GetRasterBand(1).ReadAsArray())

		# read radar stack as array

		radar_read=gdal.Open(radar_in)
		# read VV band
		vvvh_radar=np.array(radar_read.GetRasterBand(3).ReadAsArray())

		# condition to select seasonal water pixels with low ratio in VV/VH backscatter
		print("Conditions to extract vegetated water bodies....")
		watermask[np.where(watermask<2)] = 0
		watermask[np.where(watermask>=2)] = 1

		vvvh_radar=np.where(np.isfinite(vvvh_radar),vvvh_radar,999)
		watermask[np.where(vvvh_radar>0.45)]=0

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


	water_in=waterSnap
	radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
	outName=waterSnap.replace('.tif','_wetveg.tif')
	outShp=waterSnap.replace('.tif','_wetveg.shp')
	print('Vegetated water mask: ' +outShp)

	wetvegmask(water_in, radar_in, outName, outShp)

	# vectorize the result
	rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)

	# remove zero values from shapefile
	cmd="ogr2ogr -where PXLVAL='1'  -t_srs EPSG:4326 '%s' '%s'" %(outShp,outShp) 
	subprocess.call(cmd, shell=True)


	try:
		os.remove(waterSnap)
	except Exception:
		pass

print('Runnin Time: {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp