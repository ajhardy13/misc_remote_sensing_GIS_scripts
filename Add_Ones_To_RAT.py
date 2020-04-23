#! /home/osian/miniconda3/bin/python3.5

import sys
import os
import numpy as np
from rios import rat
from osgeo import gdal

SegImg = 'Segmentation.kea'
NewColName = 'Mask1'

#######################################################
if not os.path.exists(SegImg):
    sys.exit('Error: Could not find the segmented image.')

ratDataset = gdal.Open(SegImg, 1) # read the image in read-write mode.
RefCol = rat.readColumn(ratDataset, 'Alpha') # read an existing RAT pythocolumn to get size.

Ones = np.ones_like(RefCol, dtype='uint8') # create an array of ones.
del RefCol

Ones[0] = 0 # assign zero to the first clump because it contains no data.

rat.writeColumn(ratDataset, NewColName, Ones) # write numpy array to RAT.
del Ones, ratDataset
print('Done.')

ref='S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped.tif'
mask='S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_mean.kea'
mask_snap='S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_mean_snap.kea'
gdalFormat = 'KEA'
rsgislib.imageutils.resampleImage2Match(ref, mask, mask_snap, gdalFormat, interpMethod='nearestneighbour', datatype=rsgislib.TYPE_8UINT)

bandDefns = []
bandDefns.append(BandDefn('class', 'S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_erf_clumptrain_mode_snapped.tif', 1))
bandDefns.append(BandDefn('mask', 'S1B_IW_GRDH_1SDV_20170423T165655_Sigma0_stack_lee_clumps2_mean.kea', 3))


gdalformat = 'KEA'
outName='b20170423_water_b.kea'
imagecalc.bandMath(outName, '(mask>0)&&(class!=2)?1:0', gdalformat, rsgislib.TYPE_8UINT, bandDefns)




