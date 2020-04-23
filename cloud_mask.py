import rsgislib, glob, os
from rsgislib import imageutils


# for use with planet data where udm file is provided witha  cloud mask


listSR=sorted(glob.glob('*MS_SR.tif'))

gdalformat='KEA'
datatype=rsgislib.TYPE_16UINT


for img in listSR:
	udm = img.replace('SR.tif','DN_udm.tif')
	cloudimg = img.replace('.tif','_cloudmask.kea')
	rsgislib.imageutils.maskImage(img, udm, cloudimg, gdalformat, datatype, 0, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100])



