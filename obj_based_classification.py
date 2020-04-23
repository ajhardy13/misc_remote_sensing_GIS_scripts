import rsgislib, os
from rsgislib import imageutils, rastergis
from rsgislib.rastergis import ratutils
from rsgislib.segmentation import segutils
from sklearn.ensemble import ExtraTreesClassifier
from rsgislib.classification import classimgutils, classratutils

inputImg = '/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite.tif'
outputClumps = '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps.kea'
outputMeanImg = '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_mean.kea'
inputSARImg='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/S1A_20141014_tr.tif'
ndvi='/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite_ndvi.tif'
wbi='/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite_WBI.tif'

# run segmentation
# segutils.runShepherdSegmentation(inputImg, outputClumps, outputMeanImg, minPxls=100)

clumps=outputClumps # rename clumps image

# populate RAT with mean stats from landsat and S1
# ratutils.populateImageStats(inputImg, clumps, calcMean=True)
# ratutils.populateImageStats(inputSARImg, clumps, calcMean=True, calcStDev=True)
# ratutils.populateImageStats(ndvi, clumps, calcMean=True)
# ratutils.populateImageStats(wbi, clumps, calcMean=True)

# populate clumps with training data
classesDict = dict()
classesDict['FlatPasture'] = [1, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/flat_pasture.shp']
classesDict['Water'] = [2, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/water.shp']
classesDict['Agriculture'] = [3, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/agriculture.shp']
classesDict['Grassland'] = [4, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/grassland.shp']
classesDict['Forest'] = [5, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/forest.shp']
classesDict['Urban'] = [6, '/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/urban.shp']
tmpPath = './temp'
classesIntCol = 'ClassInt'
classesNameCol = 'ClassStr'
ratutils.populateClumpsWithClassTraining(clumps, classesDict, tmpPath, classesIntCol, classesNameCol)


# define the classifier
classifier = ExtraTreesClassifier(n_estimators=500, n_jobs=-1)

# define the output colours
classColours = dict()
classColours['FlatPasture'] = [212,125,83]
classColours['Water'] = [157,212,255]
classColours['Agriculture'] = [255,255,166]
classColours['Grassland'] = [200,255,187]
classColours['Forest'] = [132,200,76] 
classColours['Urban'] = [200,200,200] 


# define input variables 
variables = ['coastAvg', 'blueAvg', 'greenAvg', 'redAvg','NIRAvg', 'SWIR1Avg', 'SWIR2Avg','VVStd','wbiAvg','ndviAvg']

# run the classification
classratutils.classifyWithinRAT(clumps, classesIntCol, classesNameCol, variables, classifier=classifier, classColours=classColours)

# export rat column to image
outimage='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_classified.tif'
gdalformat = 'GTiff'
datatype = rsgislib.TYPE_8INT
fields = ['OutClass']
rastergis.exportCols2GDALImage(clumps, outimage, gdalformat, datatype, fields)

# export as shapefile
inputImg=outimage
outShp='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_classified_v2.shp'
# rsgislib.vectorutils.polygoniseRaster(inputImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)
