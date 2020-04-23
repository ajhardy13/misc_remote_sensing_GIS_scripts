import rsgislib, glob, os, gdal
import numpy as np
from rsgislib import imagecalc
#inputImage='S1B_IW_GRDH_1SDV_20170222T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped.tif'
#inputImage='S1B_IW_GRDH_1SDV_20170129T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped.tif'

#listFiles=glob.glob('*_snapped.tif')
listFiles=glob.glob('*.kea')
listFiles=['01-10-2016_S1_lee_classified_refined2.kea', '04-08-2018_S1_lee_nonan_classified_refined2.kea', '05-06-2018_S1_lee_nonan_classified_refined2.kea', '06-03-2017_S1_classified.kea', '06-04-2018_S1_lee_classified.kea', '06-11-2016_S1_lee_nonan_classified_refined2.kea', '07-12-2017_S1_lee_nonan_classified_refined2.kea', '08-10-2017_S1_lee_classified_refined2.kea', '09-08-2017_S1_lee_classified_refined2.kea', '10-02-2017_S1_classified.kea', '11-04-2017_S1_classified.kea', '11-07-2018_S1_lee_classified_refined2.kea', '12-01-2018_S1_lee_nonan_classified_refined2.kea', '12-05-2018_S1_lee_classified.kea', '12-12-2016_S1_lee_classified_refined2.kea', '13-03-2018_S1_lee_classified.kea', '13-10-2016_S1_lee_nonan_classified_refined2.kea', '13-11-2017_S1_lee_classified_refined2.kea', '14-09-2017_S1_lee_classified_refined2.kea', '16-04-2015_S1_classified.kea', '16-07-2017_S1_lee_classified_refined2.kea', '16-08-2018_S1_lee_classified_refined2.kea', '17-01-2017_S1_lee_classified_refined2.kea', '17-05-2017_S1_classified.kea', '17-06-2018_S1_lee_nonan_classified_refined2.kea', '18-03-2017_S1_classified.kea', '18-04-2018_S1_lee_classified.kea', '18-11-2016_S1_lee_classified_refined2.kea', '19-09-2015_S1_lee_classified_refined2.kea', '19-12-2017_S1_lee_classified_refined2.kea', '20-10-2017_S1_lee_nonan_classified_refined2.kea', '21-08-2017_S1_lee_nonan_classified_refined2.kea', '22-02-2017_S1_classified.kea', '22-04-2016_S1_classified.kea', '22-06-2017_S1_lee_nonan_classified_refined2.kea', '23-04-2017_S1_classified.kea', '23-07-2018_S1_lee_nonan_classified_refined2.kea', '24-01-2018_S1_lee_nonan_classified_refined2.kea', '24-05-2018_S1_classified.kea', '24-05-2018_S1_lee_classified.kea', '24-12-2016_S1_lee_nonan_classified_refined2.kea', '25-03-2018_S1_lee_classified.kea', '25-10-2016_S1_lee_classified_refined2.kea', '25-11-2017_S1_lee_nonan_classified_refined2.kea', '26-09-2017_S1_lee_nonan_classified_refined2.kea', '28-07-2017_S1_lee_nonan_classified_refined2.kea', '28-08-2018_S1_lee_nonan_classified_refined2.kea', '29-01-2017_S1_lee_nonan_classified_refined2.kea', '29-05-2017_S1_classified.kea', '29-06-2018_S1_lee_nonan_classified_refined2.kea', '30-03-2017_S1_classified.kea', '30-04-2018_S1_lee_classified.kea']


listFiles=sorted(listFiles)

imgBand=1
binWidth=1
inMin=1
inMax=3


# fetch histogram info
with open('water_extent_areas_km.csv', 'w') as f:
	f.write('Date, OpenWater, VegWater, Total, Other')
	f.write('\n')
	for inputImage in listFiles:
		date=inputImage.split('_')[0] # extract date from filename
		print(date)
		print('')
		read=gdal.Open(inputImage)
		data=np.array(read.GetRasterBand(1).ReadAsArray())
		openWater=(data==1).sum()
		vegWater=(data==3).sum()
		other=(data==2).sum()
		total=openWater+vegWater
		openWater=(openWater*(10*10))/1000000
		vegWater=(vegWater*(10*10))/1000000
		total=(total*(10*10))/1000000
		other=(other*(10*10))/1000000
		f.write('{0},'.format(date))
		f.write('{0},'.format(openWater))
		f.write('{0},'.format(vegWater))
		f.write('{0},'.format(total))
		f.write('{0}'.format(other))
		f.write('\n')		
		
#		
#		hist=rsgislib.imagecalc.getHistogram(inputImage, imgBand, binWidth, True, inMin, inMax) # extract histogram
#		try:
#			openWater=hist[0][1]
#			vegWater=hist[0][3]
#			total=openWater+vegWater
#			f.write('{0},'.format(date))
#			f.write('{0},'.format(openWater))
#			f.write('{0},'.format(vegWater))
#			f.write('{0}'.format(total))
#			f.write('\n')
#		except Exception:
#			print(date+' failed....')
#			openWater=hist[0][1]
#			vegWater=hist[0][2]
#			total=openWater+vegWater
#			f.write('{0},'.format(date))
#			f.write('{0},'.format(openWater))
#			f.write('{0},'.format(vegWater))
#			f.write('{0}'.format(total))
#			f.write('\n')
	
os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')
