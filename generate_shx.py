import fnmatch
import os
import shapefile

# List all the shapefiles
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

shp_files = find('*.shp', '.')

for shp_file in shp_files:

  # Explicitly name the shp and dbf file objects
  # so pyshp ignores the missing/corrupt shx
  
  shp = open(shp_file, "rb")
  dbf = open(shp_file.replace("shp", "dbf"), "rb")
  r = shapefile.Reader(shp=shp, shx=None, dbf=dbf)
  w = shapefile.Writer(r.shapeType)
  
  # Copy everything from reader object to writer object
  
  w._shapes = r.shapes()
  w.records = r.records()
  w.fields = list(r.fields)
  
  # saving will generate the shx
  fixed_shp_file = os.path.join(os.path.dirname(shp_file),
                                "fixed_" + os.path.basename(shp_file))
  w.save(fixed_shp_file)