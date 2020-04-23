import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns



data = 'classification_importance.csv'
df=pd.read_csv(data,header='infer',index_col=0)
#plt.pcolor(df)

matplotlib.rcParams['font.family'] = "arial"
matplotlib.rcParams['font.size'] = 8

sns.heatmap(df, annot=True, annot_kws={"size": 8}, fmt='.2f', cmap="coolwarm", cbar_kws={'label': 'Importance'})

plt.show()