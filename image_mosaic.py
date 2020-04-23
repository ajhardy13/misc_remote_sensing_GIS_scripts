import rsgislib
from rsgislib import imageutils
import glob

# Search for all files with the extension 'kea'
inputList = glob.glob('/Users/Andy/Documents/Tanzania/Landsat/Outputs/*toa.tif')
outImage = '/Users/Andy/Documents/Tanzania/Landsat/Outputs/Mosaic/LS8_mosaic.kea'
backgroundVal = 0.0
skipVal = 0.0
skipBand = 1
overlapBehaviour = 0
gdalformat = 'KEA'
datatype = rsgislib.TYPE_32FLOAT
imageutils.createImageMosaic(inputList, outImage, backgroundVal, skipVal, skipBand, overlapBehaviour, gdalformat, datatype)
