# convert nan to number, in this case producing zeros
gdal_calc.py -A 13-03-2018_S1_lee_subset_copy.tif --outfile=13-03-2018_S1_lee_subset_copy_nonan.tif --calc="nan_to_num(A)"
#gdal_translate result.tif 13-03-2018_S1_lee_subset_copy_nan.tif -a_nodata -999

# mask out values that ==0.0, i.e. nan values
import rsgislib, os
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn

inputImage='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/Processed/Update/Test/13-03-2018_S1_lee_subset_copy.tif'
nanOut=inputImage.replace('.tif','_nonan.tif')
#outputImage=inputImage.replace('.tif','_offset.kea')

###################################################################
'''
gdalformat = 'KEA'
datatype = rsgislib.TYPE_32FLOAT
expression = 'b1+50.0'
imagecalc.imageMath(inputImage, outputImage, expression, gdalformat, datatype)
bandList=['VV','VH','VVdivVH']
rsgislib.imageutils.setBandNames(outputImage, bandList)
'''
###################################################################

# define output names for each band
b1=inputImage.replace('.tif','_b1.tif')
b2=inputImage.replace('.tif','_b2.tif')
b3=inputImage.replace('.tif','_b3.tif')

# run gdal command to convert nan to a number, i.e. 0.0
cmd='gdal_calc.py -A %s --A_band=1 --outfile=%s --calc="nan_to_num(A)"' %(inputImage,b1)
os.system(cmd)
cmd='gdal_calc.py -A %s --A_band=2 --outfile=%s --calc="nan_to_num(A)"' %(inputImage,b2)
os.system(cmd)
cmd='gdal_calc.py -A %s --A_band=3 --outfile=%s --calc="nan_to_num(A)"' %(inputImage,b3)
os.system(cmd)


gdalformat = 'KEA'

# define the output names
b1_nan=b1.replace('.tif','_b1_nan.tif')
b2_nan=b2.replace('.tif','_b2_nan.tif')
b3_nan=b3.replace('.tif','_b3_nan.tif')

bandDefns = []
bandDefns.append(BandDefn('b1', b1, 1))
imagecalc.bandMath(b1_nan, '(b1==0.0)?-999:b1', gdalformat, rsgislib.TYPE_32FLOAT, bandDefns)
bandDefns = []
bandDefns.append(BandDefn('b2', b2, 1))
imagecalc.bandMath(b2_nan, '(b2==0.0)?-999:b2', gdalformat, rsgislib.TYPE_32FLOAT, bandDefns)
bandDefns = []
bandDefns.append(BandDefn('b3', b3, 1))
imagecalc.bandMath(b3_nan, '(b3==0.0)?-999:b3', gdalformat, rsgislib.TYPE_32FLOAT, bandDefns)

gdalformat='GTiff'
gdaltype = rsgislib.TYPE_32FLOAT
imageutils.stackImageBands([b1_nan,b2_nan,b3_nan], ['VV','VH','VVdivVH']  , nanOut, None, -999, gdalformat, gdaltype)

try:
	os.remove(b1)
	os.remove(b2)
	os.remove(b3)
	os.remove(b1_nan)
	os.remove(b2_nan)
	os.remove(b3_nan)
except Exception:
        pass

