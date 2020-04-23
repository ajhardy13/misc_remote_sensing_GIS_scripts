import rsgislib, re, glob
from rsgislib import imageutils

# define list of input classified images
imageList=glob.glob('*sel_lt15dB.kea')


imageList =sorted(imageList)

# snap to common grid
for img in imageList[1:len(imageList)]:
	print('')
	print('Processing: ' + img)
	print('')
	imgOut=img.replace('.kea','_snapped.kea')
	inRefImg=imageList[0] # base raster to snap to
	gdalFormat = 'kea'
	rsgislib.imageutils.resampleImage2Match(inRefImg, img, imgOut, gdalFormat, interpMethod='nearestneighbour', datatype=rsgislib.TYPE_8INT) # perform resampling/snap

# list snapped images
imageList=glob.glob('*sel_lt15dB_snapped.kea')
imageList =sorted(imageList)

# stack images
bandNamesList = []

for img in imageList:
	date=img.split('_')[4].split('T')[0]
	bandNamesList.append('b'+date)

outputImage = 'sel_lt15dB_stack_2017.kea'
gdalformat = 'KEA'
gdaltype = rsgislib.TYPE_8INT
imageutils.stackImageBands(imageList, bandNamesList, outputImage, None, 0, gdalformat, gdaltype)