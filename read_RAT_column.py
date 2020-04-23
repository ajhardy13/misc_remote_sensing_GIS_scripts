inRatFile='S1B_IW_GRDH_1SDV_20170117T165713_Sigma0_stack_lee_clumps2.kea'
ratDataset = gdal.Open(inRatFile, gdal.GA_Update)
mode_pc=[]
mode_pc.append(rat.readColumn(ratDataset, 'OutClass_mode_pc'))
mode_pc=numpy.asarray(mode_pc[0])
total=len(mode_pc)
uncertain=(mode_pc < 1).sum()

pc_changed=(uncertain/total)*100

print(pc_changed)
