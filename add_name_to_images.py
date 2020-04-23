
import gdal, os, glob, pandas, imageio, numpy
from osgeo import gdal

list=glob.glob('*.kea')
# add colour table
for f in list:
	out=f.replace('.kea','_colour.kea')
	cmd="gdaldem color-relief -of KEA %s colours.txt %s"  %(f, out)
	os.system(cmd)

# convert kea files to jpegs with reduction in resolution
list=glob.glob('*colour.kea')
for f in list:
	out=f.replace('.kea','.jpg')
	#out='./JPEG/Subset/'+out
	out='./JPEG/Subset_smaller/'+out
	#print(out)
	#cmd="gdal_translate -of JPEG -outsize 800 0 %s %s" %(f,out)
	#cmd="gdal_translate -of JPEG -projwin 22.7102 -14.6528 23.6384 -15.5930 -outsize 800 0 %s %s" %(f,out)
	cmd="gdal_translate -of JPEG -projwin 23.09387 -15.242 23.144 -15.2826 -outsize 800 0 %s %s" %(f,out)
	os.system(cmd)

list=glob.glob('./JPEG/Subset/*.jpg')	
list=glob.glob('./JPEG/Subset_smaller/*.jpg')	

# add text to corner of image
for file in list:
	#text=file.split('_')[0].split('/')[-1]
	text=file.split('_')[1].split('/')[-1]
	cmd="mogrify -fill white -undercolor '#00000080' -pointsize 50 -gravity NorthEast -annotate +10+10 '%s' '%s'" %(text,file)
	os.system(cmd)

##################################################################
## cd into JPEG drive
os.chdir('./JPEG/Subset')	
os.chdir('./JPEG/Subset_smaller')	
#list files in order of date
list=glob.glob('*.jpg')
#file=list[0]
listDates=[]
for file in list:
	dateString=file.split('_')[0]
	date=pandas.to_datetime(dateString, format='%d-%m-%Y')
	listDates.append(date)

listDates=sorted(listDates)
df=pandas.DataFrame(listDates) # convert to pandas df

# strip date as string
datesOut=[] # output list of dates in order
for i in df[0].astype(str):
	Y=i.split(' ')[0].split('-')[0]
	m=i.split(' ')[0].split('-')[1]
	d=i.split(' ')[0].split('-')[2]
	date=d+'-'+m+'-'+Y
	datesOut.append(date)

listOut=[] # final list of files in order
for d in datesOut:
	listOut.append(glob.glob(d+'*.jpg')[0])

newNames=[] # add order number to files
for l, num in zip(listOut,numpy.arange(1,len(listOut))):
	print(l)			  
	name=str(num)+'_'+l
	newNames.append(name)

for new, old in zip(newNames, listOut):
	cmd="cp %s /Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/Processed/Update/results_kea/JPEG/Ordered_smaller/%s" %(old,new)
	os.system(cmd)
	
	
	