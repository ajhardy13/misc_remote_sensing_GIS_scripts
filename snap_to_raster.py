import os

inputImage='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_classified.tif'
snapImage='/Users/Andy/Documents/Tanzania/Sentinel/Sentinel1A_Namwawala/Out/Subset/dB/vv_stack.tif'
outputImage='/Users/Andy/Documents/Tanzania/WB_Mapping/land_cover/Landsat8_composite_clumps_classified_clipped.tif'

# snap raster to shp
print('Converting to shp...')
cmd='gdaltindex snapImage.shp ' + snapImage
os.system(cmd)

# clip input image to snap
print('Clipping image...')
cmd2='gdalwarp -cutline snapImage.shp -crop_to_cutline ' + inputImage + ' outputTemp.tif'
os.system(cmd2)

# set target size
print('Setting target size...')
cmd3='gdalwarp -ts 5057 3014 outputTemp.tif outputTemp_tr.tif' 
os.system(cmd3)

# set target size
print('Setting target resolution...')
cmd4='gdalwarp -tr 0.00009 0.00009 -overwrite outputTemp_tr.tif ' + outputImage
os.system(cmd4)

# removing temp files
print('Removing temp files...')
os.remove('outputTemp.tif')
os.remove('outputTemp_tr.tif')
