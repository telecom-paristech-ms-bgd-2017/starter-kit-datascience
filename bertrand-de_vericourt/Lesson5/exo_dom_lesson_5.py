
import requests
from bs4 import BeautifulSoup
import pandas as pd

################################ DENSITY DOCTORS in France ##############################

# looping over all months takes too much time
"""
value = 0
for i in range(13):
	strValue = str(i+1)
	if i+1 < 10:
		strValue = '0' + strValue
	data = '/Users/bertrrandBertrand/Downloads/R2015/R2015' + strValue + '.CSV'
	print("trying to load " + data)
	df_temp = pd.read_csv(data)
	if i==0:
		print("CONCAT: i= " + str(i))
		df_doctors = df_temp
	else:
		print("CONCAT: i= " + str(i))
		df_doctors = pd.concat(df_doctors, df_temp)
"""

url = 'R201501.CSV'

chunksize = 10 ** 2
for chunk in pd.read_csv(url, chunksize=chunksize, skiprows=2):
    process(chunk)

chunk.head(5)