
import rasterio, glob, os
import numpy as np

# read all the kea images in the input directory
listImages=glob.glob('*.kea')


# listNames=[]
# for img in listImages:
#     listNames.append(img.split('.')[0])

# loop to read each raster into array and store
allData=[]
for img in listImages:
    rasterData=rasterio.open(img)
    allData.append(rasterData.read(1))

# print img name and max value
for i, n in zip(allData, listImages):
    print(n + ': ' + str(np.max(i)))

# find max sum value across all images
ans=sum(allData)
# find global max
maxCount=len(allData)*5

# empty array for result and flag pixels that have max value
# i.e. always have a value of 5 which is unclassified
out=np.empty_like(ans)
out[np.where(ans==maxCount)] = 1

# write the output to use as a mask
outMask=img.split('_')[-2]+'_mask.tif'
with rasterio.Env():
    # Write an array as a raster band to a new 8-bit file. For
    # the new file's profile, we start with the profile of the source
    profile = rasterData.profile

    profile.update(driver='GTiff',dtype=rasterio.int8)

    with rasterio.open(outMask, 'w', **profile) as dst:
        dst.write(out.astype(rasterio.int8), 1)

os.system('gdal_translate -of KEA '+ outMask + ' ' + outMask.replace('.tif','.kea'))
os.remove(outMask)