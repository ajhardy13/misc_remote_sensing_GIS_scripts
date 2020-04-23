import rsgislib, numpy, os, time, glob, re
from rsgislib import imageutils, imagecalc
from rsgislib.imagecalc import BandDefn

start = time.time()

outputImage='classified_stack_occurrence.kea'
#bandNames = imageutils.getBandNames(inputImage)


# list snapped images and sort them
imageList=glob.glob('*.kea')
imageList=sorted(imageList)

# print out all the various bandDefns functions
bandNames = []

for img in imageList:
	date=img.split('_')[0]
	bandNames.append('b'+date)
	
for i, b in zip(imageList, bandNames):
	band='"'+b+'"'
	img='"'+i+'"'
#	bandDefns.append(BandDefn(band, inputImage, num))
	print("bandDefns.append(BandDefn("+band+"," + img + ','+str(1)+"))")
'''
bandDefns = []
bandDefns.append(BandDefn("b01-03-2018","01-03-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b01-10-2016","01-10-2016_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b04-08-2018","04-08-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b05-02-2018","05-02-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b05-06-2018","05-06-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b06-03-2017","06-03-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b06-04-2018","06-04-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b06-11-2016","06-11-2016_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b07-12-2017","07-12-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b08-10-2017","08-10-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b09-08-2017","09-08-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b10-02-2017","10-02-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b11-04-2017","11-04-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b11-07-2018","11-07-2018_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b12-01-2018","12-01-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b12-05-2018","12-05-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b12-12-2016","12-12-2016_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b13-03-2018","13-03-2018_S1_lee_subset_copy_nonan_classified.kea",1))
bandDefns.append(BandDefn("b13-10-2016","13-10-2016_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b13-11-2017","13-11-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b14-09-2017","14-09-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b16-04-2015","16-04-2015_S1_classified.kea",1))
bandDefns.append(BandDefn("b16-07-2017","16-07-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b16-08-2018","16-08-2018_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b17-01-2017","17-01-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b17-02-2018","17-02-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b17-05-2017","17-05-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b17-06-2018","17-06-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b18-03-2017","18-03-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b18-04-2018","18-04-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b18-11-2016","18-11-2016_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b19-09-2015","19-09-2015_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b19-12-2017","19-12-2017_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b20-10-2017","20-10-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b21-08-2017","21-08-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b22-02-2017","22-02-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b22-04-2016","22-04-2016_S1_classified.kea",1))
bandDefns.append(BandDefn("b22-06-2017","22-06-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b23-04-2017","23-04-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b23-07-2018","23-07-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b24-01-2018","24-01-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b24-05-2018","24-05-2018_S1_classified.kea",1))
bandDefns.append(BandDefn("b24-05-2018","24-05-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b24-12-2016","24-12-2016_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b25-03-2018","25-03-2018_S1_lee_classified.kea",1))
bandDefns.append(BandDefn("b25-10-2016","25-10-2016_S1_lee_classified_refined2.kea",1))
bandDefns.append(BandDefn("b25-11-2017","25-11-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b26-09-2017","26-09-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b28-07-2017","28-07-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b28-08-2018","28-08-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b29-01-2017","29-01-2017_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b29-05-2017","29-05-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b29-06-2018","29-06-2018_S1_lee_nonan_classified_refined2.kea",1))
bandDefns.append(BandDefn("b30-03-2017","30-03-2017_S1_classified.kea",1))
bandDefns.append(BandDefn("b30-04-2018","30-04-2018_S1_lee_classified.kea",1))
	

datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'

print('')
print('Creating water/non-water masks')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
# expression to give water (1) and no water (0) per date



imageList=['S1B_IW_GRDH_1SDV_20170105T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170117T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170129T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170222T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170306T165712_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170318T165713_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170423T165720_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170505T165715_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170517T165715_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170529T165716_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170610T165717_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170622T165717_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif', 'S1B_IW_GRDH_1SDV_20170704T165718_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170728T165719_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170809T165720_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170821T165721_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170902T165721_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20170926T165722_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20171113T165722_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20171125T165722_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20171207T165721_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20171219T165721_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea', 'S1B_IW_GRDH_1SDV_20171231T165720_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_otsu_snap_guf.kea']
'''

datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'
#################################################################
# extract water and veg water and store as series of binary images
'''
for img in imageList:
	bandDefns = []
	out='./binary/'+img.split('_')[0]+'b_water.kea'
	bandDefns.append(BandDefn('band',img,1))
	expression='(band==1) || (band==3) ?1:0'
	imagecalc.bandMath(out, expression, gdalformat, datatype, bandDefns)
'''


#################################################################
# for 20170423 
#S10423a='S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif'
#mean='S1B_IW_GRDH_1SDV_20170423T165655_VVAvg_snapped.kea'	
#bandDefns = []
##img='S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped_otsuSnap.tif'
##out=img.split('_')[4].split('T')[0]+'b_water.kea'
#out=S10423a.replace('.tif','_mask.tif')
#bandDefns.append(BandDefn('S10423a',S10423a,1))
#bandDefns.append(BandDefn('mean',mean,1))
##expression='(mean<-0.00052) && (S10423a!=2) ?S10423a:0'
#expression='(mean<-0.00052) ?S10423a:0'
#imagecalc.bandMath(out, expression, gdalformat, datatype, bandDefns)



