import rsgislib, glob, subprocess
import rsgislib.imageutils

listFiles=glob.glob('Fractions*.tif')

for input_img in listFiles:
	
	#input_img = '/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/Fractions_April_to_June_2016_to_2020.tif'

	#need to create new img if it is not already 3 band (ie. if doing a landsat composite)
#	band_sel_img = input_img
#	band_sel_img = '/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/stretched/' + input_img.replace('.tif','_select.tif') 

#	rsgislib.imageutils.selectImageBands(input_img, band_sel_img, 'GTIFF', rsgislib.TYPE_16INT, [5,6,4])

	#output stretched img
	stch_img = './stretched/' + input_img.replace('.tif','_stretch.tif') 

	#function to stretch img
	rsgislib.imageutils.stretchImage(input_img, stch_img, False, '', True, False, 'GTIFF', rsgislib.TYPE_8INT, rsgislib.imageutils.STRETCH_LINEARMINMAX)


	#use this to generate tiles after on command line
	#gdal2tiles.py -z 1-12 -w none Fractions_April_to_June_2016_to_2020_stch.tif ./fractions_tiles

	outFolder = './stretched/tiles_'+input_img.split('.')[0]

	cmd="gdal2tiles.py -z 1-12 -w none  '%s' '%s'" %(stch_img, outFolder)
	subprocess.call(cmd, shell=True)