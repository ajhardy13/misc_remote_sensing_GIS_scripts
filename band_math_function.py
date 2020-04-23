import rsgislib
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn
from numba import jit

inputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/S2_composite_aug_sep_2017.tif'
outputImage=inputImage.replace('.tif','_ndwi.tif')

@jit
def bandMath(inputImage,outputImage):
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_32FLOAT
	expression = '(g-nir)/(g+nir)'
#	expression = '(nir-r)/(nir+r)'
	bandDefns = []
	bandDefns.append(BandDefn('g', inputImage, 4))
	bandDefns.append(BandDefn('r', inputImage, 3))
	bandDefns.append(BandDefn('nir', inputImage, 2))
	bandDefns.append(BandDefn('swir', inputImage, 1))
	imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)
	
bandMath(inputImage,outputImage)