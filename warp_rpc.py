import glob, subprocess

fileList=glob.glob('/Users/Andy/Documents/Zambia/RemoteSensing/Pleiades/Unzipped/March/*/*_MS_*/*.TIF')
for file in fileList:
	outFile='/Users/Andy/Documents/Zambia/RemoteSensing/Pleiades/Unzipped/MS_TIFF/Warp/March/'+file.split('/')[-1].split('.')[0]+'_warp.tif'
	cmd="gdalwarp -rpc '%s' '%s'" %(file,outFile)
	try:
	
		print('Processing: '+file.split('/')[-1])
		subprocess.call(cmd, shell=True)
	except Exception:
		print('Failed to process: '+file.split('/')[-1])

# gdalwarp -rpc IMG_PHR1A_MS_201509141606268_SEN_1627093101-002_R1C1.TIF IMG_PHR1A_MS_201509141606268_SEN_1627093101-002_R1C1_projected.TIF

# gdalwarp -rpc /Users/Andy/Documents/Zambia/RemoteSensing/Pleiades/Unzipped/FCGC600483937/IMG_PHR1B_MS_002/IMG_PHR1B_MS_201707020853008_SEN_2379650101-002_R1C1.TIF /Users/Andy/Documents/Zambia/RemoteSensing/Pleiades/Unzipped/MS_TIFF/Warp/IMG_PHR1B_MS_201707020853008_SEN_2379650101-002_R1C1_warp.TIF