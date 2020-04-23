import glob, sys

fileList=glob.glob('*_lee.tif')
fileList=sorted(fileList)

sys.stdout = open('jobList.txt', 'w')

with open('jobList.txt', 'w') as f:
	for file in fileList:

			f.write('caffeinate python /Users/Andy/Documents/Python/Remote_sensing/S1_WB_mapping_combined_v5_mac.py -i ' + file + '\n')
#			f.write('scp ' + file + ' andy@144.124.82.72:/mnt/Data/Andy/Projects/Zambia/Sentinel_1' + '\n')
	