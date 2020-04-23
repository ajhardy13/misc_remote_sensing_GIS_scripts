import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


# read the csv
data='water_extent_areas_km copy.csv'

dateparse = lambda x: pd.datetime.strptime(x, '%d-%m-%Y') # date reader
dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y') # date reader

df=pd.read_csv(data, parse_dates=['Date'], date_parser=dateparse) # read data


date=df['Date']
#openWater=df.iloc[:,1]
#vegWater=df.iloc[:,2]

matplotlib.rcParams['font.family'] = "arial"
matplotlib.rcParams['mathtext.default'] = 'regular'

pal = ["#848484","#A9F5D0", "#58ACFA",]

ax=df.plot.area(x=date,linewidth=0, color=pal, alpha=0.8, figsize=(5.9, 4), stacked=False, grid=True)



ax.set(ylabel='Area $km^2$')
ax.set(xlabel='')

ax.grid=True

plt.show()

#plot data