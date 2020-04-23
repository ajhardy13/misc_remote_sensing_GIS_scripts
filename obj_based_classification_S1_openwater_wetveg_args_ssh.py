import rsgislib, os, gdal, time, subprocess, argparse, sys, numpy, rios
import os.path
from rsgislib import imageutils, rastergis
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn import svm
from rsgislib.classification import classimgutils, classratutils
from sklearn.preprocessing import MaxAbsScaler
from sklearn.grid_search import GridSearchCV
from rios import rat
from scipy import stats

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
outimage=inputImg.split('.')[0]+'_clumps2_erf_clumptrain_mode.tif'

#otherMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
#waterMask='/mnt/Data/Andy/Projects/Zambia/Supporting_data/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_m18dB.shp'
#vegwaterMask='/mnt/Data/Andy/Projects/Zambia/Supporting_data/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_wetveg.shp'

otherMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/barotseland_srtm_utm_lee_slope_gt1_5_wgs84.shp'
waterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_m18dB.shp'
vegwaterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/seasonality_barotseland_snapped_'+inputImg.split('/')[-1].split('_')[4]+'_clump_wetveg.shp'
##############################################################################################





##############################################################################################    populate clumps with training data

print('Populating clumps with stats...')

print('otherMask: ' + otherMask)
print('waterMask: ' + waterMask)
print('vegwaterMask: ' + vegwaterMask)
classesDict = dict()
classesDict['Water'] = [1, waterMask]
classesDict['Other'] = [2, otherMask]  
classesDict['VegWater'] = [3, vegwaterMask]

tmpPath = './temp_' + inputImg.split('.')[0]

classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'


ratutils.populateClumpsWithClassTraining(outputClumps, classesDict, tmpPath, classesIntCol, classesNameCol)


# balance the training data
rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesInt', 50, 5000)
classesIntCol='classesIntColBal'

# classify the image ---------------------------

# use grid search to define the classifier
#classifier = ExtraTreesClassifier(n_estimators=500, n_jobs=-1)

#### Variables Set ####
# define variables for the classification
variables = ['VVMin','VHMin','VVdivVHMin','VVMax','VHMax','VVdivVHMax','VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd','SELAvg','SELMax']
classParameters = {'n_estimators':[10, 100, 500], 'max_features':[2, 3, 4]}
gsearch = GridSearchCV(ExtraTreesClassifier(bootstrap = True), classParameters)
classifier = classratutils.findClassifierParameters(outputClumps,  classesIntCol, variables,  preProcessor=None, gridSearch=gsearch)


# define the output colours
classColours = dict()
classColours['Other'] = [212,125,83]
classColours['Water'] = [157,212,255]
classColours['VegWater'] = [191,255,0]



# run the classification
############################################################################################  run thorugh mulitple classifications and store result in RAT

runs=numpy.arange(1,51)
for i in runs:
	# define output class column
	outColInt='OutClass_'+str(i)
	print('')
	print('......processing: ' + outColInt)
	print('')
	# rebalance the training data
	classesIntCol = 'ClassInt'
	rsgislib.classification.classratutils.balanceSampleTrainingRandom(outputClumps, classesIntCol, 'classesIntColBal', 50, 5000)
	classesIntCol='classesIntColBal'
	# run the classifier
	classratutils.classifyWithinRAT(outputClumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours,preProcessor=MaxAbsScaler(),outColInt=outColInt)

############################################################################################ Read all results from RAT and extract mode, providing final result
# Open RAT
inRatFile = outputClumps
ratDataset = gdal.Open(inRatFile, gdal.GA_Update)
 
# define column names for output classifications
runs=numpy.arange(1,51)
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

names=[]
for i in mode_cert:
	if i==1:
		names.append('Water')
	elif i==2:
		names.append('Other')
	elif i==3:
		names.append('VegWater')

# write columns to RAT
rios.rat.writeColumn(outputClumps, 'OutClass_mode_pc', x_percent, colType=gdal.GFT_Real)
rios.rat.writeColumn(outputClumps, 'OutClass_mode_cert', mode_cert, colType=gdal.GFT_Integer)
rios.rat.writeColumn(outputClumps, 'OutClass_mode_cert_names', names, colType=gdal.GFT_String)

############################################################################################ # Random forests ranks parameters in terms of importance to the classifier
# there is a lot which can be learnt here...
'''
print('Feature importance: ' + inputImg)
featImportances = classifier.feature_importances_
featIndices = numpy.argsort(featImportances)[::-1]
# Print the feature ranking
print("Feature ranking:")
for f in range(len(variables)):
	print("\t{0}. {1} ({2})".format(f + 1, variables[featIndices[f]], featImportances[featIndices[f]]))
'''
############################################################################################



# export rat column: mode with certainty to image

gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8INT
fields = ['OutClass_mode_cert']

rastergis.exportCols2GDALImage(outputClumps, outimage, gdalformat, datatype, fields)



os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stam
