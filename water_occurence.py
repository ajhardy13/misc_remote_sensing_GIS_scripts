import rsgislib, numpy, os, time
from rsgislib import imageutils, imagecalc
from rsgislib.imagecalc import BandDefn

start = time.time()

inputImage='classified_stack_2017.kea'
outputImage='classified_stack_2017_occurrence.kea'
#bandNames = imageutils.getBandNames(inputImage)


# read stacked image in, each band 
bandDefns = []
#bandDefns.append(BandDefn('b20170105', inputImage, 1))
#bandDefns.append(BandDefn('b20170117', inputImage, 2))

bandNames = imageutils.getBandNames(inputImage) # band names
bandNum=numpy.arange(1,len(bandNames)+1) # band numbers 

# print out all the various bandDefns functions

#for b, num in zip(bandNames,bandNum):
#	band='"'+b+'"'
#	#bandDefns.append(BandDefn(band, inputImage, num))
#	print("bandDefns.append(BandDefn("+band+",inputImage," +str(num)+"))")
print('')
print('Reading in the relevant bands')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
bandDefns = []
bandDefns.append(BandDefn('b20170105',inputImage,1))
bandDefns.append(BandDefn('b20170117',inputImage,2))
bandDefns.append(BandDefn('b20170129',inputImage,3))
bandDefns.append(BandDefn('b20170222',inputImage,4))
bandDefns.append(BandDefn('b20170306',inputImage,5))
bandDefns.append(BandDefn('b20170318',inputImage,6))
bandDefns.append(BandDefn('b20170423',inputImage,7))
bandDefns.append(BandDefn('b20170423',inputImage,8))
bandDefns.append(BandDefn('b20170505',inputImage,9))
bandDefns.append(BandDefn('b20170517',inputImage,10))
bandDefns.append(BandDefn('b20170529',inputImage,11))
bandDefns.append(BandDefn('b20170610',inputImage,12))
bandDefns.append(BandDefn('b20170622',inputImage,13))
bandDefns.append(BandDefn('b20170704',inputImage,14))
bandDefns.append(BandDefn('b20170728',inputImage,15))
bandDefns.append(BandDefn('b20170809',inputImage,16))
bandDefns.append(BandDefn('b20170821',inputImage,17))
bandDefns.append(BandDefn('b20170902',inputImage,18))
bandDefns.append(BandDefn('b20170926',inputImage,19))
bandDefns.append(BandDefn('b20171113',inputImage,20))
bandDefns.append(BandDefn('b20171125',inputImage,21))
bandDefns.append(BandDefn('b20171207',inputImage,22))
bandDefns.append(BandDefn('b20171219',inputImage,23))
bandDefns.append(BandDefn('b20171231',inputImage,24))	

datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'

print('')
print('Creating water/non-water masks')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
# expression to give water (1) and no water (0) per date
for band in bandNames[0:2]:
	expression=''
	expression+='(' + band + '==1) || (' + band + '==3) ' # select veg or open water
	expression+='?1:0' # if true give value of 1, else 0
	outputImage=band+'_water.kea'
	imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

# print out all the various bandDefns functions
#for b in bandNames:
#	band='"'+b+'"'
#	img=b+'_water.kea'
#	#bandDefns.append(BandDefn(band, inputImage, num))
#	print("bandDefns.append(BandDefn("+band+"," + img + ','+str(1)+"))")
print('')
print('Reading in the masks')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
bandDefns.append(BandDefn("b20170105",b20170105_water.kea,1))
bandDefns.append(BandDefn("b20170117",b20170117_water.kea,1))
bandDefns.append(BandDefn("b20170129",b20170129_water.kea,1))
bandDefns.append(BandDefn("b20170222",b20170222_water.kea,1))
bandDefns.append(BandDefn("b20170306",b20170306_water.kea,1))
bandDefns.append(BandDefn("b20170318",b20170318_water.kea,1))
bandDefns.append(BandDefn("b20170423",b20170423_water.kea,1))
bandDefns.append(BandDefn("b20170423",b20170423_water.kea,1))
bandDefns.append(BandDefn("b20170505",b20170505_water.kea,1))
bandDefns.append(BandDefn("b20170517",b20170517_water.kea,1))
bandDefns.append(BandDefn("b20170529",b20170529_water.kea,1))
bandDefns.append(BandDefn("b20170610",b20170610_water.kea,1))
bandDefns.append(BandDefn("b20170622",b20170622_water.kea,1))
bandDefns.append(BandDefn("b20170704",b20170704_water.kea,1))
bandDefns.append(BandDefn("b20170728",b20170728_water.kea,1))
bandDefns.append(BandDefn("b20170809",b20170809_water.kea,1))
bandDefns.append(BandDefn("b20170821",b20170821_water.kea,1))
bandDefns.append(BandDefn("b20170902",b20170902_water.kea,1))
bandDefns.append(BandDefn("b20170926",b20170926_water.kea,1))
bandDefns.append(BandDefn("b20171113",b20171113_water.kea,1))
bandDefns.append(BandDefn("b20171125",b20171125_water.kea,1))
bandDefns.append(BandDefn("b20171207",b20171207_water.kea,1))
bandDefns.append(BandDefn("b20171219",b20171219_water.kea,1))
bandDefns.append(BandDefn("b20171231",b20171231_water.kea,1))

print('')
print('Running band math to extract water occurrence')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
expression='(('
for band in bandNames[0:2]:
	expression+= band + ' + '  # band plus

expression=expression[0:len(expression)-3] # remove final
expression+=') / ' + str(len(bandNames[0:2])) + ') * 100'

outputImage=band+'_water.kea'
imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp

