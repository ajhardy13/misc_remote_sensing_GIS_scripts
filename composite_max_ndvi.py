import rsgislib, glob
from rsgislib import imageutils


inImgsPattern='/my/folder/scturcture/*.kea'
rBand=3
nBand=4
outRefImg='outRefImg.kea'
outCompImg='outCompImg.kea'
rsgislib.imageutils.imagecomp.createMaxNDVIComposite(inImgsPattern, rBand, nBand, outRefImg, outCompImg, tmpPath='./tmp', gdalFormat='KEA', dataType=None, calcStats=True)