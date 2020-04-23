from osgeo import gdal,ogr
import numpy as np
import struct, os, sys, matplotlib
import matplotlib.pyplot as plt

#src_filename = '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Fractional_cover/Fractions_class_20180515.tif'
shp_filename = '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Fractional_cover/Analysis/fractions_points_v3.shp'
#shp_filename = '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Fractional_cover/Analysis/fractions_points_transects.shp'

src_filename = '/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Fractional_cover/Fractions_class_20180515.tif' # the input fraction image

sar_filename='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GEE/S1B_IW_GRDH_1SDV_20180524_stack_lee_clumps2_mean.kea' # the input SAR image

class_filename='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GEE/S1B_IW_GRDH_1SDV_20180524_stack_classified.kea'

#lyr=None
#ds=None

# extract values from raster to point shapefile, band 1 only	
def extractpoints(src_filename,bandnum):
	src_ds=gdal.Open(src_filename) 
	gt=src_ds.GetGeoTransform()
	rb=src_ds.GetRasterBand(bandnum)
	ds=ogr.Open(shp_filename)
	lyr=ds.GetLayer()
	#	li_values = list()
	li_values=[]
	for feat in lyr:
		geom = feat.GetGeometryRef()
		feat_id = feat.GetField('id')
		mx, my = geom.GetX(), geom.GetY()
		px = int((mx - gt[0]) / gt[1])
		py = int((my - gt[3]) / gt[5])
		intval = rb.ReadAsArray(px, py, 1, 1)
#		li_values.append([feat_id, intval[0]])
		li_values.append(intval[0])
	return(li_values)
	src_ds=None
	gt=None
	rb=None

# output for water_20180515
vars()['water_'+os.path.split(src_filename)[1].split('_')[-1].split('.')[0]]=np.asarray(extractpoints(src_filename,bandnum=1))

# output for veg_20180515
vars()['veg_'+os.path.split(src_filename)[1].split('_')[-1].split('.')[0]]=np.asarray(extractpoints(src_filename,bandnum=2))

# proportion of water in pixel
prop_water=(water_20180515/(veg_20180515+water_20180515))*100
prop_water[np.where(prop_water<50)]=np.NaN
print(np.count_nonzero(~np.isnan(prop_water)))

# output for dB_vv_20180524
#vars()['dB_vv_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=np.asarray(extractpoints(sar_filename,bandnum=1))

# output for dB_vvvh_20180524
vars()['dB_vvvh_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=np.asarray(extractpoints(sar_filename,bandnum=3))
dB_vvvh_20180524[np.where(dB_vvvh_20180524>10)]=np.NaN

plt.plot(prop_water,dB_vvvh_20180524,'o',color='k')

# output for class_20180524
vars()['class_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=np.asarray(extractpoints(class_filename,bandnum=1))

#extract dB values where class is wet veg and plot
vars()['dB_vvvh_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=np.asarray(extractpoints(sar_filename,bandnum=3))
dB_vvvh_20180524[np.where(dB_vvvh_20180524>10)]=np.NaN
dBclass_veg=dB_vvvh_20180524
dBclass_veg[np.where((class_20180524!=3))&(prop_water!=np.NaN)]=np.NaN
print(np.count_nonzero(~np.isnan(dBclass_veg)))
plt.plot(prop_water,dBclass_veg,'go',label='Class: Veg Water')

#extract dB values where class is water and plot
vars()['dB_vvvh_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=np.asarray(extractpoints(sar_filename,bandnum=3))
dB_vvvh_20180524[np.where(dB_vvvh_20180524>10)]=np.NaN
dBclass_wat=dB_vvvh_20180524
dBclass_wat[np.where(class_20180524!=1)]=np.NaN
print(np.count_nonzero(~np.isnan(dBclass_wat)))
plt.plot(prop_water,dBclass_wat,'o',label='Class: Open Water',color='royalblue')

# plot the output
matplotlib.rcParams['font.family'] = "arial"
matplotlib.rcParams['mathtext.default'] = 'regular'
plt.ylabel('VV/VH ratio')
plt.xlabel('Fractional water cover (%)')


plt.legend()
plt.grid(True)

plt.show()

###########################################################
#identify points that are gt 50 water and were not classified as wetveg AND are not classified as water
np.count_nonzero(~np.isnan(dBclass_mask))
np.count_nonzero(~np.isnan(prop_water_mask))
###########################################################
###########################################################
#extracting unclassified wet pixels
# extract values from raster to point shapefile, band 1 only	


def extractpoints_id(src_filename,bandnum):
	src_ds=gdal.Open(src_filename) 
	gt=src_ds.GetGeoTransform()
	rb=src_ds.GetRasterBand(bandnum)
	ds=ogr.Open(shp_filename)
	lyr=ds.GetLayer()
	li_values = list()
#	li_values=[]
	for feat in lyr:
		geom = feat.GetGeometryRef()
		feat_id = feat.GetField('id')
		mx, my = geom.GetX(), geom.GetY()
		px = int((mx - gt[0]) / gt[1])
		py = int((my - gt[3]) / gt[5])
		intval = rb.ReadAsArray(px, py, 1, 1)
		li_values.append([feat_id, intval[0]])
#		li_values.append(intval[0])
	return(li_values)
	src_ds=None
	gt=None
	rb=None

# output for id_water_20180515
vars()['id_water_'+os.path.split(src_filename)[1].split('_')[-1].split('.')[0]]=extractpoints_id(src_filename,bandnum=1)

# output for id_veg_20180515
vars()['id_veg_'+os.path.split(src_filename)[1].split('_')[-1].split('.')[0]]=extractpoints_id(src_filename,bandnum=2)

# output for id_class_20180524
vars()['id_class_'+os.path.split(sar_filename)[1].split('_')[-5].split('.')[0]]=extractpoints_id(class_filename,bandnum=1)


import pandas as pd

dF_water=pd.DataFrame(id_water_20180515)
dF_veg=pd.DataFrame(id_veg_20180515)
dF_class=pd.DataFrame(id_class_20180524)
result=pd.concat([dF_water,dF_veg,dF_class],axis=1)
result.columns=['id','water','id2','veg','id3','class']
result.Index=['id']

result['prop']=(result.water/(result.water + result.veg))*100	

result.to_csv('test.csv',sep=',')
