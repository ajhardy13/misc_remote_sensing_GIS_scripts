import rsgislib, ogr, subprocess, os, glob, shutil
from rsgislib import imageutils, vectorutils

classImage = '06-11-2016_S1_lee_nonan_classified_refined2.kea'

inputROIimage = '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_2/GEE/20161102T082112_20161102T134135_T34LGJ.tif'
outClassImage = classImage.replace('.kea','_masked.tif')

# subset classification and output GTiff
#rsgislib.imageutils.subset2img(classImage, inputROIimage, outputimage, gdalformat, type)

#snap the orginal clasiication to the size of the reference image
gdalFormat='GTiff'
rsgislib.imageutils.resampleImage2Match(inputROIimage, classImage, outClassImage, gdalFormat,interpMethod='nearestneighbour', datatype=rsgislib.TYPE_8INT)

# convert to classimage to GTiff
out='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','.tif')
cmd="gdal_translate %s %s" %(classImage,out)
os.system(cmd)

#generate random points for the snapped class image
inputImage=outClassImage
outputImage=inputImage.replace('.kea','_sample.kea')
gdalFormat='KEA'
rsgislib.imageutils.performRandomPxlSampleInMask(inputImage, outputImage, gdalFormat, maskvals=[1,2,3], numSamples=300)

#convert raster to point shapefile
inputImage=outputImage
listNums=[1,2,3]
listClasses=['Water','Other','VegWater']

#loop to add new field 'Class' and populate with relative class name
for n, c in zip(listNums, listClasses):	
	outputShp='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_'+str(n)+'.shp')
	maskVal=n
	force=True
	rsgislib.vectorutils.exportPxls2Pts(inputImage, outputShp, maskVal, force)
	ds = ogr.Open(outputShp, update = 1 )
	lyr = ds.GetLayer( 0 )
	lyr.ResetReading()

	# creat an populate relevant fields
	lyr.CreateField(ogr.FieldDefn('Class', ogr.OFTString ))
	lyr.CreateField(ogr.FieldDefn('ClassRef', ogr.OFTString ))
	lyr.CreateField(ogr.FieldDefn('Processed', ogr.OFTInteger ))
	
	for i in lyr:
		lyr.SetFeature(i)
		i.SetField( 'Class', c )
		i.SetField( 'ClassRef', c )
		i.SetField( 'Processed', 0 )
		lyr.SetFeature(i)	

	ds = None


#merge shapefiles	
outputShp='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points.shp')

shp1='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_1.shp')
shp2='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_2.shp')
shp3='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_3.shp')

print('Merging...')
#cmd='ogrmerge.py -o ' + outputShp + ' ' + shp1 + ' ' + shp2 + ' ' + shp3 + ' -overwrite_layer -single'
cmd='ogrmerge.py -o ' + outputShp + ' ' + shp1 + ' ' + shp2 + ' ' + shp3 + ' -single -overwrite_ds '
subprocess.call(cmd, shell=True)

#remove unwanted files
for i in glob.glob('/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_1*')):
	os.remove(i)
for i in glob.glob('/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_2*')):
	os.remove(i)
for i in glob.glob('/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+classImage.replace('.kea','_points_3*')):
	os.remove(i)
for i in glob.glob('*masked*'):
	os.remove(i)
#shutil.move(outClassImage,'/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/accuracy_assessment/Accuracy_assessment_update/'+outClassImage)
