import rsgislib, glob
from rsgislib import imagecalc
from rsgislib.imagecalc import BandDefn

#radar_in='S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee.tif'

outName='S1B_IW_GRDH_1SDV_2017_sel.kea'
listFiles=glob.glob('*_stack_lee.tif')

#for radar_in in listFiles:
#	print('')
#	print('Processing: ' + radar_in)
#
#	def high_dB(radar_in, outName):
#		print("Reading raster datasets as arrays....")
#
#		# define bands
#		bandDefns = []
#		bandDefns.append(BandDefn('VV', radar_in, 1))
#
#		# conditional statement to select low backscatter pixels
#		print("Running conditional statement....")
#		gdalformat = 'KEA'
#		imagecalc.bandMath(outName, '(VV<-15)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)
#
#	outName=radar_in.replace('.tif','_sel_lt15dB.kea')
#
#	high_dB(radar_in, outName)
	
listFiles=glob.glob('*sel_lt15dB.kea')
listFiles=sorted(listFiles)

bandDefns = []

for img in listFiles:
	band=band='"'+img.split('.')[0]+'"'
	bandDefns.append(BandDefn(band, img, 1))

expression='('+listFiles[0].split('.')[0]
for img in listFiles[1:len(listFiles)]:
	expression += ' + '
	expression += img.split('.')[0]

expression += ') / ' + str(len(listFiles))
	
gdalformat = 'KEA'
imagecalc.bandMath(outName, expression, gdalformat, rsgislib.TYPE_8UINT, bandDefns)
imagecalc.bandMath(outName, '(S1B_IW_GRDH_1SDV_20170105T165713_Sigma0_stack_lee_sel_lt15dB.kea + S1B_IW_GRDH_1SDV_20170117T165713_Sigma0_stack_lee_sel_lt15dB.kea + S1B_IW_GRDH_1SDV_20170129T165713_Sigma0_stack_lee_sel_lt15dB.kea) / 3', gdalformat, rsgislib.TYPE_8UINT, bandDefns)