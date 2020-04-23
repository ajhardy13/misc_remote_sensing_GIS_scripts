from rsgislib.classification import classimgutils
from rsgislib import imageutils

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import GridSearchCV

imageBandInfo=[imageutils.ImageBandInfo('/Users/Andy/Documents/Mozambique/remote_sensing/planet/20190405_SR/planet_20190405_SR_cloudmask.tif', 'Planet', [1,2,3,4])]

classInfo=dict()
classInfo['urban_commercial'] = classimgutils.ClassInfoObj(id=11, fileH5='./urban_commercial.shp', red=204, green=204, blue=204)
classInfo['urban_dense'] = classimgutils.ClassInfoObj(id=12, fileH5='./urban_dense.shp', red=102, green=102, blue=102)
classInfo['urban_sparse'] = classimgutils.ClassInfoObj(id=13, fileH5='./urban_sparse.shp', red=153, green=153, blue=153)
classInfo['water_open'] = classimgutils.ClassInfoObj(id=21, fileH5='./water_open.shp', red=51, green=102, blue=255)
classInfo['water_turbid'] = classimgutils.ClassInfoObj(id=22, fileH5='./water_urban.shp', red=51, green=102, blue=153)
classInfo['cloud'] = classimgutils.ClassInfoObj(id=31, fileH5='./cloud.shp', red=255, green=255, blue=255)
classInfo['cloud_shadow'] = classimgutils.ClassInfoObj(id=32, fileH5='./cloud_shadow.shp', red=0, green=0, blue=0)
classInfo['vegetation_inundated'] = classimgutils.ClassInfoObj(id=41, fileH5='./vegetation_inundated.shp', red=0, green=102, blue=0)
classInfo['vegetation_photosynthetic'] = classimgutils.ClassInfoObj(id=42, fileH5='./vegetation_photosynthetic.shp', red=153, green=255, blue=102)
classInfo['sediment_sand'] = classimgutils.ClassInfoObj(id=51, fileH5='./sediment_sand.shp', red=255, green=255, blue=102)
classInfo['sediment_mud'] = classimgutils.ClassInfoObj(id=52, fileH5='./sediment_mud.shp', red=153, green=102, blue=0)


skClassifier=ExtraTreesClassifier(n_estimators=20)

#classimgutils.performPerPxlMLClassShpTrain(imageBandInfo, classInfo, outputImg='planet_20190405_SR_classified.kea', gdalFormat='KEA', tmpPath='./tmp', skClassifier=skClassifier)
classimgutils.performPerPxlMLClassShpTrain(imageBandInfo, outputImg='planet_20190405_SR_classified.kea', gdalformat='KEA', tmpPath='./tmp', skClassifier=skClassifier)



