import rsgislib
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn

def bandMath(inputImage1,inputImage2,outputImage):
	gdalformat = 'GTiff'
	datatype = rsgislib.TYPE_32FLOAT
	expression = 'b1/b2'
	bandDefns = []
	bandDefns.append(BandDefn('b1', inputImage1, 1))
	bandDefns.append(BandDefn('b2', inputImage2, 1))
	imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

# bandMath(inputImage1,inputImage2,outputImage)
