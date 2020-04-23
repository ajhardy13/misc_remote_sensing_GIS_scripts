
import rsgislib, time
from rsgislib.segmentation import segutils, rastergis
from rsgislib import imageutils

start = time.time()

inputImage='S1B_IW_GRDH_1SDV_20180524_stack_lee.tif'

outputClumps='test_not_gridded_clumps2.kea'
outputMeanImg='test_not_gridded_clumps2_mean.kea'

segutils.runShepherdSegmentation(inputImage, outputClumps, outputMeanImg, minPxls=100)
bandList=['VV','VH','VVdivVH']  
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
rastergis.populateStats(outputClumps, True, True, True, 1)
rastergis.populateStats(outputMeanImg, True, True, True, 1)

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp