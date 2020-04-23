import rsgislib, glob
import rsgislib.imageutils


listSR=sorted(glob.glob('./*/*MS_SR.tif'))

gdalformat='KEA'
datatype=rsgislib.TYPE_16UINT
for img in listSR:
	udm = img.replace('SR.tif','DN_udm.tif')
	outputimage = img.replace('.tif','_cloudmask.tif')
	rsgislib.imageutils.maskImage(img, udm, outputimage, gdalformat, datatype, 0, 2)

inImgsPattern='./*/*MS_SR_cloudmask.tif'
outRefImg='./20190325_refimage.kea'
outCompImg='./20190325_composite.kea'
rsgislib.imageutils.imagecomp.createMaxNDVIComposite(inImgsPattern, 3, 4, outRefImg, outCompImg, tmpPath='./tmp', gdalFormat='KEA', dataType=None, calcStats=True)
