import rsgislib, os, gdal, time, argparse, sys, numpy, rios, os.path, glob
from numba import jit
import os.path
from rsgislib import imageutils, rastergis, imagefilter, imagecalc
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier
from rsgislib.classification import classimgutils, classratutils
from sklearn.preprocessing import MaxAbsScaler
from sklearn.grid_search import GridSearchCV
from rsgislib.imagecalc import BandDefn
from rios import rat
from scipy import stats
import numpy as np
from osgeo import gdal
from skimage import filters
from scipy.stats import skew



start = time.time()

##############################################################################################
# definition of arguments
parser = argparse.ArgumentParser(prog='Extraction of training data for water/non-water', description='Extraction of training data for use in water/non-water classification.')
parser.add_argument('-i', metavar='', type=str, help='Path to the input image, i.e. original stacked image *_stack_lee.tif.')
args = parser.parse_args()
# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')
##############################################################################################

##############################################################################################	
inputImage=args.i
print('')
print('Input image: ' + inputImage)
print('')

##############################################################################################
# output classifcation rootname
outimage=inputImage.split('.')[0]+'_classified.kea'

##############################################################################################
# ancialliary datasets
guf='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_Zambia_extended.kea' # global urban footprint
permWater='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/2017/classified_stack_2017_occurrence_v2_perm_water.kea' # permanent water layer
globalWater='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif' # global water seasonality layer
otherMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_gt1_5_AND_HAND_gt_30.shp' # training data for dry areas

# check that ancilliary dataset exist
if not os.path.isfile(guf):
	sys.exit('\n' + 'Missing: Global Urban Footprint.')
if not os.path.isfile(permWater):
	sys.exit('\n' + 'Missing: Water occurence layer.')
if not os.path.isfile(globalWater):
	sys.exit('\n' + 'Missing: Pekel water seasonality layer.')
if not os.path.isfile(otherMask):
	sys.exit('\n' + 'Missing: "Other" mask.')

############################################################################################################################################################################################
# perform Lee filter
#outputImage=inputImage.replace('.tif','_lee.tif')
outputImage=inputImage

#imagefilter.applyLeeFilter(inputImage, outputImage, 3, 3, "GTiff", rsgislib.TYPE_32FLOAT)

bandList=['VV','VH','VVdivVH']
rsgislib.imageutils.setBandNames(outputImage, bandList)

inputImage=outputImage # define lee image as input for rest of the script

##############################################################################################
# Shepherd segmentation - this output will be used in second script to run classifier
##############################################################################################
print('Performing the segmentation...')

outputClumps=inputImage.replace('.tif','_clumps2.kea')
outputMeanImg=inputImage.replace('.tif','_clumps2_mean.kea')

#segutils.runShepherdSegmentation(inputImage, outputClumps, outputMeanImg, minPxls=100)
bandList=['VV','VH','VVdivVH']  
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
#rastergis.populateStats(outputClumps, True, True, True, 1)
#rastergis.populateStats(outputMeanImg, True, True, True, 1)

clumps=outputClumps # rename clumps image
#ratutils.populateImageStats(inputImage, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True) # add radar stats

##############################################################################################
# add global urban footprint stats

