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

fileList=['S1B_IW_GRDH_1SDV_20170105T165713_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170423T165720_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170610T165717_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170728T165719_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170809T165720_Sigma0_stack_lee_clumps2.kea','S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee_clumps2.kea']

#fileList=['S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee_clumps2.kea']

for outputClumps in fileList:
	print('')
	print('......processing: '+ outputClumps)
	print('')
	
	outimage=outputClumps.replace('.kea','_erf_clumptrain_mode.tif')
	
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

	# where percentage match is less that 100% (both open water and wet veg), classify as dry
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
	
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_8INT
	fields = ['OutClass_mode_cert']

	rastergis.exportCols2GDALImage(outputClumps, outimage, gdalformat, datatype, fields)
