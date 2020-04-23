import glob, rsgislib
from rsgislib import rastergis



listImages=glob.glob('*20170129T165721*_lee.tif')

for inputImg in listImages:

	# input clumps
	outputClumps=inputImg.split('.')[0]+'_clumps2.kea' 

	# output classified image
	outimage='./Out/'+inputImg.split('.')[0]+'_clumps2_erf_clumptrain.tif'

	# export rat column to image

	fields = ['OutClass']
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_8INT

	rastergis.exportCols2GDALImage(outputClumps, outimage, gdalformat, datatype, fields)