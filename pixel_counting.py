# read WB result as numpy array and extract number of wetted pixels
# compare against rainfall

import glob, gdal, csv
import numpy as np

inFolder='/Users/Andy/Documents/Tanzania/Sentinel/Sentinel1A_Namwawala/Out/Subset/dB/WB_prediction/Static_thresh/v2/dry_rule/adaptive/'

inFiles=glob.glob(inFolder+'*.tif')

dates=[]
wet_area_stats=[]

for f in inFiles:
	# open the image
	print('Processing: ' + f.split('/')[-1])
	image=gdal.Open(f)
	data=np.array(image.GetRasterBand(1).ReadAsArray())
	
	# flatten data
	dataFlat=data.flatten()
	
	# extract pixels for WBs, veg WBs
	wb=np.extract(dataFlat==1,dataFlat)
	wv=np.extract(dataFlat==2,dataFlat)
	o=np.extract(dataFlat==3,dataFlat)
	
	# calculate % wet
# 	wet=len(wb)+len(wv)+len(o)
	wet=len(wv)
	all=len(dataFlat)
	pc_wet=(wet/all)*100
	
	# calculate wet area in km^2
	wet_area_m=wet*(10**2)
	wet_area_km=(wet*(10**2)*0.000001)
	
	#extract date and append
	d=(f.split('VV_')[1].split('_WB.tif')[0])
	dates.append(d[0:4]+'/'+d[4:6]+'/'+d[6:8])
	
	# extract stat and append
	wet_area_stats.append(wet_area_m)

# writing stats to csv
print('Writing stats to csv...')
# write out date and stats to csv
print('Writing csv...')
with open(inFolder+'pixelstats_vegwb_prediction.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Dates','WBArea'])
    writer.writerows(zip(dates, wet_area_stats))
	
	