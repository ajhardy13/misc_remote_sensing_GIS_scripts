import rsgislib, os
from rsgislib import imageutils
from rsgislib import vectorutils
from rsgislib.classification import classimgutils
from sklearn.ensemble import ExtraTreesClassifier

inputImg = 'ortho_mwera_2_RGB.tif'

# output classified image
outimage=inputImg.replace('.tif','_svm_water.kea')

# generate img mask to perform classificaiton over
validImgMsk = 'ortho_mwera_2_RGB_mask.tif'
imageutils.genValidMask(inputImg, validImgMsk, 'KEA', 0.0)

# define the input image for the classification
imageBandInfo=[imageutils.ImageBandInfo(inputImg, 'droneRGB', [1,2,3])]


# define training data
vectorutils.rasterise2Image('ortho_mwera_2_RGB_training_WET.shp', inputImg, 'ortho_mwera_2_RGB_training_WET.kea', gdalformat='KEA', burnVal=1)
vectorutils.rasterise2Image('ortho_mwera_2_RGB_training_DRY.shp', inputImg, 'ortho_mwera_2_RGB_training_DRY.kea', gdalformat='KEA', burnVal=2)

# Extract the training data to HDF files.
imageutils.extractZoneImageBandValues2HDF(imageBandInfo, 'ortho_mwera_2_RGB_training_WET.kea', 'ortho_mwera_2_RGB_training_WET.h5', 1.0)
imageutils.extractZoneImageBandValues2HDF(imageBandInfo, 'ortho_mwera_2_RGB_training_DRY.kea', 'ortho_mwera_2_RGB_training_DRY.h5', 2.0)

# Define the classes to be classified with the training data (HDF5 file) and colour
classTrainInfo=dict()
classTrainInfo['Water'] = classimgutils.ClassInfoObj(id=1, fileH5='ortho_mwera_2_RGB_training_WET.h5', red=133, green=186, blue=255)
classTrainInfo['Non-Water'] = classimgutils.ClassInfoObj(id=2, fileH5='ortho_mwera_2_RGB_training_DRY.h5', red=166, green=97, blue=26)

# Create scikit-learn classifier and train
skClassifier=ExtraTreesClassifier(n_estimators=20)
classimgutils.trainClassifier(classTrainInfo, skClassifier)

# apply the classifier
classimgutils.applyClassifer(classTrainInfo, skClassifier, validImgMsk, 1, imageBandInfo, outimage, 'KEA')


os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')
