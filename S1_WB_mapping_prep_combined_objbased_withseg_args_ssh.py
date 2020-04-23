#take stack_lee image > segment > add basic stats > 
#resample global water dataset to segmented image > 
#generate water mask using 'np.where' using global 
#water mask AND clump_mean data > generate wet veg mask

import rsgislib, os, gdal, subprocess, time, glob, argparse
from rsgislib import imagecalc, rastergis, imagefilter, vectorutils, imageutils
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from rsgislib.imagecalc import BandDefn



start = time.time()


globalWater='/mnt/Data/Andy/Projects/Zambia/Supporting_data/seasonality_barotseland_snapped.tif'
slopeMask='/mnt/Data/Andy/Projects/Zambia/Supporting_data/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
globalWater='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif'
slopeMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
sand_exclusion='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/2017/S1B_IW_GRDH_1SDV_2017_sel_2_gt60_lt94.kea'


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
# Shephard segmentation - this output will be used in second script to run classifier
##############################################################################################
print('Processing: ' + inputImage)

# run segmentation ---------------------------

print('Performing the segmentation...')
outputClumps=inputImage.split('.')[0]+'_clust5_clumps2.kea'
outputMeanImg = inputImage.split('.')[0]+'_clust5_clumps2_mean.kea'

segutils.runShepherdSegmentation(inputImage, outputClumps, outputMeanImg, minPxls=100, numClusters=5)

# set output band names
bandList=['VV','VH','VVdivVH']

#rsgislib.imageutils.setBandNames(inputImage, bandList)
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
# rastergis.populateStats(outputMeanImg, True, True, True, 1)


# populate RAT with mean stats from  S1
clumps=outputClumps # rename clumps image

ratutils.populateImageStats(inputImage, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)

##############################################################################################
# snap the sand exclusion layer and populate to RAT
bandList=['SEL']
rsgislib.imageutils.setBandNames(sand_exclusion, bandList)
sand_exclusion_snap=sand_exclusion.replace('.kea','_snapped.kea')
gdalFormat = 'KEA'
inRefImg=inputImage
rsgislib.imageutils.resampleImage2Match(inRefImg, sand_exclusion, sand_exclusion_snap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap
ratutils.populateImageStats(sand_exclusion_snap, clumps, calcMax=True,calcMean=True)

##############################################################################################



##############################################################################################
#  snapping global water product to SAR image
##############################################################################################
print('Snapping watermask...')

#waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-2]+'_new.tif'
waterSnap=globalWater.split('.')[0]+'_'+inputImage.split('_')[-4]+'_clump.tif'

inRefImg=inputImage # base raster to snap to

gdalFormat = 'GTiff'
rsgislib.imageutils.resampleImage2Match(inRefImg, globalWater, waterSnap, gdalFormat, interpMethod='nearestneighbour', datatype=None) # perform resampling/snap


##############################################################################################
# create open water training data
##############################################################################################
def watermask(water_in, radar_in, outName, outShp):
	print("Reading raster datasets as arrays....")
	
	# define bands
	bandDefns = []
	bandDefns.append(BandDefn('VV', radar_in, 1))
	bandDefns.append(BandDefn('water', water_in, 1))
	
	# conditional statement to select permanent water with low backscatter
	print("Running conditional statement....")
	gdalformat = 'KEA'
	imagecalc.bandMath(outName, '(VV<-18)&&(water==12)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)


water_in=waterSnap
radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
outName=waterSnap.replace('.tif','_m18dB.tif')
outShp=waterSnap.replace('.tif','_m18dB.shp')
print('Open water mask: ' +outShp)

watermask(water_in, radar_in, outName, outShp)

# vectorize the result
rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=outName, imgMaskBandNo=1)


##############################################################################################
# create veg water training data from global water layer and low VV/VH
##############################################################################################

#  select wet veg pixels defined as global water layer >2 and low ratio (<0.45) between VV and VH

def wetvegmask(water_in, radar_in, outName, outShp):
	print("Reading raster datasets as arrays....")
	
	# define bands
	bandDefns = []
	bandDefns.append(BandDefn('VVVH', radar_in, 3))
	bandDefns.append(BandDefn('water', water_in, 1))

	# conditional statement to select semi-permanent water with high VV:VH difference 
	print("Running conditional statement....")
	gdalformat = 'KEA'
	imagecalc.bandMath(outName, '(VVVH<0.45)&&(water>=2)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)


water_in=waterSnap
radar_in=inputImage.replace('.tif','_clumps2_mean.kea')
outName=waterSnap.replace('.tif','_wetveg.tif')
outShp=waterSnap.replace('.tif','_wetveg.shp')
print('Vegetated water mask: ' +outShp)

wetvegmask(water_in, radar_in, outName, outShp)

# vectorize the result
rsgislib.vectorutils.polygoniseRaster(outName, outShp, imgBandNo=1, maskImg=outName, imgMaskBandNo=1)


try:
	os.remove(waterSnap)
except Exception:
	pass

print('Runnin Time: {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp