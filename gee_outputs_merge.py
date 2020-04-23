import glob, sys

# list all files
listFiles=glob.glob('*.tif')
listNames=[]

# list of month/year names
for l in listFiles:
	part1=l.split('FeatID')[0]+'FeatID'
	part2=l.split('FeatID')[1].split('-')[1]
	name=part1+'-'+part2
	listNames.append(name)


# extract unique values from list of names
uniqueListNames=list(set(listNames))


# open the jobList that will contain the output list of commands
jobList='merge_jobList.sh'
sys.stdout = open(jobList, 'w')


with open(jobList, 'w') as f:
	for n in uniqueListNames:
			outName=n+'.kea'
			
			f.write('gdal_merge.py -of KEA -ot Byte -o ' + n + '.kea ' + n +'*\n')