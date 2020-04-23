import rsgislib
from rsgislib import imagecalc
 
inputImage='ortho_mwera_2_RGB.tif'
maskImg='ortho_mwera_2_RGB_training_snap.tif'
 
inImgBands=['R','G','B']
inImgBands=[1,2,3]
maskImgVal=1
histBinWidths=[5,5,5] 
outputImage=inputImage.replace('.tif','_WBprob.tif')
 
rsgislib.imagecalc.calcMaskImgPxlValProb(inputImage, inImgBands, maskImg, maskImgVal, outputImage, 'GTiff',histBinWidths)