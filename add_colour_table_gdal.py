import gdal, glob

# specify GeoTIFF file name, open it using GDAL and get the first band
listFiles=glob.glob('/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/Classified*')

for fn in listFiles:

#fn = '/Users/Andy/Documents/Rwanda/Data/TropWet_Outputs/TW_v7.2/Classified_Output_April_to_June_2016_to_2020.tif'
	ds = gdal.Open(fn, 1)
	band = ds.GetRasterBand(1)

	# create color table
	colors = gdal.ColorTable()

	# set color for each value
	colors.SetColorEntry(0, (209, 209, 204))
	colors.SetColorEntry(1, (69, 174, 144))
	colors.SetColorEntry(2, (221, 154, 162))
	colors.SetColorEntry(3, (229, 206, 113))
	colors.SetColorEntry(4, (34, 80, 202))
	colors.SetColorEntry(5, (50, 133, 54))
	colors.SetColorEntry(6, (203, 191, 124))


	# set color table and color interpretation
	band.SetRasterColorTable(colors)
	band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

	# close and save file
	del band, ds