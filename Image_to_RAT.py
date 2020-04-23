#! /home/osian/miniconda3/bin/python

# Create a 'segmented' image for each pixel with a value not equal to 0.
import numpy
from osgeo import gdal
from rsgislib import rastergis

InputImage = 'InputImage.kea'
OutImage = 'Segmented_Image.kea'

######################################################################################
dataset = gdal.Open(InputImage, gdal.GA_ReadOnly)
X_Size = dataset.RasterXSize
Y_Size = dataset.RasterYSize
Projection = dataset.GetProjectionRef()
GeoTransform = dataset.GetGeoTransform()

# Read first band as a numpy array
band1 = dataset.GetRasterBand(1) 
Array = band1.ReadAsArray()
dataset = None # close raster to save memory.

# Count non-zeros
ValidPixels = numpy.count_nonzero(Array)
print("Valid pixels:", ValidPixels)

# Convert non-zeros to 1
MaskArray = numpy.not_equal(Array, 0)
numpy.putmask(Array, MaskArray, 1)

# Convert array to uint32 format
Array = Array.astype('uint32')

# assign unique integers to non-zero pixels
NewVals = numpy.arange(1, ValidPixels+1, 1, dtype='uint32')
numpy.place(Array, MaskArray, NewVals)

del NewVals
del MaskArray

# Create output raster
print("Creating raster...")
gdalformat = 'KEA'
datatype = gdal.GDT_UInt32
driver = gdal.GetDriverByName(gdalformat)
metadata = driver.GetMetadata()
output = driver.Create(OutImage, X_Size, Y_Size, 1, datatype)
output.SetProjection(Projection)
output.SetGeoTransform(GeoTransform)
outband = output.GetRasterBand(1)
outband.WriteArray(Array)

# Close datasets
output = None
del Array

# Add a raster attribute table
rastergis.populateStats(OutImage, True, True, True, 1)
print("Done.")
