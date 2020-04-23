import collections, glob
from rsgislib import rastergis


listFiles=glob.glob('*_clumps2.kea')
for clumps in listFiles[0:2]:
#	clumps=listFiles[1]
	field = 'OutClass_mode_cert'
classcolours = {}
colourCat = collections.namedtuple('ColourCat', ['red', 'green', 'blue', 'alpha'])
classcolours[1] = colourCat(red=106, green=143, blue=255, alpha=255)
classcolours[2] = colourCat(red=169, green=169, blue=169, alpha=255)
classcolours[3] = colourCat(red=177, green=255, blue=165, alpha=255)
classcolours[4] = colourCat(red=255, green=255, blue=191, alpha=255)
rastergis.colourClasses(clumps, field, classcolours)