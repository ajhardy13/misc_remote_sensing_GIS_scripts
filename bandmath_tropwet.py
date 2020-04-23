import gdal, argparse, sys
import numpy as np

# definition of arguments
parser = argparse.ArgumentParser(prog='Extract thematic classes from unmixed image', description='Extracts thematic classes from unmixed image using numpy where statements.')
parser.add_argument('-i', metavar='', type=str, help='Path to the unmixed image, e.g. Fractions_*.kea.')
parser.add_argument('-d', metavar='', type=str, default='./', help='Path to the output folder destination')

args = parser.parse_args()
# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')

# define the input argument
inImg=args.i
print('')
print('Input image: ' + inImg)
print('')
outFolder=args.d
print('Output directory: ' + outFolder)
print('')

# function to exctract thematic classes from unmixed image
def tropClass(inImg, outImg):
	img_read=gdal.Open(inImg)
	W=np.array(img_read.GetRasterBand(1).ReadAsArray())
	V=np.array(img_read.GetRasterBand(2).ReadAsArray())
	S=np.array(img_read.GetRasterBand(3).ReadAsArray())

	WV=W+V
	WS=W+S

	# create empty array and make all the values equal 4, i.e. 'dry'
	out=np.empty_like(W)
	out=out+5

	# series of conditions represnting EFV:3, WBS:2, OW:1
	out[np.where(W>=75)] = 1
	out[np.where((WS>=75) & (W>=25) & (W<75) & (S>=25) & (S<75))] = 2
	out[np.where((WV>=75) & (W>=25) & (W<75) & (V>=25) & (V<75))] = 3
	out[np.where((W < 25))] = 4
	out[np.where((W==0) & (V==0) & (S==0))] = 5



	driver = gdal.GetDriverByName('KEA')
	imageout = driver.Create(outImg, img_read.RasterXSize , img_read.RasterYSize , 1, gdal.GDT_Byte)
	imageout.GetRasterBand(1).WriteArray(out)

	# spatial ref system
	proj = img_read.GetProjection()
	georef = img_read.GetGeoTransform()
	imageout.SetProjection(proj)
	imageout.SetGeoTransform(georef)
	imageout.FlushCache()

outImg=outFolder+inImg.replace('.kea','_classified.kea')

tropClass(inImg, outImg)