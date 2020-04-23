import glob, matplotlib, csv
import pandas as pd
import rsgislib.imagecalc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# list input images
listImages=glob.glob('Fractions*.kea')
mask=glob.glob('*mask.kea')[0]

maskVal=rsgislib.imagecalc.countPxlsOfVal(mask, vals=[1])[0]
# extract pixel counts
countOW=[]
countEFV=[]
countWS=[]
countDRY=[]
countUNC=[]
nameList=[]
maskValues=[]
for img in listImages:
	maskValues.append(maskVal)
	nameList.append(img)
	countOW.append(rsgislib.imagecalc.countPxlsOfVal(img, vals=[1])[0])
	countWS.append(rsgislib.imagecalc.countPxlsOfVal(img, vals=[2])[0])
	countEFV.append(rsgislib.imagecalc.countPxlsOfVal(img, vals=[3])[0])
	countDRY.append(rsgislib.imagecalc.countPxlsOfVal(img, vals=[4])[0])
	countUNC.append(rsgislib.imagecalc.countPxlsOfVal(img, vals=[5])[0])

# create dataframe with values
df=pd.DataFrame(list(zip(nameList, countOW, countWS, countEFV, countDRY, countUNC, maskValues)), columns=['Img','OW','WS','EFV','DRY','UNC','MSK'])

df.to_csv('tropwet_out_values.csv')


# pixels that are na (slopes and forest)
# loop with multiple empty arrays, filled with vals=[4]
# add all together - if = count x 4 then na
# probably want this as a raster dont we?



# convert pixel counts to area
countOW=np.asarray(countOW)*(50*50)/1000000
countWS=np.asarray(countWS)*(50*50)/1000000
countEFV=np.asarray(countEFV)*(50*50)/1000000

# extract date information from filename
dateStr=[]
for img in listImages:
	month=int(img.split('_')[2].split('-')[0])+1
	year=img.split('_')[3]
	date='15/'+str(month)+'/'+year
	dateStr.append(date)

# convert to pandas data frame and set date column and sort
dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y') # date reader
dataFrame=pd.DataFrame({'Date':dateStr, 'OW':countOW, 'WS':countWS,'EFV':countEFV})
dataFrame['Date']=pd.to_datetime(dataFrame['Date'], format='%d/%m/%Y')
dataFrame=dataFrame.sort_values(by='Date')

# set plot parameters
matplotlib.rcParams['font.family'] = "arial"
matplotlib.rcParams['mathtext.default'] = 'regular'
pal = ["#58ACFA",  "#848484", "#A9F5D0"]

# plot the data against dates
fig, ax = plt.subplots()
dataFrame.plot.bar(x='Date',ax=ax,linewidth=0, color=pal, alpha=0.8, stacked=True, grid=True)
ax.set(ylabel='Area $km^2$')
ax.set(xlabel='')

# format date tick labels
ticklabels = ['']*len(dataFrame)
skip = len(dataFrame)//12
ticklabels[::skip] = dataFrame['Date'].iloc[::skip].dt.strftime('%b-%Y')
ax.xaxis.set_major_formatter(mticker.FixedFormatter(ticklabels))
fig.autofmt_xdate()