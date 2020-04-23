import gdal, glob

#inImg='S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee.tif'

imgList=glob.glob('*_lee.tif')
imgList=sorted(imgList)

for inImg in imgList:

	ds1 = gdal.Open(inImg)
	stats = ds1.GetRasterBand(1).GetStatistics(0,1)

	name=inImg.split('_')[4]

	print('Mean ' + name + ': ' + str(stats[2]))

	ds1=None