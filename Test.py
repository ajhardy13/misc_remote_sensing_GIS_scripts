import rsgislib
from rsgislib import imagefilter, segmentation
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils

inputImage = 'S1B_20170728_stack_lee_clip.kea'
outImgFile = 'S1B_20170728_stack_lee_clip_txt23.kea'
datatype='rsgislib.TYPE_32FLOAT'
#imagefilter.applyStdDevFilter(inputImage, outImgFile, 33, "KEA", rsgislib.TYPE_32FLOAT)
#imagefilter.applyCoeffOfVarFilter(inputImage, outImgFile, 9, "KEA", rsgislib.TYPE_32FLOAT)
#imagefilter.applyRangeFilter(inputImage, outImgFile, 9, "KEA", rsgislib.TYPE_32FLOAT)
rsgislib.imagefilter.applyTextureVarFilter(inputImage, outImgFile, 23, "KEA", rsgislib.TYPE_32FLOAT)






clumpsImage='S1B_20170728_cumps_mean_clip.kea'
spectralImage='S1B_20170728_stack_lee_clip.kea'
outputClumps='S1B_20170728_cumps_mean_clip_clmpMerge.kea'
rsgislib.segmentation.mergeSegments2Neighbours(clumpsImage, spectralImage, outputClumps, rsgislib.TYPE_32FLOAT)

outputClumps=inputImage.split('.')[0]+'_clumps2.kea'
outputMeanImg = inputImage.split('.')[0]+'_clumps2_mean.kea'

inputImage = 'S1B_20170728_stack_lee_clip.kea'
outputClumps = 'S1B_20170728_stack_lee_clip_clumps2_clust5.kea'
outputMeanImg = 'S1B_20170728_stack_lee_clip_clumps_clust5_mean.kea'




segutils.runShepherdSegmentation(inputImage, outputClumps, outputMeanImg, minPxls=100, numClusters=5)

# set output band names
bandList=['VV','VH','VVdivVH']

rsgislib.imageutils.setBandNames(inputImage, bandList)
rsgislib.imageutils.setBandNames(outputMeanImg, bandList)
# rastergis.populateStats(outputMeanImg, True, True, True, 1)


# populate RAT with mean stats from  S1
clumps=outputClumps # rename clumps image

ratutils.populateImageStats(inputImage, clumps, calcMin=True,calcMax=True,calcMean=True, calcStDev=True)