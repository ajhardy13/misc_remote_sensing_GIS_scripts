import rsgislib
from rsgislib import imageutils, rastergis
from rsgislib.segmentation import segutils
from rsgislib.rastergis import ratutils
from rios import rat
import osgeo.gdal as gdal
import numpy as np
from sklearn import svm

inImg = 'S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee.tif'
imgMask = inImg.replace('.tif','_clumps2_erf_clumptrain_mode.tif')
outImg = inImg.replace('.tif','_wb_mask.kea')

outimage=outImg.replace('.kea','_openwater.kea')

waterMask='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped_'+inImg.split('/')[-1].split('_')[4]+'_m18dB.shp'

gdalformat='KEA'
datatype=rsgislib.TYPE_32FLOAT

#mask the original stacked S1 image using open water prediction
#rsgislib.imageutils.maskImage(inImg, imgMask, outImg, gdalformat, datatype, 0, [2,3])
#imageutils.popImageStats(outImg, True, 0.0, True)

inImg=outImg

clumps=outImg.replace('.kea','_clumps2.kea')
clumpsMean=outImg.replace('.kea','_clumps2_mean_test.kea')

#segment image and add stats from S1 image
segutils.runShepherdSegmentation(inImg, clumps, clumpsMean, minPxls=100, numClusters=5)
bandList=['VV','VH','VVdivVH']
rsgislib.imageutils.setBandNames(inImg, bandList)
ratutils.populateImageStats(inImg, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)

# populate clumps with training data
print('Populating clumps with stats...')
classesDict = dict()
classesDict['OpenWater'] = [1, waterMask]
tmpPath = './temp'
classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'
ratutils.populateClumpsWithClassTraining(clumps, classesDict, tmpPath, classesIntCol, classesNameCol)

################################################################
# Open RAT
inRatFile = clumps
ratDataset = gdal.Open(clumps, gdal.GA_Update)
 
# Set column names
x_col_names = ['VVAvg','VHAvg','VVdivVHAvg', 'VVStd','VHStd','VVdivVHStd','VVAvg','VHAvg','VVdivVHAvg', 'VVMin','VHMin','VVdivVHMin','VVMax','VHMax','VVdivVHMax']
x_col_names = ['VVAvg','VHAvg','VVdivVHAvg']
# x_col_names = ['VVAvg','VHAvg', 'VVStd','VHStd']
y_col_name = 'ClassInt'
 
# Set up list to hold data
X = []
 
# Read in data from each column
print('read data')
for colName in x_col_names:
    X.append(rat.readColumn(ratDataset, colName))

#function to implement single class svm classifier

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
#clf= svm.OneClassSVM(kernel='rbf',nu=0.2,gamma='auto',verbose=False)
clf= svm.OneClassSVM(kernel='rbf',gamma='auto',verbose=True)
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

# write the output file ---------------------------
gdalformat = 'KEA'
datatype = rsgislib.TYPE_8INT
fields = ['predictClass']
print('export cols...')
rastergis.exportCols2GDALImage(clumps, outimage, gdalformat, datatype, fields)