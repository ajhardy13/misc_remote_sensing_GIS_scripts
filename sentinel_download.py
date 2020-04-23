# https://pypi.python.org/pypi/sentinelsat

# sentinelsat -u ajhardy13 -p Geomatics123 -g 'intersects(22.951, -15.268)' -s 20171001 -e 20171101 --producttype GRD  --url "https://scihub.copernicus.eu/dhus"

sentinelsat -u ajhardy13 -p Geomatics123 -g '/Users/Andy/Documents/Mozambique/GIS/s1_download_area.json' -s 20190315 -e 20190328 --producttype GRD  --url "https://scihub.copernicus.eu/dhus" -d

sentinelsat -u ajhardy13 -p Geomatics123 -g '/Users/Andy/Documents/Zambia/RemoteSensing/Sentinel_1/GRD/Out/Subset/AccuracyAssessment/pleiades_bounding_box.json' -s 20180301 -e 20180329 --name *SDV* --producttype GRD  --url "https://scihub.copernicus.eu/dhus" -d


import subprocess,os.path, os, time
from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

start = time.time()

# input AOI as .shp
inputAOI='/Users/Andy/Documents/Mozambique/GIS/s1_download_area.shp' # vector file for defining AOI subset area
# vector file for defining AOI subset area

# set temporal query using ISO8601 format
# beginposition='[2017-01-01T00:00:00.000Z TO NOW]'
beginposition='[2017-01-01T00:00:00.000Z TO 2018-01-01T00:00:00.000Z]'
# beginposition='[2017-10-01T00:00:00.000Z TO NOW]'

# product/platform search options
platformname = 'Sentinel-1'
producttype='GRD'


# convert aoi to json 
jsonAOI=inputAOI.split('.')[0]+'.json'

if os.path.exists(jsonAOI):
	print('AOI already exists as .json')
	pass
else:
	print('Generating AOI .json')
	cmd="ogr2ogr -f GeoJSON -nlt POLYGON -skipfailures -overwrite '%s' '%s'" %(jsonAOI,inputAOI)
	subprocess.call(cmd, shell=True)
'''
cmd="ogr2ogr -f GeoJSON -nlt POLYGON -skipfailures -overwrite '%s' '%s'" %(jsonAOI,inputAOI)
subprocess.call(cmd, shell=True)
'''
# connect to the API
user='ajhardy13'
password='Geomatics123'

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id
# api.download(<product_id>)

# footprint='intersects(22.951, -15.268)' # any scene that intersects a central point lon, lat

# search by polygon, time, and Hub query keywords
footprint = geojson_to_wkt(read_geojson(jsonAOI))
products = api.query(footprint=footprint, beginposition=beginposition, platformname=platformname, producttype=producttype)

# query the product list
# items=list(products.items())



# download all results from the search
print('Downloading all products...')
api.download_all(products)
'''
# GeoJSON FeatureCollection containing footprints and metadata of the scenes
api.to_geojson(products)

# GeoPandas GeoDataFrame with the metadata of the scenes and the footprints as geometries
api.to_geopandas(products)

# Get basic information about the product: its title, file size, MD5 sum, date, footprint and
# its download url
api.get_product_odata(<product_id>)



# Get the product's full metadata available on the server
api.get_product_odata(<product_id>, full=True)
'''

os.system('afplay /System/Library/Sounds/Tink.aiff')
os.system('afplay /System/Library/Sounds/Tink.aiff')

print('It took {0:0.1f} minutes'.format((time.time() - start) / 60)) #time-stam
