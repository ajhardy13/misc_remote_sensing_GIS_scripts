import rsgislib, glob, subprocess
import rsgislib.imageutils

listFiles=glob.glob('Classified*.tif')

for input_img in listFiles:
	
	#input_img = '/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/Fractions_April_to_June_2016_to_2020.tif'

	#need to create new img if it is not already 3 band
	band_sel_img = input_img
#	band_sel_img = '/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/stretched/' + input_img.replace('.tif','_select.tif') 

	#rsgislib.imageutils.selectImageBands(input_img, band_sel_img, 'GTIFF', rsgislib.TYPE_16INT, [5,6,4])

	#output stretched img
	stch_img = './stretched/' + input_img.replace('.tif','_stretch.tif') 
	
	cmd="gdal_translate -of GTIFF -ot Byte -expand rgb '%s' '%s'" %(input_img, stch_img)
	subprocess.call(cmd, shell=True)
	

	outFolder = './stretched/tiles_'+input_img.split('.')[0]

	cmd="gdal2tiles.py -z 1-12 -w none  '%s' '%s'" %(stch_img, outFolder)
	subprocess.call(cmd, shell=True)