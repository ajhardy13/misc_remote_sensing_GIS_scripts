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
	
listFiles=glob.glob('*sel_lt15dB_snapped.kea')
listFiles=sorted(listFiles)

bandNum=list(range(1,len(listFiles)+1))
bands=[]
for n in bandNum:
	bands.append('b'+str(n))

bandDefns = []

for b, img in zip(bands,listFiles):
	bandDefns.append(BandDefn(b, img, 1))

expression='((b1'
for b in bands[1:len(bands)]:
	expression += ' + '
	expression += b

expression += ') / ' + str(len(bands)) + ') * 100'
	
gdalformat = 'KEA'
imagecalc.bandMath(outName, expression, gdalformat, rsgislib.TYPE_8UINT, bandDefns)
