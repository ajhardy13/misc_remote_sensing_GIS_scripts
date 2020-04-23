#! /home/osian/miniconda3/bin/python3.5

''' Description: A script to perform an unsupervised pixel-based classification using the sklearn MiniBatchKMeans classifier.
The image is classified block-by-block to avoid memory errors associated with very large rasters.
Training pixels are randomly selected from each block, thereby ensuring that the training data is evenly distributed throughout the scene. 
Osian Roberts 10/11/2017'''

import argparse
import sys
import os
import shutil
import numpy
from osgeo import gdal
from sklearn.cluster import MiniBatchKMeans
from rsgislib import imageutils

parser = argparse.ArgumentParser(prog='Unsupervised K-means classification.', description='Perform an unsupervised pixel-based classification using the K-means classifier.')
parser.add_argument('-i', metavar='', type=str, help='Path to the input image.')
parser.add_argument('-o', metavar='', type=str, help='Path to the output image.')
parser.add_argument('-of', metavar='', type=str, choices=['KEA','GTiff'], default='KEA', help='Output format (KEA or GTiff). Defaults to KEA if undefined.')
parser.add_argument('-classes', metavar='', type=int, help='The number of spectral classes.')
parser.add_argument('-sample', metavar='', type=float, default=0.01, help='The ratio of valid pixels to use for classifier training. Default = 0.01 (1 percent).')
args = parser.parse_args()

#########################################################################################################################################################################################

# terminate the script when incorrect inputs are provided:
if args.i == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an input image.')
if args.o == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify an output image.')
if args.classes == None:
	parser.print_help()
	sys.exit('\n' + 'Error: Please specify the number of spectral classes.')

# terminate the script if the input image does not exist
if not os.path.exists(args.i):
	parser.print_help()
	sys.exit('\n' + 'Error: The input image does not exist. Check file path.')

#########################################################################################################################################################################################
def ProgressBar(n_tasks, progress):
	'''
	A function to display a progress bar on an unix terminal.
	Source: https://stackoverflow.com/questions/3160699/python-progress-bar
	'''
	barLength, status = 50, ''
	progress = float(progress) / float(n_tasks)
	if progress >= 1.0:
		progress = 1
		status = 'Done. \n'
	block = round(barLength * progress)
	text = '\r{} {:.0f}% {}'.format('#' * block + '-' * (barLength - block), round(progress * 100, 0), status)
	sys.stdout.write(text)
	sys.stdout.flush()

def GetImageBlocks(x_size, y_size, x_blocksize, y_blocksize):
	''' A function to calculate image block coordinates and dimensions.
	x_size = Pixels along the image x axis.
	y_size = Pixels along the image y axis.
	x_blocksize = Block size along the x axis.
	y_blocksize = Block size along the y axis.
	'''
	BlockInfo = []	
	
	for BlockY in range(0, y_size, y_blocksize):
		if BlockY + y_blocksize < y_size:
			rows = y_blocksize
		else:
			rows = y_size - BlockY

		for BlockX in range(0, x_size, x_blocksize):
			if BlockX + x_blocksize < x_size:
				cols = x_blocksize
			else:
				cols = x_size - BlockX

			BlockInfo.append(numpy.array([BlockX, BlockY, cols, rows]))
	return BlockInfo

