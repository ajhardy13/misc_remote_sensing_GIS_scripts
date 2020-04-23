import glob, csv

fileList=glob.glob('*_lee.tif.txt')
fileList=sorted(fileList)

values=[] # list of lists of values
date=[]

# iterate over text files and extract data from txt file and  store in sorted list
for fname in fileList:

	with open(fname) as f:
		lines = f.readlines()
	content = [x.strip() for x in lines] # remove \n etc.
	content=sorted(content) # sort alphabetically
	
	date.append(fname.split('_')[5].split('T')[0])
	
#date=[]	
#name=[]
	val=[]
	name=[]
	
	for c in content:
			name.append(c.split(' ')[0])	
	for c in content:
			val.append(c.split('(')[1].split(')')[0]) # read in value
	values.append(val)

#print(date)

#open the csv file and write all the rows in the list of lists
with open('classification_importance.csv', 'w') as f:
	# loop through lines and extract info
	writer = csv.writer(f, lineterminator='\n')
	writer.writerow(name)
	for row in values:
		writer.writerow(row)
#print(date)
#date=zip(*date)
print(date)
with open('classification_importance_dates.csv', 'w') as f:
	writer = csv.writer(f, lineterminator='\n')
	writer.writerow(date)
		
#	with open('classification_importance.csv', 'a') as f:
#		# loop through lines and extract info
#		for c in content:
#			name=c.split(' ')[0] # read variable name
#			f.write(name+',')
#		date=fname.split('_')[5].split('T')[0]
#		f.write('\n')
#		f.write(date+',')


'''
		with open('classification_importance.csv', 'w') as f:
		# loop through lines and extract info
	f.write('\n')
	
for fname in fileList:
		#fname='importance_S1B_IW_GRDH_1SDV_20170105T165713_Sigma0_stack_lee.tif.txt'
	#print(fname)
	with open(fname) as f:
		lines = f.readlines()

	content = [x.strip() for x in lines] # remove \n etc.

	content=sorted(content) # sort alphabetically

	with open('classification_importance.csv', 'w') as f:		
		
		for c in content:		
			val=c.split('(')[1].split(')')[0] # read in value
			f.write(val+',')
		f.write('\n')
'''