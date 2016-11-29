import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns

path = "aliments.csv"
data = pd.read_csv(path, sep = '\t', skiprows=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21])

data['vitamin-c_100g'].describe()
df_vitamin_c  = data.dropna(subset=['vitamin-c_100g'])
#df_vitamin_c.sort('quantity',ascending=False)['product_name']
dataV = data['stores'].value_counts()>30
print(dataV)
