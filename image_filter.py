import rsgislib
from rsgislib import imagefilter, imageutils, rastergis

# read and filter image
print('Filtering image...')
inputImage='/Users/Andy/Documents/Zanzibar/Jun16_visit/UAV_data/Mwera_2/ortho_mwera_2.tif'
outputImage='/Users/Andy/Documents/Zanzibar/Jun16_visit/UAV_data/Mwera_2/ortho_mwera_2_median9x9.tif'
#imagefilter.applyLeeFilter(inputImage, outputImage, 9, 9, "GTiff", rsgislib.TYPE_32FLOAT)
imagefilter.applyMedianFilter(inputImage, outputImage, 9, "GTiff", rsgislib.TYPE_32FLOAT)

# bandList=['VV','VH','VVdivVH']
# rsgislib.imageutils.setBandNames(outputImage, bandList)
# rastergis.populateStats(outputImage, True, True, True, 1)
