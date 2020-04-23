import rsgislib
from rsgislib import classification


# input classified image
stamp='20170610T165717'
inputImage='S1B_IW_GRDH_1SDV_'+stamp+'_Sigma0_stack_lee_clumps2.kea'
# output point shapefile
outputShp='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/2017/Out/Accuracy_Assess/acc_assessment_mode_'+stamp+'.shp'

# input bounding: shp or img
#boundshp='/Users/Andy/Documents/Zambia/RemoteSensing/Pleiades/pleiades_area.shp'
#boundimg='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/20170421T082011_20170421T084245_T34LGJ.tif'



##################################################################################
#outputimage='clipped_image.kea'
#rsgislib.imageutils.subset(inputImage, boundshp, outputimage, 'KEA', rsgislib.TYPE_8INT)
#rsgislib.imageutils.subset2img(inputImage, boundimg, outputimage, 'KEA', rsgislib.TYPE_8INT)

# define input and output columns
classImgCol='OutClass_mode_cert_names'
classImgVecCol='ClassName'
classRefVecCol='RefName'

rsgislib.classification.generateStratifiedRandomAccuracyPts(inputImage, outputShp, classImgCol, classImgVecCol, classRefVecCol, 500,10,True)

# clip the shapefile result
#ogr2ogr -clipsrc 22.98 -15.41 23.42 -15.05 outputShp outputShp -nlt POINT

# Generates a set of stratified random points for accuracy assessment.
# 
# Where:
# 
# inputImage is a string containing the name and path of the input image with attribute table.
# outputShp is a string containing the name and path of the output shapefile.
# classImgCol is a string speciyfing the name of the column in the image file containing the class names.
# classImgVecCol is a string specifiying the output column in the shapefile for the classified class names.
# classRefVecCol is a string specifiying an output column in the shapefile which can be used in the accuracy assessment for the reference data.
# numPts is an int specifying the number of points for each class which should be created.
# seed is an int specifying the seed for the random number generator. (Optional: Default 10)
# force is a bool, specifying whether to force removal of the output vector if it exists. (Optional: Default False)