gufSnap=guf.split('.')[0]+'_'+inputImage.split('/')[-1].split('_')[4]+'.tif'
#gufSnap=guf.split('.')[0]+'_'+inputImage.split('/')[-1].split('_')[0]+'.tif'
inRefImg=clumps # base raster to snap to
gdalFormat = 'GTiff'
rsgislib.imageutils.resampleImage2Match(inRefImg, guf, gufSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap
bandList=['guf']  
rsgislib.imageutils.setBandNames(gufSnap, bandList)
#ratutils.populateImageStats(gufSnap, clumps, calcMax=True) # add urban footprint stats

# remove the intermediate snapped guf image
try:
	os.remove(gufSnap)
except Exception:
	pass

##############################################################################################
# Extracting training data masks 
##############################################################################################

waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('/')[-1].split('_')[4]+'_clump.tif'
#waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('/')[-1].split('_')[0]+'_clump.tif'
inRefImg=inputImage # base raster to snap to
gdalFormat = 'GTiff'
rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap

##############################################################################################
# create open water training data
##############################################################################################
#function to extract permanent water with low dB (lt -18dB)
@jit
def watermask(water_in, radar_in, outName, outShp): 
	bandDefns = []
	bandDefns.append(BandDefn('VV', radar_in, 1))
	bandDefns.append(BandDefn('water', water_in, 1))
	gdalformat = 'KEA'
	imagecalc.bandMath(outName, '(VV<-18)&&(water==12)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)

water_in=waterSnap
radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
outName=waterSnap.replace('.tif','_m18dB.tif')
outShp=waterSnap.replace('.tif','_m18dB.shp')
watermask(water_in, radar_in, outName, outShp) # implement function
rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=outName, imgMaskBandNo=1) # vectorize the result
waterMask=outShp # define training data filename for rest of script

##############################################################################################
# create veg water training data 
##############################################################################################

# function to extract low VV/VH ratio (lt 0.5) 
@jit
def wetvegmask(water_in, radar_in, outName, outShp):
	bandDefns = []
	bandDefns.append(BandDefn('VVVH', radar_in, 3))
	#bandDefns.append(BandDefn('water', water_in, 1))
	gdalformat = 'KEA'
	#imagecalc.bandMath(outName, '(VVVH<0.45)&&(water>=2)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)
	imagecalc.bandMath(outName, '(VVVH<0.5)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)

water_in=waterSnap
radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
outName=waterSnap.replace('.tif','_wetveg.tif')
outShp=waterSnap.replace('.tif','_wetveg.shp')
wetvegmask(water_in, radar_in, outName, outShp) # implement function 
rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=outName, imgMaskBandNo=1) # vectorize the result
vegwaterMask=outShp # define training data filename for rest of script

# remove the intermediate snapped water image
try:
	os.remove(waterSnap)
except Exception:
	pass

##############################################################################################
##############################################################################################
######
###### perform the classification
######
##############################################################################################
##############################################################################################

##############################################################################################
# populate clumps with training data
classesDict = dict()
classesDict['Water'] = [1, waterMask]
classesDict['Other'] = [2, otherMask]  
classesDict['VegWater'] = [3, vegwaterMask]

tmpPath = './temp_' + inputImage.split('.')[0]
classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'
ratutils.populateClumpsWithClassTraining(outputClumps, classesDict, tmpPath, classesIntCol, classesNameCol)
rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesIntColBal', 50, 5000) # balance the training data
classesIntCol='classesIntColBal'

##############################################################################################
# use grid search to define the classifier
variables = ['VVMin','VHMin','VVdivVHMin','VVMax','VHMax','VVdivVHMax','VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd']
classParameters = {'n_estimators':[10, 100, 500], 'max_features':[2, 3, 4]}
gsearch = GridSearchCV(ExtraTreesClassifier(bootstrap = True), classParameters)
classifier = classratutils.findClassifierParameters(outputClumps,  classesIntCol, variables,  preProcessor=None, gridSearch=gsearch)

# define the output colours
classColours = dict()
classColours['Other'] = [212,125,83]
classColours['Water'] = [157,212,255]
classColours['VegWater'] = [191,255,0]

##############################################################################################
# run the classification
###########################################################################################
#  run thorugh mulitple classifications and store result in RAT
runs=numpy.arange(1,51)
#runs=numpy.arange(1,3)
'''
for i in runs:
	outColInt='OutClass_'+str(i) # define output class column
	print('')
	print('......processing: ' + outColInt)
	print('')
	classesIntCol = 'ClassInt'
	rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesIntColBal', 50, 5000) # rebalance the training data
	classesIntCol='classesIntColBal'
	# run the classifier
	classratutils.classifyWithinRAT(outputClumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours,preProcessor=MaxAbsScaler(),outColInt=outColInt)
'''
###########################################################################################
# Read all results from RAT and extract mode, providing final result
# Also, mask out nan values from the classification where vvMax==0

inRatFile = outputClumps
ratDataset = gdal.Open(inRatFile, gdal.GA_Update) # Open RAT

vvMax_val=[]
vvMax_val.append(rat.readColumn(ratDataset, 'VVMax')) # read in urban footprint column
vvMax_val=numpy.asarray(vvMax_val[0])

guf_val=[]
guf_val.append(rat.readColumn(ratDataset, 'gufMax')) # read in urban footprint column
guf_val=numpy.asarray(guf_val[0])

# define column names for output classifications
#runs=numpy.arange(1,51)
x_col_names = []
for i in runs:
	# define output class column
	col_name='OutClass_'+str(i)
	x_col_names.append(col_name)

X=[]
# Read in data from each column
for colName in x_col_names:
    X.append(rat.readColumn(ratDataset, colName))

mode = stats.mode(X)
mode=numpy.asarray(mode[0][0])
rios.rat.writeColumn(outputClumps, 'OutClass_mode', mode, colType=gdal.GFT_Integer)

# calc certainty from mode and count of mode
X_arr=numpy.asarray(X)
x_count=[]
x_percent=[]
for i, m in zip((range(X_arr.shape[1])),mode):
	b=X_arr[:,i]
	count=numpy.count_nonzero(b==m)
	x_percent.append(count/X_arr.shape[0])

x_percent=numpy.asarray(x_percent)

# where percentage match is less that 100%, classify as dry
mode_cert=mode
mode_cert[numpy.where((x_percent<1)&(mode_cert==1))]=2
mode_cert[numpy.where((x_percent<1)&(mode_cert==3))]=2

# where GUF == 255, and mode_cert==3 (vegWater) classify as dry
mode_cert[numpy.where((guf_val==255)&(mode_cert==3))]=2

# where vvMax==0, unclassified
mode_cert[numpy.where((vvMax_val==0))]=0

#write out the result
names=[]
for i in mode_cert:
	if i==0:
		names.append('Unclassified')
	elif i==1:
		names.append('Water')
	elif i==2:
		names.append('Other')
	elif i==3:
		names.append('VegWater')

# write columns to RAT
rios.rat.writeColumn(outputClumps, 'OutClass_mode_pc', x_percent, colType=gdal.GFT_Real)
rios.rat.writeColumn(outputClumps, 'OutClass_mode_cert', mode_cert, colType=gdal.GFT_Integer)
rios.rat.writeColumn(outputClumps, 'OutClass_mode_cert_names', names, colType=gdal.GFT_String)

###########################################################################################
# export rat column: mode with certainty to image
gdalformat = 'KEA'
datatype = rsgislib.TYPE_8INT
fields = ['OutClass_mode_cert']
outCert=inputImage.split('.')[0]+'_cert.kea'
rastergis.exportCols2GDALImage(outputClumps, outCert, gdalformat, datatype, fields)

####################################################################
# snap permanent water	
inProcessImg=permWater
inRefImg=inputImage
outSnap=permWater.replace('.kea','_'+inputImage.split('/')[-1].split('_')[4]+'_snap.kea')
#outSnap=permWater.replace('.kea','_'+inputImage.split('/')[-1].split('_')[0]+'_snap.kea')
gdalformat = 'KEA'
rsgislib.imageutils.resampleImage2Match(inRefImg, inProcessImg, outSnap, gdalformat,interpMethod='nearestneighbour', datatype=rsgislib.TYPE_8UINT)


####################################################################
# add permanent water mask
permWaterMask=outSnap

bandDefns = []
bandDefns.append(BandDefn('class', outCert, 1))
bandDefns.append(BandDefn('permWat', permWaterMask, 1))

condition='(permWat==1)?1:class'

gdalformat = 'kea'
imagecalc.bandMath(outimage, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)

# remove the intermediate certainty classifcation image
try:
	os.remove(outCert)
except Exception:
	pass

###########################################################################################
# select dry season images and apply refinement
d=int(inputImage.split('/')[-1].split('_')[4][4:6])
#d=int(inputImage.split('/')[-1].split('_')[0][3:5])

if (d >= 2) & (d <= 5): # select dry season images based on image month
	print('')
	print('Finished...')
	print('')
else:
	print('')
	print('Refinement needed.')
	print('')
	
	'''
	#mask the original stacked S1 image using open water prediction
	gdalformat='KEA'
	datatype=rsgislib.TYPE_32FLOAT
	imgMask=outimage
	outImg = inputImage.replace('.tif','_wb_mask.kea')
	rsgislib.imageutils.maskImage(inputImage, imgMask, outImg, gdalformat, datatype, 0, [2,3]) # mask out dry or wetVeg pixels
	imageutils.popImageStats(outImg, True, 0.0, True)
	
	#segment image and add stats from S1 image
	inImg=outImg # in image based on masked radar image
	clumps=inImg.replace('.kea','_clumps2.kea')
	clumpsMean=outImg.replace('.kea','_clumps2_mean.kea')
	segutils.runShepherdSegmentation(inImg, clumps, clumpsMean, minPxls=100, numClusters=5)
	bandList=['VV','VH','VVdivVH']
	rsgislib.imageutils.setBandNames(inImg, bandList)
	
	####################################################################
	# extract otsu threshold from VV band
	ds1 = gdal.Open(clumpsMean)
	maskVV = np.array(ds1.GetRasterBand(1).ReadAsArray())
	maskVV=maskVV[maskVV<0]
	threshold=filters.threshold_otsu(maskVV)
	ds1=None
	'''
	clumpsMean=outputMeanImg
	# read in VV mean data and original classificaiton
	ds1 = gdal.Open(clumpsMean)
	meanVV = np.array(ds1.GetRasterBand(1).ReadAsArray())
	ds1 = gdal.Open(outimage)
	classImg = np.array(ds1.GetRasterBand(1).ReadAsArray())

	#	mask out mean VV pixels where original classificaiton was open water
	meanVV[numpy.where(classImg!=1)]=numpy.nan
	meanVVsmoothed5=filters.gaussian(meanVV,sigma=5) # smooth out masked image using gaussian, sigma=5
	
	ds1=None
	
#	pylab.hist(meanVVsmoothed5[~numpy.isnan(meanVVsmoothed5)],bins=100)
#	pylab.hist(meanVV[~numpy.isnan(meanVV)],bins=100)
#	pylab.show()
#	define threhsold using otsu applied to gaussian smoothed masked image
	threshold=filters.threshold_otsu(meanVVsmoothed5[meanVVsmoothed5<0])
	print('')
	print('Ostu threshold = ' + str(threshold))
	print('')
	meanVVsmoothed5=None
	meanVV=None
	classImg
#	filters.threshold_otsu(meanVV[meanVV<0])
	
	####################################################################
	# apply threshold 
	bandDefns = []
	bandDefns.append(BandDefn('class', outimage, 1))
	bandDefns.append(BandDefn('vvMean', clumpsMean, 1))
	
	condition='(class==1)&&(vvMean>'+str(threshold)+')?2:class'
	outClass=outimage.replace('.kea','_otsu.kea')
	gdalformat = 'KEA'
	imagecalc.bandMath(outClass, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)
	
	bandDefns = []
	bandDefns.append(BandDefn('class', outClass, 1))
	bandDefns.append(BandDefn('permWat', permWaterMask, 1))
	
	condition='(permWat==1)?1:class'
	outClass=outimage.replace('.kea','_refined2.kea')
	gdalformat = 'KEA'
	imagecalc.bandMath(outClass, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)

	try:
		os.remove(outimage.replace('.kea','_otsu.kea'))
	except Exception:
		pass
	
	# remove all open water snapped images
	for file in glob.glob('*'+os.path.split(inputImage)[1].split('_')[4]+'*wb*'):
#	for file in glob.glob('*'+os.path.split(inputImage)[1].split('_')[0]+'*wb*'):
		os.remove(file)

	
	###################################################################
	print('')
	print('Finished refinement.')
	print('')
	

###########################################################################################

try:
	os.remove(permWaterMask)
except Exception:
	pass
'''
# remove all open water snapped images
for file in glob.glob(os.path.split(permWater)[0]+'/*'+os.path.split(inputImage)[1].split('_')[4]+'*'):
#for file in glob.glob(os.path.split(permWater)[0]+'/*'+os.path.split(inputImage)[1].split('_')[0]+'*'):
	os.remove(file)
'''
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp
