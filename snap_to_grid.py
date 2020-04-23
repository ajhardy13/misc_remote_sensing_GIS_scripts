import rsgislib, glob, os
from rsgislib import imageutils

listFiles=['/Users/Andy/Documents/Zanzibar/IVCC/SIS/Cluster_definition/Modelling/Modelling_Layers/Infiltration_TEST_mosaic_snap_mask.tif','/Users/Andy/Documents/Zanzibar/Data/Analysis/R/Rasters/Geology.tif','/Users/Andy/Documents/Zanzibar/Data/Analysis/R/Rasters/Landcover.tif']
#listFiles=glob.glob('*.tif')

#listFiles=glob.glob('*_otsu_snap_guf.kea')

# base raster to snap to
inRefImg='/Users/Andy/Documents/Zanzibar/IVCC/SIS/Cluster_definition/Modelling/Modelling_Layers/GMW_znz.tif'

for inProcessImg in listFiles:
	# input raster
	#inProcessImg='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/Barotseland-Zambia04.tif'
	#outImg='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped.tif'
	
	outImg='./snapped/'+os.path.basename(inProcessImg).replace('.tif','_snap.tif')
	
	# perform resampling/snap
	gdalFormat = 'GTiff'
#	rsgislib.imageutils.resampleImage2Match(inRefImg, inProcessImg, outImg, gdalFormat,interpMethod='nearestneighbour', datatype=None)
	try:
		rsgislib.imageutils.resampleImage2Match(inRefImg, inProcessImg, outImg, gdalFormat,interpMethod='nearestneighbour', datatype=rsgislib.TYPE_16INT)
	except:
		print('Failed: '+ outImg)
		pass


