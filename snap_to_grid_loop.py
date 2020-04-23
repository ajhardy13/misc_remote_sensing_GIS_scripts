import rsgislib, glob
from rsgislib import imageutils

# input folder with datasets to process
infolder='/Users/Andy/Documents/TEACHING/Lectures/EAM2920 - issues/Public Health/Practicals/Data/Datasets/'

# base raster to snap to
inRefImg='/Users/Andy/Documents/TEACHING/Lectures/EAM2920 - issues/Public Health/Practicals/Data/Landsat8_composite_zbar.tif'

# list .tif images in the input folder
imageList=glob.glob(infolder+'*.tif')

# loop round .tif images in the input folder
for inImg in imageList:
	# define output filename based on input plus '_snap'
	outImg=inImg.split('.tif')[0]+'_snap.tif'
	# perform resampling/snap
	gdalFormat = 'GTiff'
	rsgislib.imageutils.resampleImage2Match(inRefImg, inImg, outImg, gdalFormat, interpMethod='nearestneighbour', datatype=None)