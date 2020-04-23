'''
# extract data
arcsiextractdata.py -i ./RAW/ -o ./Inputs/

#  build arcsi commands
arcsibuildcmdslist.py -s ls8 -f GTiff --stats -p TOA \
        --outpath ./Outputs 
        -i ./Inputs -e MTL.txt -o LS8ARCSICmds.sh

#  build arcsi commands
arcsibuildcmdslist.py -s ls8 -f GTiff --stats -p RAD DOSAOTSGL SREF \
        --outpath ./Outputs --aeroimg ../WorldAerosolParams.kea \
        --atmosimg ../WorldAtmosphereParams.kea --dem ./Users/Andy/Documents/Sentinel/Scripts/Sentinel1_processing/Support_data/srtm_44_14.tif \
        --tmpath ./LS8/tmp --minaot 0.05 --maxaot 0.6 --simpledos \
        -i ./Inputs -e MTL.txt -o LS8ARCSICmds.sh
        

# exectute the command
sh LS8ARCSICmds.sh


# cmd=["gdalwarp -tr 0.000089831528412 0.000089831528412 " + input + " " + output] 

MTL='/Users/Andy/Documents/Tanzania/Landsat/Inputs/LC81670662014299LGN00/LC81670662014299LGN00_MTL.txt'

cmd=["arcsi.py -s ls8 -f GTiff --stats -p TOA --outpath ./Outputs -i " + MTL]

try:
	subprocess.call(cmd, shell=True)

except Exception:
	print('Failed to process')
	pass
'''	
	
	
	
arcsi.py -s ls8 -f KEA -p TOA --outpath ./Outputs -i /Users/Andy/Documents/Tanzania/Landsat/Inputs/LC81670662014299LGN00/LC81670662014299LGN00_MTL.txt;
arcsi.py -s ls8 -f KEA -p TOA --outpath ./Outputs -i /Users/Andy/Documents/Tanzania/Landsat/Inputs/LC81670662015158LGN00/LC81670662015158LGN00_MTL.txt;
arcsi.py -s ls8 -f KEA -p TOA --outpath ./Outputs -i /Users/Andy/Documents/Tanzania/Landsat/Inputs/LC81670662015190LGN00/LC81670662015190LGN00_MTL.txt;
arcsi.py -s ls8 -f KEA -p TOA --outpath ./Outputs -i /Users/Andy/Documents/Tanzania/Landsat/Inputs/LC81670662015222LGN00/LC81670662015222LGN00_MTL.txt

