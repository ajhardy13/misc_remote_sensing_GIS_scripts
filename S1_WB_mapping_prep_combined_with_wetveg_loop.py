import rsgislib, os, gdal, subprocess, time, glob
from rsgislib import imagecalc, rastergis, imagefilter, vectorutils, imageutils
from rsgislib.imagecalc import BandDefn, imageutils
import rsgislib.imageutils
import numpy as np
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn import svm
from rsgislib.classification import classimgutils, classratutils
from sklearn.preprocessing import MaxAbsScaler

start = time.time()


# list all individual scenes (sorted by VV polarisation)
listFiles = glob.glob('*VV_dB.tif')

#  loop around list to extract snapped training data
for inFile in listFiles[14:len(listFiles)]:
	inputImage=inFile.split('_VV_')[0]
	print('Processing: ' + inputImage)
	#	point towards these input datasets

# 	inputImage='S1B_IW_GRDH_1SDV_20170517T165715_Sigma0' # prefix for image
	# globalWater='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland.tif'
	globalWater='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif'
	slopeMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'

	# inputImage='S1A_IW_GRDH_1SDV_20170315_B.tif'
	# globalWater='/Users/Andy/Documents/Zanzibar/Data/Rasters/global_water/water_mask_zbar_aoi.tif'
	# slopeMask='/Users/Andy/Documents/Zanzibar/Data/Rasters/SRTM/srtm_unguja_utm_lee9_slope_wgs84_mask.shp'

	inputImageVV=inputImage+'_VV_dB.tif'
	inputImageVH=inputImage+'_VH_dB.tif'

	#  function to create VV/VH ratio
	print('Creating VV/VH ratio...')
	def bandMath(inputImageVV,inputImageVH,outputImage):
		gdalformat = 'GTiff'
		datatype = rsgislib.TYPE_32FLOAT
		expression = 'b1/b2'
		bandDefns = []
		bandDefns.append(BandDefn('b1', inputImageVV, 1))
		bandDefns.append(BandDefn('b2', inputImageVH, 1))
		imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

	VVdivVH=inputImage+'_VVdivVH.tif'	

	bandMath(inputImageVV,inputImageVH,VVdivVH)


	#  function to stack VV, VH and VV/VH bands
	print('Stacking bands...')
	def imageStack(img1, img2, img3, outputImage):
		inputImages=[img1,img2,img3]
		bandList=['VV','VH','VVdivVH']

		gdalformat = 'GTiff'
		gdaltype = rsgislib.TYPE_32FLOAT
		rsgislib.imageutils.stackImageBands(inputImages, bandList, outputImage, None, 0, gdalformat, gdaltype)
		rsgislib.imageutils.setBandNames(outputImage, bandList)

	img1=inputImageVV
	img2=inputImageVH
	img3=VVdivVH
	outputImage=inputImage.split('.')[0]+'_stack.tif'

	imageStack(inputImageVV, inputImageVH, img3, outputImage)



	#  remove VV, VH and VVdivVH images
	# print('Removing intermediate images...')
# 	os.remove(inputImage.split('.')[0]+'_VV.tif')
# 	os.remove(inputImage.split('.')[0]+'_VH.tif')
# 	os.remove(VVdivVH)

	# read and filter image
	print('Filtering image...')

	outputImage=inputImage+'_stack_lee.tif'

	imagefilter.applyLeeFilter(inputImage+'_stack.tif', outputImage, 3, 3, "GTiff", rsgislib.TYPE_32FLOAT)

	bandList=['VV','VH','VVdivVH']
	rsgislib.imageutils.setBandNames(outputImage, bandList)

	#  snapping global water product to SAR image
	print('Snapping watermask...')

	waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-2]+'.tif'

	inRefImg=inputImage+'_stack_lee.tif' # base raster to snap to

	gdalFormat = 'GTiff'
	rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap


	#  select water mask pixels with global water layer =12 and low (<-18dB) backscatter

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
	radar_in=inputImage+'_stack_lee.tif'
	outName=waterSnap.split('.tif')[0]+'_m18dB.tif'
	outShp=waterSnap.split('.tif')[0]+'_m18dB.shp'
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
	radar_in=inputImage+'_stack_lee.tif'
	outName=waterSnap.split('.tif')[0]+'_wetveg.tif'
	outShp=waterSnap.split('.tif')[0]+'_wetveg.shp'
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