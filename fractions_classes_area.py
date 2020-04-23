import glob, csv
from osgeo import gdal_array
import numpy as np


list=sorted(glob.glob('*.tif'))

valsArray=[]
valsArray.append(['Date','Water_area'])


for l in list:
	print('Input file: ' + l)
	date='28/'+l.split('m')[1].split('to')[0]+'/'+l.split('.')[0].split('to')[-1]
	rasterArray = gdal_array.LoadFile(l)
	areaWater = rasterArray[0].flatten()
	#areaVeg = rasterArray[1].flatten()
	#areaSand = rasterArray[2].flatten()

	# considered a water body (veg, open, wet sand) if fraction gt 225 m^2
	areaWater[np.where(areaWater>900)] = np.nan
	areaWater[np.where(areaWater<225)] = 0
	areaWater[np.where(areaWater>=225)] = 1
	#	areaVeg[np.where(areaVeg>900)] = 0
	#	areaSand[np.where(areaSand>900)] = 0

	vals=[]
	waterPixels=np.nansum(areaWater)
	waterArea=np.nansum(waterPixels*900)/1000000

	print('water pixels, '+ date + ': ' + str(waterPixels))
	print('water area, '+ date + ': ' + str(waterArea))

	vals.append(date)
	vals.append(waterArea)

	valsArray.append(vals)

with open('water_areas_2015.csv', 'w', newline='') as f:
#with open('fractional_areas_water.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerows(valsArray)


	