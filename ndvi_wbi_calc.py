import rsgislib.imagecalc

inputImg = '/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite.tif'
outNDVI = '/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite_ndvi.tif'
outWBI = '/Users/Andy/Documents/Tanzania/Landsat/GEE/Composites/Landsat8_composite_WBI.tif'
rBand=4
nBand=5
bBand=2

rsgislib.imagecalc.calcNDVI(inputImg, rBand, nBand, outNDVI, stats=True, gdalFormat='KEA')
rsgislib.imagecalc.calcWBI(inputImg, bBand, nBand, outWBI, stats=True, gdalFormat='KEA')