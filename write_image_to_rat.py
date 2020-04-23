import rsgislib
from rsgislib import rastergis

##############################################################################################   write stats from texture image to RAT from clumps

clumps='S1B_20170728_stack_lee_clip_clumps2.kea'
texture='S1B_20170728_stack_lee_clip_txt9.kea'

bs = []
bs.append(rastergis.BandAttStats(band=2, minField='VHtxtMin', maxField='VHtxtb1Max', meanField='VHtxtMean', sumField='VHtxtSum', stdDevField='VHtxtStdDev'))


rastergis.populateRATWithStats(texture, clumps, bs)