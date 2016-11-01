from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
url = "http://www.cdiscount.com/informatique/ordinateurs-pc-portables/v-10709-10709.html"
html = urlopen(url)

obj = BeautifulSoup(html, "lxml")

res3 = obj.findAll("div", {"class": "prdtBTit"})

lst3 = list()
for v in res3:
    u = v.get_text()
    brand = u.split()[0]
    lst3.append(brand)


res4 = obj.findAll("div", {"class": "ecoBlk"})
lst4 = list()
for t in res4:
    e = t.get_text().replace("d'économie", " ").replace("€", " ").replace("%", " ")
    lst4.append(e)

a = list(zip(lst3, lst4))

a.sort(key=lambda tup: tup[1])
df = pd.DataFrame(a, columns=['Marque', 'Prix'])

df.columns = ['Marque', 'Prix']
df['Prix'] = df['Prix'].astype(float)
df['Marque'] = df['Marque'].map(lambda x: x if type(x)!=str else x.lower())

data = pd.DataFrame(df)
grouped = data.groupby(data['Marque']).mean()
print(grouped)

