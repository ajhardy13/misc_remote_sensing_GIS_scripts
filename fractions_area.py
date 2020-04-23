import glob, csv
from osgeo import gdal_array
import numpy as np


list=sorted(glob.glob('*.tif'))
#list=['Fractions_m7to9_y2016to2016.tif','Fractions_m6to8_y2017to2017.tif','Fractions_m7to9_y2018to2018.tif']
#valsArray=[]
#valsArray.append(['Water','Veg','Sand'])

#for l in list:
#	print('Input file: ' + l)
#	rasterArray = gdal_array.LoadFile(l)
#	areaWater = rasterArray[0].flatten()
#	areaVeg = rasterArray[1].flatten()
#	areaSand = rasterArray[2].flatten()
#
#	areaWater[np.where(areaWater>900)] = 0
#	areaVeg[np.where(areaVeg>900)] = 0
#	areaSand[np.where(areaSand>900)] = 0
#
#	vals=[]
#	vals.append(np.nansum(areaWater))
#	vals.append(np.nansum(areaVeg))
#	vals.append(np.nansum(areaSand))
#	valsArray.append(vals)

valsArray=[]
valsArray.append(['Date','%_pixels_Water','area_pixels_water'])


for l in list:
	print('Input file: ' + l)
	date='14/'+l.split('m')[1].split('to')[0]+'/'+l.split('.')[0].split('to')[-1]
	rasterArray = gdal_array.LoadFile(l)
	areaWater = rasterArray[0].flatten()
	areaVeg = rasterArray[1].flatten()
	areaSand = rasterArray[2].flatten()

	areaWater[np.where(areaWater>900)] = 0
#	areaVeg[np.where(areaVeg>900)] = 0
#	areaSand[np.where(areaSand>900)] = 0

	vals=[]
	waterPixels=sum(1 for i in areaWater if i>0)
	totalPixels=len(areaWater)
	print('water pixels, '+ date + ': ' + str(waterPixels))
	propWater=(waterPixels/totalPixels)*100
	areaWaterCalc=(waterPixels)*900
	vals.append(date)
	vals.append(propWater)
	vals.append(areaWaterCalc)

	valsArray.append(vals)

with open('fractional_areas_2015.csv', 'w', newline='') as f:
#with open('fractional_areas_water.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerows(valsArray)


	