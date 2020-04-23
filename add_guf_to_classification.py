import rsgislib, gdal, glob, sys, argparse
from rsgislib import rastergis, imageutils, imagecalc
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn

###################
# definition of arguments
parser = argparse.ArgumentParser(prog='Implement global urban footprint refinement', description='Refines veg water prediciton using global urban footprint mask.')
parser.add_argument('-i', metavar='', type=str, help='Path to the classified image, i.e. *_mode_otsu_snap.kea.')
args = parser.parse_args()
# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')
##############################################################################################

##############################################################################################	
inFile=args.i
print('')
print('Input image: ' + inFile)
print('')
##############################################################################################

	
outFile=inFile.replace('.kea','_guf.kea')
guf1='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped.tif'
guf2='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped_2.tif'
guf3='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped_3.tif'

ds1 = gdal.Open(inFile)
x=ds1.RasterXSize
y=ds1.RasterYSize
ds1=None

guf = gdal.Open(guf1)
g1_x=guf.RasterXSize
g1_y=guf.RasterYSize
guf=None

guf = gdal.Open(guf2)
g2_x=guf.RasterXSize
g2_y=guf.RasterYSize
guf=None

guf = gdal.Open(guf3)
g3_x=guf.RasterXSize
g3_y=guf.RasterYSize
guf=None

try:
	guf_num=[]

	if (x==g1_x and y==g1_y):
		guf_num.append('guf1')
		print('Found a match: guf1')
	elif (x==g2_x and y==g2_y):
		guf_num.append('guf2')
		print('Found a match: guf2')
	elif (x==g3_x and y==g3_y):
		guf_num.append('guf3')
		print('Found a match: guf3')
	else:
		pass		

	print('')

	print("Running conditional statement....")
	gdalformat = 'KEA'
	bandDefns = []
	bandDefns.append(BandDefn('class', inFile, 1))
	bandDefns.append(BandDefn('urban', eval(guf_num[0]), 1))

	condition='(class==3)&&(urban>0)?2:class'

	imagecalc.bandMath(outFile, condition, gdalformat, rsgislib.TYPE_8UINT, bandDefns)

except:
	print('No matching GUF for: ' + inFile)	
	pass
