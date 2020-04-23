import matplotlib
import pandas as pd
import matplotlib.pyplot as plt


# read the csv
data='classification_importance.csv'

dateparse = lambda x: pd.datetime.strptime(x, '%Y%m%d') # date reader

df=pd.read_csv(data, parse_dates=['Date'], date_parser=dateparse) # read data


date=df['Date']
#openWater=df.iloc[:,1]
#vegWater=df.iloc[:,2]

matplotlib.rcParams['font.family'] = "arial"
matplotlib.rcParams['mathtext.default'] = 'regular'

ax=df.plot(x=date, alpha=0.3, figsize=(5.9, 4))

ax.set(ylabel='Importance %')
ax.set(xlabel='')
plt.ylim(0.1, 0.24) 


plt.show()

#plot data