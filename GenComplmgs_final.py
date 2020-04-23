import rsgislib
import rsgislib.imageutils
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.imagecalc.calcindices

import glob
import os.path

# Generate a composite image
def createCompImg(testImage, outRefCompImg, outCompImg):
    """
    A function which generates a maximum NDVI composite image.
    """
    
	# Get list of input images.
	imgs = glob.glob(testImage)

	# Calculate the NDVI for each input image.
	refLyrsLst = []
	for img in imgs:
		print('Processing:\t' + img)
		baseImgName = os.path.splitext(os.path.basename(img))[0]
		refLyrImg = os.path.join(baseImgName+'_ndvi.kea')
		refLyrsLst.append(refLyrImg)
		rsgislib.imagecalc.calcindices.calcNDVI(img, 3, 4, refLyrImg, stats=False, gdalFormat='KEA')


	# Create Reference Image.
	rsgislib.imagecalc.getImgIdxForStat(refLyrsLst, outRefCompImg, 'KEA', 0, rsgislib.SUMTYPE_MAX)

	# Populate the Reference image with statistics and pyramids.
	rsgislib.rastergis.populateStats(outRefCompImg, True, True, True)

	# Create Composite Image.
	rsgislib.imageutils.createRefImgCompositeImg(imgs, outCompImg, outRefCompImg, 'KEA', rsgislib.TYPE_16UINT, 0.0)

	# Calculate output image statistics and pyramids.
	rsgislib.imageutils.popImageStats(outCompImg, usenodataval=True, nodataval=0, calcpyramids=True)


# Call the function for testImage.
createCompImg ('./*/*MS_SR_cloudmask.tif', './20190325_refimage.kea', './20190325_composite.kea')

