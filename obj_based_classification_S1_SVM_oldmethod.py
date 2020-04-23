import rsgislib, os
from rsgislib import imageutils, rastergis
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm
from rsgislib.classification import classimgutils, classratutils

inputImg = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3.kea'
outputClumps='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_clumps2.kea'
outputMeanImg = inputImg.split('.')[0]+'_clumps_mean.'+inputImg.split('.')[1]

# 
# 
# run segmentation
# 
# 
print('Performing the segmentation...')
segutils.runShepherdSegmentation(inputImg, outputClumps, outputMeanImg, minPxls=100)
imageutils.popImageStats(outputClumps,True,0.,True)
# populate RAT with mean stats from  S1
clumps=outputClumps # rename clumps image
ratutils.populateImageStats(inputImg, clumps, calcMean=True, calcStDev=True)


# populate clumps with training data
print('Populating clumps with stats...')
classesDict = dict()
classesDict['Water'] = [1, '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_m18dB_20170704.shp']
tmpPath = './temp'
classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'
ratutils.populateClumpsWithClassTraining(clumps, classesDict, tmpPath, classesIntCol, classesNameCol)

# 
# 
# classify the image
# 
# 
# define the classifier
# 
from rios import rat
import osgeo.gdal as gdal
import numpy as np

# Open RAT
inRatFile = clumps
ratDataset = gdal.Open(clumps, gdal.GA_Update)
 
# Set column names
x_col_names = ['VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd']
# x_col_names = ['VVAvg','VHAvg', 'VVStd','VHStd']
y_col_name = 'ClassInt'
 
# Set up list to hold data
X = []
 
# Read in data from each column
print('read data')
for colName in x_col_names:
    X.append(rat.readColumn(ratDataset, colName))
 
# Read in training data
print('read training data')
y = rat.readColumn(ratDataset, y_col_name) 
# Set NA values to 0
y = np.where(y == b'NA',0,y)
y = y.astype(np.int16)
 
X.append(y)
 
X = np.array(X)
X = X.transpose()
 
# Remove rows with 0 (NA) for wetCode
X_train = X[X[:,-1] != 0]
 
# Remove non-finite values
X_train = X_train[np.isfinite(X_train).all(axis=1)]
 
# Split into variables (X) and class (y)
y_train = X_train[:,-1]
X_train = X_train[:,0:-1]
 
# Train CSV classifier
print('define clf')
# clf= svm.OneClassSVM(kernel='rbf',nu=0.2,gamma='auto',verbose=False)
clf= svm.OneClassSVM(kernel='poly',nu=0.1,gamma='auto',verbose=True)

print('fit clf')
clf.fit(X_train, y_train)
 
# Set NaN values to 0
X = np.where(np.isfinite(X),X,0)
 
# Apply classification
print('apply classification ')
predictClass = clf.predict(X[:,0:-1])
 
# Write out data to RAT
print('write RAT')
rat.writeColumn(ratDataset, 'predictClass', predictClass)
ratDataset = None

outimage='S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_clumps2_classified_ploynu01.tif'
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8INT
fields = ['predictClass']
print('export cols')
rastergis.exportCols2GDALImage(clumps, outimage, gdalformat, datatype, fields)


'''
classifier = svm.SVC(kernel='rbf',gamma='auto',verbose=True)

# define the output colours
classColours = dict()
classColours['Water'] = [157,212,255]



# define input variables 
variables = ['VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd']

# run the classification
print('Running the classifier...')
classratutils.classifyWithinRAT(clumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours)

# export rat column to image
outimage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee3_testAOI_clumps2_classified.kea'
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8INT
fields = ['OutClass']
rastergis.exportCols2GDALImage(clumps, outimage, gdalformat, datatype, fields)

# export as shapefile
# inputImg=outimage
# outShp='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_classified_v2.shp'
# rsgislib.vectorutils.polygoniseRaster(inputImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)
'''