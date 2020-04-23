import rsgislib
from rsgislib.segmentation import skimgseg

inputImg="/Users/Andy/Documents/Zanzibar/Jun16_visit/UAV_data/computer_vision/ortho_mwera_2_RGB.tif"
inputImg="/data/computer_vision/ortho_mwera_2_RGB_reduced.tif"
outputImg=inputImg.replace('.tif','_slic.kea')

rsgislib.segmentation.skimgseg.performSlicSegmentation(inputImg, outputImg,gdalformat='KEA', noDataVal=0, n_segments=3000, compactness=10, sigma=5, convert2lab=True)

