
import rsgislib, gdal, numpy
import numpy as np
import pandas as pd
from rsgislib import imageutils, imagecalc
from sklearn.decomposition import PCA

inImg='S1B_IW_GRDH_1SDV_20171125T165722_Sigma0_stack_lee.tif'
imgMask = inImg.replace('.tif','_clumps2_erf_clumptrain_mode.tif')
outImg = inImg.replace('.tif','_wb_mask.kea')
classification=inImg.replace('.tif','_clumps2_erf_clumptrain_mode.tif')
outClass=classification.replace('.tif','_std.kea')

gdalformat='KEA'
datatype=rsgislib.TYPE_32FLOAT

clumps=outImg.replace('.kea','_clumps2.kea')
clumpsMean=outImg.replace('.kea','_clumps2_mean.kea')

inputImage=clumpsMean
#inImgBands=[1,3]
#maskImg='/Users/Andy/Documents/Zambia/RemoteSensing/WB_classification/Supporting_data/global_surface_water/ssh_out/seasonality_barotseland_snapped_'+inImg.split('/')[-1].split('_')[4]+'_clump_m18dB.tif'
#maskImgVal=1
#outputImage=inputImage.replace('.kea','_prob.kea')
#histBinWidths=[0.2,0.01]


#rsgislib.imagecalc.calcMaskImgPxlValProb(inputImage, inImgBands, maskImg, maskImgVal, outputImage, gdalformat, histBinWidths, True, True)

def extractImgPxlSample(inputImg, pxlNSample, noData=None):

	# Import the RIOS image reader
	from rios.imagereader import ImageReader

	first = True
	reader = ImageReader(inputImg, windowxsize=200, windowysize=200)
	print('Started .0.', end='', flush=True)
	outCount = 10
	for (info, block) in reader:
		if info.getPercent() > outCount:
			print('.'+str(int(outCount))+'.', end='', flush=True)
			outCount = outCount + 10

		blkShape = block.shape
		blkBands = block.reshape((blkShape[0], (blkShape[1]*blkShape[2])))

		blkBandsTrans = numpy.transpose(blkBands)

		if noData is not None:
			blkBandsTrans = blkBandsTrans[(blkBandsTrans!=noData).all(axis=1)]

		if blkBandsTrans.shape[0] > 0:
			nSamp = int((blkBandsTrans.shape[0])/pxlNSample)
			nSampRange = numpy.arange(0, nSamp, 1)*pxlNSample
			blkBandsTransSamp = blkBandsTrans[nSampRange]

			if first:
				outArr = blkBandsTransSamp
				first = False
			else:
				outArr = numpy.concatenate((outArr, blkBandsTransSamp), axis=0)
	print('. Completed')
	return outArr

def getPCAEigenVector(inputImg, pxlNSample, noData=None, outMatrixFile=None):

	# Read input data from image file.
	X = extractImgPxlSample(inputImg, pxlNSample, noData)

	print(str(X.shape[0]) + ' values were extracted from the input image.')

	pca = PCA()
	pca.fit(X)

	if outMatrixFile is not None:
		f = open(outMatrixFile, 'w')
		f.write('m='+str(pca.components_.shape[0])+'\n')
		f.write('n='+str(pca.components_.shape[1])+'\n')
		first = True
		for val in pca.components_.flatten():
			if first:
				f.write(str(val))
				first = False
			else:
				f.write(','+str(val))
		f.write('\n\n')
		f.flush()
		f.close()

	pcaComp = 1
	print("Prop. of variance explained:")
	for val in pca.explained_variance_ratio_:
		print('\t PCA Component ' + str(pcaComp) + ' = ' + str(round(val, 4)))
		pcaComp = pcaComp + 1

	return pca.components_, pca.explained_variance_ratio_


outputImage=inputImage.replace('.kea','_pca.kea')
outMatrixFile=inputImage.replace('.kea','_eigen.kea')
getPCAEigenVector(inputImg=clumpsMean, pxlNSample=1, noData=0, outMatrixFile=outMatrixFile)

#rsgislib.imagecalc.performImagePCA(clumpsMean, outputImg, eigenVecFile, nComponents=None, pxlNSample=100, gdalformat='KEA', datatype=rsgislib.TYPE_32UINT, noData=None, calcStats=True)


#ds = gdal.Open(clumpsMean)
#maskVV = np.array(ds.GetRasterBand(1).ReadAsArray())
##maskVV = maskVV.flatten()
#maskVV[maskVV == 0] = 'nan'
#ds=None
#
#ds = gdal.Open(clumpsMean)
#maskVVVH = np.array(ds.GetRasterBand(3).ReadAsArray())
##maskVV = maskVV.flatten()
#maskVVVH[maskVVVH == 0] = 'nan'
#ds=None
#
#stack=np.dstack((maskVV, maskVVVH))
#
##df = pd.DataFrame(stack, columns=['VV','VVdivVH'])
#
#pca = PCA(n_components=2)
#principalComponents = pca.fit_transform(stack)
#principalDf = pd.DataFrame(data = principalComponents
#             , columns = ['principal component 1', 'principal component 2'])
