import rsgislib, os, gdal, time, subprocess
from rsgislib import imageutils, rastergis
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn import svm
from rsgislib.classification import classimgutils, classratutils
from sklearn.preprocessing import MaxAbsScaler

start = time.time()

'''
inputImg = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3.tif'
outputClumps='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3_clumps2.kea'
outputMeanImg = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3_clumps_mean.kea'
# output classified image
outimage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee3_clumps2_classified_multi_svm_balanced_allstats_wetveg.tif'
'''
inputImg = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20171020T165722_Sigma0_stack_lee.tif'
outputClumps=inputImg.split('.')[0]+'_clumps2.kea'
outputMeanImg = inputImg.split('.')[0]+'_clumps2_mean.kea'
# output classified image
outimage=inputImg.split('.')[0]+'_clumps2_classified_multi_svm_balanced_allstats_wetveg.tif'

otherMask='/Users/Andy/Documents/Zambia/FloodModelling/Data/DEMs/SRTM/barotseland_srtm_utm_lee_slope_mask_wgs84.shp'
waterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped_20171020T165722_m18dB.shp'
combinedMask=waterMask.split('.')[0]+'_slope.shp'
vegwaterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped_20171020T165722_wetveg.shp'
'''
# run segmentation ---------------------------
print('Performing the segmentation...')

segutils.runShepherdSegmentation(inputImg, outputClumps, outputMeanImg, minPxls=100)
gdalformat = 'KEA'


bandList=['VV','VH','VVdivVH']

rsgislib.imageutils.setBandNames(inputImg, bandList)
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
# rastergis.populateStats(outputMeanImg, True, True, True, 1)


# populate RAT with mean stats from  S1
clumps=outputClumps # rename clumps image

ratutils.populateImageStats(inputImg, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)

'''

# imageutils.popImageStats(outputClumps,True,0.,True)
# imageutils.popImageStats(outputMeanImg,True,0.,True)

# merge 'other' and 'open water' masks to act as non-veg water training
print("Creating training mask for 'other' regions...") 
cmd="ogr2ogr -f 'ESRI Shapefile' '%s' '%s'" %(combinedMask, otherMask)
subprocess.call(cmd, shell=True)
# cmd="ogr2ogr -f 'ESRI Shapefile' -update -append '%s' '%s' -nln merge" %(combinedMask, waterMask)
cmd="ogr2ogr -f 'ESRI Shapefile' -update -append '%s' '%s'" %(combinedMask, waterMask)
subprocess.call(cmd, shell=True)

# populate clumps with training data
print('Populating clumps with stats...')
classesDict = dict()
classesDict['Other'] = [2, combinedMask]  
classesDict['VegWater'] = [3, vegwaterMask]

tmpPath = './temp'

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
# classColours['Water'] = [157,212,255]
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
