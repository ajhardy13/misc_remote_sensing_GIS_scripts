from rsgislib import zonalstats
inputimage = 'S2_aber.tif'
inputvector = 'S2_aber_ROIs_v2.shp'
outputtxtbase = 'zones_s2_txt'
zonalstats.pixelVals2TXT(inputimage, inputvector, outputtxtbase, 'FID', True,  zonalstats.METHOD_POLYCONTAINSPIXELCENTER)

