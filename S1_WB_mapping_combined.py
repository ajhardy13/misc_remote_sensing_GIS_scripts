import rsgislib, os, gdal, subprocess, time
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

#	***ensure you have created a 'Classified' folder in your working dir***

# inputImage='S1B_IW_GRDH_1SDV_20170330.tif'
# globalWater='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland.tif'
# slopeMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_mask_wgs84.shp'

inputImage='S1A_IW_GRDH_1SDV_20170315_B.tif'
globalWater='/Users/Andy/Documents/Zanzibar/Data/Rasters/global_water/water_mask_zbar_aoi.tif'
slopeMask='/Users/Andy/Documents/Zanzibar/Data/Rasters/SRTM/srtm_unguja_utm_lee9_slope_wgs84_mask.shp'

#  function to create VV/VH ratio
print('Creating VV/VH ratio...')
def bandMath(inputImage,outputImage):
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_32FLOAT
	expression = 'b1/b2'
	bandDefns = []
	bandDefns.append(BandDefn('b1', inputImage, 1))
	bandDefns.append(BandDefn('b2', inputImage, 2))
	imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

VVdivVH=inputImage.split('.')[0]+'_VVdivVH.tif'	
bandMath(inputImage,VVdivVH)

#  extract first two bands from the S1 image
print('Extrating VV and VH bands...')
def selectImage(inputImage,bandNum, outputImage):	
	bands = bandNum
	rsgislib.imageutils.selectImageBands(inputImage, outputImage, 'GTiff', rsgislib.TYPE_32FLOAT, bands)

outputImage=inputImage.split('.')[0]+'_VV_VH.tif'

selectImage(inputImage, [1], inputImage.split('.')[0]+'_VV.tif')	
selectImage(inputImage, [2], inputImage.split('.')[0]+'_VH.tif')	

#  function to stack VV, VH and VV/VH bands
print('Stacking bands...')
def imageStack(img1, img2, img3, outputImage):
	inputImages=[img1,img2,img3]
	bandList=['VV','VH','VVdivVH']

	gdalformat = 'GTiff'
	gdaltype = rsgislib.TYPE_32FLOAT
	rsgislib.imageutils.stackImageBands(inputImages, bandList, outputImage, None, 0, gdalformat, gdaltype)
	rsgislib.imageutils.setBandNames(outputImage, bandList)

img1=inputImage.split('.')[0]+'_VV.tif'
img2=inputImage.split('.')[0]+'_VH.tif'
img3=VVdivVH
outputImage=inputImage.split('.')[0]+'_stack.tif'

imageStack(img1, img2, img3, outputImage)

#  remove VV, VH and VVdivVH images
print('Removing intermediate images...')
os.remove(inputImage.split('.')[0]+'_VV.tif')
os.remove(inputImage.split('.')[0]+'_VH.tif')
os.remove(VVdivVH)

# read and filter image
print('Filtering image...')
outputImage=inputImage.split('.')[0]+'_stack_lee.tif'
imagefilter.applyLeeFilter(inputImage.split('.')[0]+'_stack.tif', outputImage, 3, 3, "GTiff", rsgislib.TYPE_32FLOAT)

bandList=['VV','VH','VVdivVH']
rsgislib.imageutils.setBandNames(outputImage, bandList)

#  snapping global water product to SAR image
print('Snapping watermask...')
waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-1]
inRefImg=inputImage.split('.')[0]+'_stack_lee.tif' # base raster to snap to
gdalFormat = 'GTiff'
rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap


#  select water mask pixels with low (<-18dB) backscatter

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
	watermask[np.where(watermask!=1)] = 0
	watermask[np.where(watermask==1)] = 1
	# watermask[np.ma.masked_where(np.isnan(vv_radar) > -18)]=0 # masked to handle nan values

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

	# option to vectorize the output
	inputImg=outName

	rsgislib.vectorutils.polygoniseRaster(inputImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)

	cmd="ogr2ogr -where PXLVAL='1' '%s' '%s'" %(outShp,outShp) 
	subprocess.call(cmd, shell=True)	
	
water_in=waterSnap
radar_in=inputImage.split('.')[0]+'_stack_lee.tif'
outName=waterSnap.split('.tif')[0]+'_m18dB.tif'
outShp=waterSnap.split('.tif')[0]+'_m18dB.shp'

watermask(water_in, radar_in, outName, outShp)

try:
	os.remove(waterSnap)
except Exception:
	pass

# 
#     perform the classification
# 

def classify(inputImg, outputClumps, outputMeanImg, outimage):
	# run segmentation ---------------------------
	print('Performing the segmentation...')

	segutils.runShepherdSegmentation(inputImg, outputClumps, outputMeanImg, minPxls=100)
	gdalformat = 'KEA'
	bandList=['VV','VH','VVdivVH']
	rsgislib.imageutils.setBandNames(inputImg, bandList)
	rsgislib.imageutils.setBandNames(outputMeanImg, bandList)

	print('Populate RAT with stats...')
	clumps=outputClumps # rename clumps image
	ratutils.populateImageStats(inputImg, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)

	# populate clumps with training data
	print('Populating clumps with training data...')
	classesDict = dict()
	classesDict['Water'] = [1, outShp]
	classesDict['Other'] = [2, slopeMask]  
	tmpPath = './temp'
	classesIntCol = 'ClassInt'
	classesNameCol = 'ClassStr'
	ratutils.populateClumpsWithClassTraining(outputClumps, classesDict, tmpPath, classesIntCol, classesNameCol)
 
 	# balance the training data
	# rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesIntColBal', 500, 1000)
	# classesIntCol='classesIntColBal'

	# classify the image ---------------------------
	print('Performing classification...')
	
	classifier = svm.SVC(kernel='rbf') # define the classifier
	# define the output colours
	classColours = dict()
	classColours['Other'] = [212,125,83]
	classColours['Water'] = [157,212,255]

	variables = ['VVMin','VHMin','VVdivVHMin','VVMax','VHMax','VVdivVHMax','VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd']
	classratutils.classifyWithinRAT(outputClumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours,preProcessor=MaxAbsScaler())

	# export rat column to image
	print('Exporting RAT to image...')
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_8INT
	fields = ['OutClass']
	rastergis.exportCols2GDALImage(outputClumps, outimage, gdalformat, datatype, fields)

inputImg = inputImage.split('.')[0]+'_stack_lee.tif'
outputClumps=inputImage.split('.')[0]+'_stack_lee_clumps2.kea' # for some reason the clumps filename cannot end in '...clumps.kea' - it gets deleted in the process
outputMeanImg = inputImage.split('.')[0]+'_stack_lee_clumps_mean.kea'
outimage='Classified/'+inputImage.split('.')[0]+'_WB.tif'

classify(inputImg, outputClumps, outputMeanImg, outimage)



os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp