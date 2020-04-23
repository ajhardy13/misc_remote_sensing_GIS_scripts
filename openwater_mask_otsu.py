import rsgislib, argparse, sys
from rsgislib.segmentation import segutils
from rsgislib import imageutils, imagecalc
from rsgislib.imagecalc import BandDefn
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from skimage import filters
from scipy.stats import skew



#inImg = 'S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee.tif'
###################
# definition of arguments
parser = argparse.ArgumentParser(prog='Implement open water refinement', description='Refines open water prediciton using Otsu threholding.')
parser.add_argument('-i', metavar='', type=str, help='Path to the input image, i.e. original stacked image *_stack_lee.tif.')
args = parser.parse_args()
# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')
##############################################################################################

##############################################################################################	
inputImage=args.i
print('')
print('Input image: ' + inputImage)
print('')
##############################################################################################

inImg=inputImage
imgMask = inImg.replace('.tif','_clumps2_erf_clumptrain_mode.tif')
outImg = inImg.replace('.tif','_wb_mask.kea')
classification=inImg.replace('.tif','_clumps2_erf_clumptrain_mode.tif')
outClass=classification.replace('.tif','_std.kea')

gdalformat='KEA'
datatype=rsgislib.TYPE_32FLOAT

clumps=outImg.replace('.kea','_clumps2.kea')
clumpsMean=outImg.replace('.kea','_clumps2_mean.kea')

# base raster to snap to
inRefImg='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/seasonality_barotseland_snapped.tif'
outImg=outClass.replace('.tif','_snap.kea')

guf='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped.tif'

#mask the original stacked S1 image using open water prediction
#rsgislib.imageutils.maskImage(inImg, imgMask, outImg, gdalformat, datatype, 0, [2,3])
#imageutils.popImageStats(outImg, True, 0.0, True)

#segment image and add stats from S1 image
inImg=outImg
#segutils.runShepherdSegmentation(inImg, clumps, clumpsMean, minPxls=100, numClusters=5)
#bandList=['VV','VH','VVdivVH']
#rsgislib.imageutils.setBandNames(inImg, bandList)

####################################################################
#extract otsu threshold from VV band
ds1 = gdal.Open(clumpsMean)
maskVV = np.array(ds1.GetRasterBand(1).ReadAsArray())
maskVV=maskVV[maskVV<0]
#threshold=filters.threshold_otsu(maskVV)
threshold=np.std(maskVV)+np.mean(maskVV)

ds1=None

print('')
print('Threshold: ' + str(threshold))
print('')

####################################################################
#apply threshold
print("Running conditional statement....")
gdalformat = 'KEA'
bandDefns = []
bandDefns.append(BandDefn('class', classification, 1))
bandDefns.append(BandDefn('vvAvgMask', clumpsMean, 1))
condition='(class==1)&&(vvAvgMask>'+str(threshold)+')?2:class'
imagecalc.bandMath(outClass, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)

#resampling output to match each other
inProcessImg=outClass

rsgislib.imageutils.resampleImage2Match(inRefImg, inProcessImg, outImg, gdalFormat,interpMethod='nearestneighbour', datatype=rsgislib.TYPE_8UINT)

#add GUF mask
gdalformat = 'KEA'
bandDefns = []
bandDefns.append(BandDefn('class', inFile, 1))
bandDefns.append(BandDefn('urban', eval(guf_num[0]), 1))

condition='(class==3)&&(urban>0)?2:class'

imagecalc.bandMath(outFile, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)
