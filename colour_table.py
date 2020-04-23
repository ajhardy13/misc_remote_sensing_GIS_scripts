import collections
from rsgislib import rastergis
 
classification='/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/2017/Out/Out/S1B_IW_GRDH_1SDV_20170105T165713_Sigma0_stack_lee_clumps2_classified_multi_erf_balanced_allstats_wetveg.tif'
 
# Add histogram (automatically adds attribute table)
# rastergis.populateStats(classification, addclrtab=False, \
#         calcpyramids=False, ignorezero=False)
 
# Add pixel values to attribute table
# bandStats = []
# bandStats.append(rastergis.BandAttStats(band=1, maxField='Class'))
#  
# rastergis.populateRATWithStats(classification, \
#                                 classification, bandStats)
 
# Add colour table
# classColours = dict()
# classColours['Other'] = [212,125,83]
# classColours['Water'] = [157,212,255]
# classColours['VegWater'] = [191,255,0]
# # 
# classcolours = {}
# colourCat = collections.namedtuple('ColourCat', \
#                         ['red', 'green', 'blue', 'alpha'])
# classcolours[0] = colourCat(red=0, green=0, blue=0, alpha=0)
# classcolours[1] = colourCat(red=255, green=0, blue=0, alpha=255)
# classcolours[2] = colourCat(red=0, green=0, blue=255, alpha=255)
# classcolours[3] = colourCat(red=0, green=200, blue=0, alpha=255)
# classcolours[4] = colourCat(red=0, green=100, blue=0, alpha=255)
# rastergis.colourClasses(classification, 'Class', classColours)
 
# Add pyramids (for fast display)
# rastergis.populateStats(classification, addclrtab=False, \
#           calcpyramids=True, ignorezero=False)

# pyramids=True
# colourtable=True
# rastergis.populateStats(classification, colourtable, pyramids)

field = 'Value'
classcolours = {}
colourCat = collections.namedtuple('ColourCat', ['red', 'green', 'blue', 'alpha'])
classcolours[1] = colourCat(red=200, green=50, blue=50, alpha=255)
classcolours[2] = colourCat(red=200, green=240, blue=50, alpha=255)
classcolours[3] = colourCat(red=50, green=240, blue=50, alpha=255)
rastergis.colourClasses(classification, field, classcolours)