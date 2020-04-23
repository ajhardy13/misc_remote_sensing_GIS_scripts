import rsgislib, numpy
from rsgislib import imageutils, imagecalc
from rsgislib.imagecalc import BandDefn

inputImage='classified_stack_2017.kea'
outputImage='classified_stack_2017_max_wb.kea'
outputImage='classified_stack_2017_max_open_wb.kea'
outputImage='classified_stack_2017_max_veg_wb.kea'
#bandNames = imageutils.getBandNames(inputImage)


# read stacked image in, each band 
bandDefns = []
#bandDefns.append(BandDefn('b20170105', inputImage, 1))
#bandDefns.append(BandDefn('b20170117', inputImage, 2))

bandNames = imageutils.getBandNames(inputImage) # band names
bandNum=numpy.arange(1,len(bandNames)+1) # band numbers 

# print out all the various bandDefns functions
'''
for band, num in zip(bandNames,bandNum):
	band='"+band+"'
	bandDefns.append(BandDefn(band, inputImage, num))
	print("bandDefns.append(BandDefn('"+band+"',inputImage," +str(num)+"))")
'''
for b, num in zip(bandNames,bandNum):
	band='"'+b+'"'
	bandDefns.append(BandDefn(band, inputImage, num))
	print("bandDefns.append(BandDefn("+band+",inputImage," +str(num)+"))")


#bandDefns = []
#bandDefns.append(BandDefn('b20170105',inputImage,1))
#bandDefns.append(BandDefn('b20170117',inputImage,2))
#bandDefns.append(BandDefn('b20170129',inputImage,3))
#bandDefns.append(BandDefn('b20170222',inputImage,4))
#bandDefns.append(BandDefn('b20170306',inputImage,5))
#bandDefns.append(BandDefn('b20170318',inputImage,6))
#bandDefns.append(BandDefn('b20170423',inputImage,7))
#bandDefns.append(BandDefn('b20170423',inputImage,8))
#bandDefns.append(BandDefn('b20170505',inputImage,9))
#bandDefns.append(BandDefn('b20170517',inputImage,10))
#bandDefns.append(BandDefn('b20170529',inputImage,11))
#bandDefns.append(BandDefn('b20170610',inputImage,12))
#bandDefns.append(BandDefn('b20170622',inputImage,13))
#bandDefns.append(BandDefn('b20170704',inputImage,14))
#bandDefns.append(BandDefn('b20170728',inputImage,15))
#bandDefns.append(BandDefn('b20170809',inputImage,16))
#bandDefns.append(BandDefn('b20170821',inputImage,17))
#bandDefns.append(BandDefn('b20170902',inputImage,18))
#bandDefns.append(BandDefn('b20170926',inputImage,19))
#bandDefns.append(BandDefn('b20171113',inputImage,20))
#bandDefns.append(BandDefn('b20171125',inputImage,21))
#bandDefns.append(BandDefn('b20171207',inputImage,22))
#bandDefns.append(BandDefn('b20171219',inputImage,23))
#bandDefns.append(BandDefn('b20171231',inputImage,24))	

datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'

expression=''
for band in bandNames:
	#expression+='(' + band + '!=2) || '
	#expression+='(' + band + '==1) || '
	expression+='(' + band + '==3) || '

expression=expression[0:len(expression)-3] # remove final OR || condit	
expression+='?1:0' # if true give value of 1, else 0

#expression='(b20170105!=2)||(b20170117!=2)?1:0'

datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'

imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)
