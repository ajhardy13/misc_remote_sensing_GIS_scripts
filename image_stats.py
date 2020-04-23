import rsgislib, glob
from rsgislib import imageutils

listFiles=glob.glob('*20180101T082329_20180101T084222_T34LGH.tif')
#inputImage='Fractions_and_Class_MARCH_2017_18.tif'
for inputImage in listFiles:
	imageutils.popImageStats(inputImage, False,0,True)
	

