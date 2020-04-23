import rsgislib, gdal
from rsgislib import rastergis
import numpy as np
from rsgislib.rastergis import ratutils

clumps='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_testAOI2_gridclumps2_100.kea'
outimage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_testAOI2_gridclumps2_100_classified.tif'
outTestimage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee3_testAOI2_gridclumps2_100_test.tif'

# testShp='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_m18dB_20170704_train.shp'

# populate clumps with test data
print('Populating clumps with test data...')

fields=['predictClass','ClassRefInt']
outfile='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/test.csv'
# rastergis.export2Ascii(clumps, outfile, fields)

classified,test=np.loadtxt(outfile,delimiter=',',usecols=[1,2],unpack=True,skiprows=1)

numclass=[]
numtest=[]
for c, t in zip(classified,test):
	if c == t:
		if t == c:
			numclass.append(1)
		else:
			numclass.append(0)
	else:
		numclass.append(-1)

for t in test:
	if t==1:
		numtest.append(1)
	else:
		numtest.append(0)

posclass=numclass.count(1)
postest=numtest.count(1)
truepos=(posclass/postest)*100
print('True positive: '+str("%.2f" %truepos)+'%')


'''
classesDict = dict()
classesDict['Water'] = [1, '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/watermask_barotseland_m18dB_20170704_train.shp']
tmpPath = './temp'
classesIntCol = 'ClassRefInt'
classesNameCol = 'ClassRefStr'
# ratutils.populateClumpsWithClassTraining(clumps, classesDict, tmpPath, classesIntCol, classesNameCol)

datatype = rsgislib.TYPE_8INT
fields=['predictClass']
# rsgislib.rastergis.exportCols2GDALImage(clumps, outimage, 'GTiff', 
# 	datatype, fields, ratband=1, tempDIR=None)
'''

'''	
fields=['ClassRefInt']
rsgislib.rastergis.exportCols2GDALImage(clumps, outTestimage, 'GTiff', 
	datatype, fields, ratband=1, tempDIR=None)
	

classImage=gdal.Open(outimage)
classified=np.array(classImage.GetRasterBand(1).ReadAsArray())
classified.flatten()
testImage=gdal.Open(outTestimage)
test=np.array(testImage.GetRasterBand(1).ReadAsArray())
test.flatten()

truePos=[]
for cls, tst in zip(classified,test):
	truePos.append(cls+tst)
'''	
	