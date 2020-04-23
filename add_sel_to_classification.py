import glob, rsgislib, rios, gdal, numpy, subprocess, time, os
from rsgislib import rastergis, imageutils, imagecalc
from rsgislib.rastergis import ratutils
from rsgislib.imagecalc import BandDefn
from rios import rat

start = time.time()

#read Sand Exclusion Layer
sel='S1B_IW_GRDH_1SDV_2017_sel_2.kea'
# set SEL band names
bandList=['SEL']
rsgislib.imageutils.setBandNames(sel, bandList)

#read Sand Exclusion Layer
waterPerm='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/seasonality_barotseland_snapped_3.tif'
# set SEL band names
bandList=['waterPerm']
rsgislib.imageutils.setBandNames(waterPerm, bandList)

guf='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_urban_footprint/GUF_Barotseland_snapped_3.tif'
# set SEL band names
bandList=['guf']
rsgislib.imageutils.setBandNames(guf, bandList)

#read clumps RAT
#listFiles=glob.glob('*_clumps2.kea')
listFiles=['S1B_IW_GRDH_1SDV_20170423T165720_Sigma0_stack_lee_clumps2.kea']

#for clumps in listFiles[2:len(listFiles)]:
for clumps in listFiles:

	try:
		
		print('')
		print('Processing: ' + clumps)
		#clumps=listFiles[0]

		outImage=clumps.replace('.kea','_erf_clumptrain_mode_sel.tif')
		print('')
	#	print('SEL: ' + sel)
	#	print('clumps: ' + clumps)
		print('')
		ratutils.populateImageStats(sel,clumps,calcMax=True,calcMean=True,calcMin=True) # add SEL statistics to RAT
		ratutils.populateImageStats(guf,clumps,calcMax=True) # add SEL statistics to RAT
		#ratutils.populateImageStats(waterPerm,clumps,calcMean=True) # add water permanance statistics to RAT

		# Open RAT
		ratDataset = gdal.Open(clumps, gdal.GA_Update)
		data=[]
		# Read in data from class_cert and sel columns
		data.append(rat.readColumn(ratDataset, 'OutClass_mode_cert'))
		data.append(rat.readColumn(ratDataset, 'SELMax'))
		data.append(rat.readColumn(ratDataset, 'gufMax'))

		mode_cert=data[0]
		sel_d=data[1]
		guf_d=data[2]
		mode_cert_sel=mode_cert

		#where statement to make sel > 60 objects 'other'
		mode_cert_sel[numpy.where((mode_cert_sel==1)&(sel_d>=60))]=2
		mode_cert_sel[numpy.where((mode_cert_sel==3)&(guf_d>0))]=2

		names=[]
		for i in mode_cert_sel:
			if i==1:
				names.append('Water')
			elif i==2:
				names.append('Other')
			elif i==3:
				names.append('VegWater')

		#write out columns to RAT
		rios.rat.writeColumn(clumps, 'OutClass_mode_cert_sel', mode_cert_sel, colType=gdal.GFT_Integer)
		rios.rat.writeColumn(clumps, 'OutClass_mode_cert_sel_names', names, colType=gdal.GFT_String)

		# export rat column: mode with certainty to image

		gdalformat = 'GTiff'
		datatype = rsgislib.TYPE_8INT
		fields = ['OutClass_mode_cert_sel']

		rastergis.exportCols2GDALImage(clumps, outImage, gdalformat, datatype, fields)

		#bandmath to add permananent water pixels
		bandDefns = []
		bandDefns.append(BandDefn('class', outImage, 1))
		bandDefns.append(BandDefn('permWater', waterPerm, 1))
		imagecalc.bandMath(outImage, '(permWater>=5)?1:class', 'GTiff', rsgislib.TYPE_8UINT, bandDefns)


		ratDataset=None
	#	clumps=None

		# add colourtable
		#cmd='gdaldem color-relief ' + outImage + ' /Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/gdaldem_wb_class_colours.txt ' + outImage
		#subprocess.call(cmd)
		os.system('afplay /System/Library/Sounds/Tink.aiff')
	except Exception:
		print('')
		print('............................................')
		print('Failed: ' + clumps)
		print('............................................')
		print('')
		pass

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stam

