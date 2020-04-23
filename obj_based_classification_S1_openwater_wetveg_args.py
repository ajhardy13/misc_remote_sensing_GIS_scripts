import rsgislib, os, gdal, time, subprocess, argparse, sys
from rsgislib import imageutils, rastergis
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn import svm
from rsgislib.classification import classimgutils, classratutils
from sklearn.preprocessing import MaxAbsScaler

start = time.time()

##############################################################################################
# definition of arguments
parser = argparse.ArgumentParser(prog='Extra trees classifier (OBIA).', description='Extra trees classifier (OBIA) for open and vegetated water using automatically generated training data.')
parser.add_argument('-i', metavar='', type=str, help='Path to the input image, i.e. original stacked image *_stack_lee.tif.')
args = parser.parse_args()
# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')
##############################################################################################



	
##############################################################################################	
inputImg=args.i
print('')
print('Input image: ' + inputImg)
print('')
#inputImg = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee.tif'
outputClumps=inputImg.split('.')[0]+'_clumps2.kea'    # name cf clumps image
outputMeanImg = inputImg.split('.')[0]+'_clumps2_mean.kea'    # name of clumps mean image

# output classified image
outimage=inputImg.split('.')[0]+'_clumps2_erf_clumptrain.tif'

otherMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
waterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_m18dB.shp'
vegwaterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_wetveg.shp'
##############################################################################################





##############################################################################################
# run segmentation ---------------------------
'''
print('Performing the segmentation...')

segutils.runShepherdSegmentation(inputImg, outputClumps, outputMeanImg, minPxls=100,distThres=500)
gdalformat = 'KEA'


bandList=['VV','VH','VVdivVH']

rsgislib.imageutils.setBandNames(inputImg, bandList)
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
# rastergis.populateStats(outputMeanImg, True, True, True, 1)


# populate RAT with mean stats from  S1
clumps=outputClumps # rename clumps image

ratutils.populateImageStats(inputImg, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)'''
##############################################################################################




# populate clumps with training data
print('Populating clumps with stats...')
classesDict = dict()
classesDict['Water'] = [1, waterMask]
classesDict['Other'] = [2, otherMask]  
classesDict['VegWater'] = [3, vegwaterMask]

tmpPath = './temp_' + inputImg

classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'


ratutils.populateClumpsWithClassTraining(outputClumps, classesDict, tmpPath, classesIntCol, classesNameCol)

# balance the training data
rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesIntColBal', 50, 5000)
classesIntCol='classesIntColBal'

# classify the image ---------------------------

# define the classifier
classifier = ExtraTreesClassifier(n_estimators=500, n_jobs=-1)
# classifier = RandomForestClassifier(n_estimators=100, max_features=3, oob_score=True, n_jobs=-1, verbose=0)
# classifier = svm.SVC(kernel='rbf') 

# define the output colours
classColours = dict()
classColours['Other'] = [212,125,83]
classColours['Water'] = [157,212,255]
classColours['VegWater'] = [191,255,0]


# define variables for the classification
variables = ['VVMin','VHMin','VVdivVHMin','VVMax','VHMax','VVdivVHMax','VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd']
# run the classification
classratutils.classifyWithinRAT(outputClumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours,preProcessor=MaxAbsScaler())

# export rat column to image

gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8INT
fields = ['OutClass']

rastergis.exportCols2GDALImage(outputClumps, outimage, gdalformat, datatype, fields)


os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stam
