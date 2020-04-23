import rsgislib
from rsgislib import imageutils
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from skimage import filters



inImg = '26-09-2017_S1_lee.tif'


gdalformat='KEA'
datatype=rsgislib.TYPE_32FLOAT

#mask the original stacked S1 image using open water training
outImg = inImg.replace('.tif','_wbtrain_mask.kea')
imgMask = 'seasonality_barotseland_snapped_20170926T165722_clump_m18dB.tif'
rsgislib.imageutils.maskImage(inImg, imgMask, outImg, gdalformat, datatype, 0, [0])
imageutils.popImageStats(outImg, True, 0.0, True)


#mask the original stacked S1 image using open water prediction
imgMask='26-09-2017_S1_lee_classified.kea'
outImg = inImg.replace('.tif','_unrefinedclass_mask.kea')
rsgislib.imageutils.maskImage(inImg, imgMask, outImg, gdalformat, datatype, 0, [0,2,3])
imageutils.popImageStats(outImg, True, 0.0, True)




trainImage=inImg.replace('.tif','_wbtrain_mask.kea')
maskImage=inImg.replace('.tif','_unrefinedclass_mask.kea')

####################################################################
#histogram for VV band
ds1 = gdal.Open(trainImage)
trainVV = np.array(ds1.GetRasterBand(1).ReadAsArray())
trainVV = trainVV.flatten()
trainVV[trainVV == 0] = 'nan'
ds1=None

ds2 = gdal.Open(maskImage)
maskVV = np.array(ds2.GetRasterBand(1).ReadAsArray())
maskVV = maskVV.flatten()
maskVV[maskVV == 0] = 'nan'
ds2=None

plt.hist(trainVV[~np.isnan(trainVV)], bins=120, alpha=0.5, color='Blue',density=True, label='Training')
plt.hist(maskVV[~np.isnan(maskVV)], bins=120, alpha=0.5, color='Black', density=True, label='Other')

plt.legend(loc='upper right')
plt.xlabel('Backscatter (dB)')
plt.ylabel('Normalised Probality Density (0-1)')

plt.show()
'''
####################################################################
#histogram for VVdivVH band
ds1 = gdal.Open(trainImage)
trainVV = np.array(ds1.GetRasterBand(3).ReadAsArray())
trainVV = trainVV.flatten()
trainVV[trainVV == 0] = 'nan'
ds1=None

ds2 = gdal.Open(maskImage)
maskVV = np.array(ds2.GetRasterBand(3).ReadAsArray())
maskVV = maskVV.flatten()
maskVV[maskVV == 0] = 'nan'
ds2=None

plt.hist(trainVV[~np.isnan(trainVV)], bins=60, alpha=0.5, color='Blue',normed=True, label='Training')
plt.hist(maskVV[~np.isnan(maskVV)], bins=60, alpha=0.5, color='Black', normed=True, label='Other')

plt.legend(loc='upper right')
plt.xlabel('VV/VH ratio')

plt.show()

####################################################################
#histogram for VH band
ds1 = gdal.Open(trainImage)
trainVV = np.array(ds1.GetRasterBand(2).ReadAsArray())
trainVV = trainVV.flatten()
trainVV[trainVV == 0] = 'nan'
ds1=None

ds2 = gdal.Open(maskImage)
maskVV = np.array(ds2.GetRasterBand(2).ReadAsArray())
maskVV = maskVV.flatten()
maskVV[maskVV == 0] = 'nan'
ds2=None

plt.hist(trainVV[~np.isnan(trainVV)], bins=60, alpha=0.5, color='Blue',normed=True, label='Training')
plt.hist(maskVV[~np.isnan(maskVV)], bins=60, alpha=0.5, color='Black', normed=True, label='Other')

plt.legend(loc='upper right')
plt.xlabel('Backscatter (dB)')

plt.show()
'''
####################################################################
#extract otsu threshold from VV band
'''
from skimage import data, filters
from skimage.filters import try_all_threshold

ds1 = gdal.Open(maskImage)
maskVV = np.array(ds1.GetRasterBand(1).ReadAsArray())
maskVV[maskVV == 0] = 'nan'

threhsolds=[]
thresholds.append(filters.threshold_otsu(maskVV))
'''
#imgBand=1
#binWidth=0.25
#inMin=-25
#inMax=-16
#train=rsgislib.imagecalc.getHistogram(trainImage, imgBand, binWidth, False, inMin, inMax)
#mask=rsgislib.imagecalc.getHistogram(maskImage, imgBand, binWidth, False, inMin, inMax)
#
#imgBand=3
#binWidth=0.01
#inMin=0.68
#inMax=0.95
#trainVVdivVH=rsgislib.imagecalc.getHistogram(trainImage, imgBand, binWidth, False, inMin, inMax)
#maskVVdivVH=rsgislib.imagecalc.getHistogram(maskImage, imgBand, binWidth, False, inMin, inMax)
#
#
#import matplotlib
#import matplotlib.pyplot as plt
#
#plt.plot(train[0])
#plt.plot(mask[0])