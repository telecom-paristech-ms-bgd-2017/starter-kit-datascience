import pandas as pd
path = '/Users/Stephan/Desktop/Aliments.csv'
df = pd.read_csv(path, delimiter='\t')
df.head()
df.info()
df.describe()
df.columns()
list(df.columns)
df = df.set_index(['product_name'])
df.head()
df
#looking for Aliments with packaging
#Type of packaging
df['packaging'].value_counts()
df_packaging = df['packaging'].value_counts() > 100
df_packaging.head(50)
df_packaging.head(26)
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)
df.plot(figsize = (15, 10))
df_packaging[:26].plot(kind='bar')
#not interesting plot :(
df.plot(figsize = (15, 10))
df_packaging[:26].plot()
#great !!!
#idea : correlation between packaging and product sugar content ...
df_new = df[['packaging', 'fat_100g', 'sugars_100g', 'sodium_100g']]
df_new.head()
df_new.groupby('packaging').sum()
df_fat_packaging.plot()