def ClassifyImage(InputImage, OutputImage, GDALformat, SpectralClasses, SampleSize):
	''' A function to classify an image in blocks.'''
	# Define the classifier
	clf = MiniBatchKMeans(n_clusters=SpectralClasses, init='k-means++', max_iter=20, batch_size=1000, verbose=0, compute_labels=True, random_state=None, tol=0.0, max_no_improvement=100, init_size=10000, n_init=10, reassignment_ratio=0.05)
	
	print('Performing K-means unsupervised classification with '+str(SpectralClasses)+' spectral classes...')
	# Read the input image:
	InputRaster = gdal.Open(InputImage, gdal.GA_ReadOnly)
	RasterBands = InputRaster.RasterCount
	SRS = InputRaster.GetProjection()
	GeoT = InputRaster.GetGeoTransform()
	SizeX = InputRaster.RasterXSize
	SizeY = InputRaster.RasterYSize
	BlockSize = InputRaster.GetRasterBand(1).GetBlockSize()
	NoDataValue = InputRaster.GetRasterBand(1).GetNoDataValue()

	# Get the extent of each image block
	RasterBlocks = GetImageBlocks(SizeX, SizeY, BlockSize[0], BlockSize[1])
	n_blocks = len(RasterBlocks)

	TrainingData = []

	# iterate over each raster block and obtain a sample of pixels for classifier training
	print('Extracting training data from each image block...')
	for idx, Block in enumerate(RasterBlocks):
		BlockData = []

		# iterate over each raster band
		for Band in range(RasterBands):
			Band += 1
			BandData = InputRaster.GetRasterBand(Band).ReadAsArray(int(Block[0]), int(Block[1]), int(Block[2]), int(Block[3]))
			BandData = numpy.ma.compressed(numpy.ma.masked_equal(BandData, NoDataValue))
			if len(BandData) != 0:
				BlockData.append(BandData)
			del BandData

		if len(BlockData) != 0:
			Pixels = int(len(BlockData[0]))
			Sample = int(Pixels*SampleSize)
			BlockData = numpy.array(BlockData).T
			BlockData = BlockData[numpy.random.choice(BlockData.shape[0], size=Sample, replace=False), :] # Sample without replacement.
			TrainingData.append(BlockData)
			del BlockData
		ProgressBar(n_blocks-1, idx)

	# fit the training data
	TrainingData = numpy.concatenate(TrainingData)
	print('Training the classifier using '+str(len(TrainingData))+' pixels...')
	clf.fit(TrainingData, y=None)
	del TrainingData

	# Create output raster
	Driver = gdal.GetDriverByName(GDALformat)
	OutputRaster = Driver.Create(OutputImage, SizeX, SizeY, 1, 1)
	OutputRaster.SetProjection(SRS)
	OutputRaster.SetGeoTransform(GeoT) 
	OutBand = OutputRaster.GetRasterBand(1)
	OutBand.SetNoDataValue(0)

	# Read the input image in blocks and perform classification
	print('Classifying '+str(len(RasterBlocks))+' blocks...')
	for idx, Block in enumerate(RasterBlocks):
		TestData = []

		for Band in range(RasterBands):
			Band += 1
			BandData = InputRaster.GetRasterBand(Band).ReadAsArray(int(Block[0]), int(Block[1]), int(Block[2]), int(Block[3]))

			if Band == 1: # Create a binary mask for 
				BinaryMask = numpy.ones_like(BandData)
				BinaryMask = numpy.where(BandData == NoDataValue, 0, BinaryMask)

			TestData.append(BandData.flatten())
			del BandData

		# Perform classification
		TestData = numpy.array(TestData).T
		PredClass = clf.predict(TestData) + 1 # Add 1 to avoid having a class value = 0.
		del TestData

		PredClass = numpy.reshape(PredClass, (int(Block[3]), int(Block[2])))
		PredClass = PredClass * BinaryMask # Reclassify nodata regions to zero using Binary Mask.
		del BinaryMask

		# write classification to the output raster
		OutBand.WriteArray(PredClass, int(Block[0]), int(Block[1]))
		del PredClass
		ProgressBar(n_blocks-1, idx)

	del RasterBlocks

	# Close the input and output rasters 
	InputRaster, OutputRaster = None, None

	# Build image overviews for faster viewing in external software (e.g. QGIS or Tuiview)
	print('Generating image overviews...')
	imageutils.popImageStats(OutputImage, True, 0, True)

#########################################################################################################################################################################################

ClassifyImage(args.i, args.o, args.of, args.classes, args.sample)
