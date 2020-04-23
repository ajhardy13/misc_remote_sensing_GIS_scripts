#!/Users/Andy/miniconda3/envs/osgeoenv/bin/python

#############################################
# rsgislibmosaic.py
#
#  Copyright 2014 RSGISLib.
#
#  RSGISLib: 'The remote sensing and GIS Software Library'
#
#  RSGISLib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  RSGISLib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RSGISLib.  If not, see <http://www.gnu.org/licenses/>.
#
# Purpose: A script to recursivly find files with a given search
# string and mosaic using RGISLib.
#
# Author: Dan Clewley
# Email: daniel.clewley@gmail.com
# Date: 28/08/2013
# Version: 1.0
# 
##############################################

import os, sys
import rsgislib
from rsgislib import imageutils
import argparse
import fnmatch

"""
# Print help
print('rsgislibmosaic.py script provides command line utility for')
print('mosaicking image files, including recursively finding files')
print('within an input directory.')
print('This script was distributed with RSGISLib 3.5.7')
print('Copyright (C) 2014 Peter Bunting and Daniel Clewley')
print('For support please email rsgislib-support@googlegroups.com\n')
"""

# Get input parameters
parser = argparse.ArgumentParser()
parser.add_argument("--inputimages", type=str, nargs='+', required=False, help="Provide a list of images to be mosaicked rather than search info.")
parser.add_argument("-i", "--indir", type=str, required=False, help="Input directory to recursively search")
parser.add_argument("-s", "--search", type=str, required=False, help="Search string, e.g., '*kea', must be in quotes.")
parser.add_argument("-o", "--outmosaic", type=str, required=True, help="Output mosaic file")
parser.add_argument("-l",'--outlist',type=str, default=None,help="Output text file with list of files in mosaic (optional)")
parser.add_argument("-ot",'--datatype',choices=['int8', 'int16', 'int32', 'int64', 'uint8', 'byte', 'uint16', 'uint32', 'uint64', 'float32', 'float64'], default='float32',help="Data type")
parser.add_argument("--backgroundval", type=float, default=0,help="Background Value (default 0)")
parser.add_argument("--skipval", type=float, default=0,help="Value to be skipped (nodata values) in the input images (default 0)")
parser.add_argument("--skipband", type=int, default=1,help="Band to check for skip val (default 1)")
parser.add_argument("--minpix", action='store_true', default=False, help="Use minimum pixel in overlap areas (default, use last image in)")
parser.add_argument("--maxpix", action='store_true', default=False, help="Use maximum pixel in overlap areas (default, use last image in)")
parser.add_argument("--nostats", action='store_true', default=False, help="Don't calculate statistics and pyramids for mosaic (default is to calculate)")
args = parser.parse_args()    

rsgisUtils = rsgislib.RSGISPyUtils()

search4InImgs = True
if args.inputimages != None:
    if len(args.inputimages) > 0:
        search4InImgs = False


if search4InImgs and ((args.indir == "") or (args.search == "")):
    print('ERROR: Either a list of input images (--inputimages) or a search path (--indir) and string (--search) did to be given.')
    sys.exit()


overlapBehaviour = 0
if args.minpix and args.maxpix:
    print("ERROR: Either '--minpix' or '--maxpix' expected (not both)")
    sys.exit()
elif args.minpix:
    print("Taking minimum pixel value in band {} for overlapping areas.".format(args.skipband))
    overlapBehaviour = 1
elif args.maxpix:
    print("Taking maximum pixel value in band {} for overlapping areas.".format(args.skipband))
    overlapBehaviour = 2
else:
    print("Using values of last image for overlapping areas.")

# Get output extension from input file
outFormat = rsgisUtils.getGDALFormatFromExt(args.outmosaic)

if search4InImgs:
    # Recursively find all files in the input directory using specified search string
    fileList = []
    
    # Walk through directory
    for dName, sdName, fList in os.walk(args.indir):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, args.search): # Match search string
                fileList.append(os.path.join(dName, fileName))
else:
    fileList = args.inputimages

fileCount=len(fileList)
if fileCount == 0:
    print('ERROR: No files found')
    sys.exit()
else:
    print('Found %i files'%fileCount)

# Save list of files
if args.outlist is not None:
    rsgisUtils.writeList2File(fileList, args.outlist)

print('Creating mosaic...')
t = rsgislib.RSGISTime()
t.start(True)
imageutils.createImageMosaic(fileList, args.outmosaic, args.backgroundval, args.skipval, args.skipband, overlapBehaviour, outFormat, rsgisUtils.getRSGISLibDataType(args.datatype))
t.end()

if not args.nostats:
    print('\nCalculating stats and pyramids...')
    t.start(True)
    imageutils.popImageStats(args.outmosaic, True, args.backgroundval, True)
    t.end()
print('rsgismosaic.py - Finished')
    