for band in bandNames:
	expression=''
	expression+='(' + band + '==1) || (' + band + '==3) ' # select veg or open water
	expression+='?1:0' # if true give value of 1, else 0
	out=band+'_water.kea'
	imagecalc.bandMath(out, expression, gdalformat, datatype, bandDefns)

os.chdir('/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/Processed/Update/Complete/binary')
	
images=glob.glob('*.kea')
images=sorted(images)

bandNames = []
for img in images:
	bandNames.append('b'+img.split('-')[0]+img.split('-')[1]+img.split('-')[2].split('_')[0])


# print out all the various bandDefns functions

for b, i in zip(bandNames, images):
	print("bandDefns.append(BandDefn( '"+b+"','" + i + "',"+str(1)+"))")


print('Reading in the masks')
#print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
bandDefns = []

bandDefns.append(BandDefn( 'b01032018b','01-03-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b01102016b','01-10-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b04082018b','04-08-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b05022018b','05-02-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b05062018b','05-06-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b06032017b','06-03-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b06042018b','06-04-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b06112016b','06-11-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b07122017b','07-12-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b08102017b','08-10-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b09082017b','09-08-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b10022017b','10-02-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b11042017b','11-04-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b11072018b','11-07-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b12012018b','12-01-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b12052018b','12-05-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b12122016b','12-12-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b13102016b','13-10-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b13112017b','13-11-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b14092017b','14-09-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b16042015b','16-04-2015b_water.kea',1))
bandDefns.append(BandDefn( 'b16072017b','16-07-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b16082018b','16-08-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b17012017b','17-01-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b17022018b','17-02-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b17052017b','17-05-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b17062018b','17-06-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b18032017b','18-03-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b18042018b','18-04-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b18112016b','18-11-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b19092015b','19-09-2015b_water.kea',1))
bandDefns.append(BandDefn( 'b19122017b','19-12-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b20102017b','20-10-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b21082017b','21-08-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b22022017b','22-02-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b22042016b','22-04-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b22062017b','22-06-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b23042017b','23-04-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b23072018b','23-07-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b24012018b','24-01-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b24052018b','24-05-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b24122016b','24-12-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b25032018b','25-03-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b25102016b','25-10-2016b_water.kea',1))
bandDefns.append(BandDefn( 'b25112017b','25-11-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b26092017b','26-09-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b28072017b','28-07-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b28082018b','28-08-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b29012017b','29-01-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b29052017b','29-05-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b29062018b','29-06-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b30032017b','30-03-2017b_water.kea',1))
bandDefns.append(BandDefn( 'b30042018b','30-04-2018b_water.kea',1))

bandDefns = []
bandDefns.append(BandDefn( 'b01032018b','01-03-2018b_water.kea',1))
bandDefns.append(BandDefn( 'b01102016b','01-10-2016b_water.kea',1))
expression='b01032018b + b01032018b'
outputImage='test.kea'
imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)


print('')
print('Running band math to extract water occurrence')
print('It took {0:0.1f} minutes'.format((time.time() - start) / 60))
expression='(('
for band in bandNames:
	expression+= band + ' + '  # band plus

expression=expression[0:len(expression)-3] # remove final
expression+=') / ' + str((len(bandNames)-3)) + ') * 100'
print(expression)
datatype = rsgislib.TYPE_8UINT
gdalformat = 'KEA'
expression='((b01102016b + b04082018b + b05062018b + b06032017b + b06042018b + b06112016b + b07122017b + b08102017b + b09082017b + b10022017b + b11042017b + b11072018b + b12012018b + b12052018b + b12122016b + b13102016b + b13112017b + b14092017b + b16042015b + b16072017b + b16082018b + b17012017b + b17052017b + b17062018b + b18032017b + b18042018b + b18112016b + b19092015b + b19122017b + b20102017b + b21082017b + b22022017b + b22042016b + b22062017b + b23042017b + b23072018b + b24012018b + b24052018b + b24122016b + b25032018b + b25102016b + b25112017b + b26092017b + b28072017b + b28082018b + b29012017b + b29052017b + b29062018b + b30032017b + b30042018b) / 50) * 100'

exp='(('
for l in list:
	b=l.split("'")[1]
	exp+=b+' + '
	
exp+=') / 34) * 100'

expression='((b01102016b + b04082018b + b05062018b + b06112016b + b07122017b + b08102017b + b09082017b + b11072018b + b12012018b + b12122016b + b13102016b + b13112017b + b14092017b + b16072017b + b16082018b + b17012017b + b17062018b + b18112016b + b19092015b + b19122017b + b20102017b + b21082017b + b22062017b + b23072018b + b24012018b + b24122016b + b25102016b + b25112017b + b26092017b + b28072017b + b28082018b + b29012017b  + b29062018b ) / 33) * 100'

expression='((  b04082018b   + b06112016b   + b08102017b + b09082017b  + b13102016b + b13112017b + b14092017b +  b16082018b  + b18112016b + b19092015b + b20102017b + b21082017b + b25102016b + b25112017b + b26092017b + b28082018b ) / 16) * 100'
	
expression='((   b08102017b + b09082017b  + b13112017b + b14092017b + b20102017b + b21082017b +  b25112017b + b26092017b  ) / 8) * 100'	

expression='(( b06032017b + b10022017b + b11042017b + b17052017b + b18032017b + b22022017b + b23042017b + b24052018b + b29052017b + b30032017b) / 10) * 100'


imagecalc.bandMath(outputImage, expression, gdalformat, datatype, bandDefns)

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stamp

