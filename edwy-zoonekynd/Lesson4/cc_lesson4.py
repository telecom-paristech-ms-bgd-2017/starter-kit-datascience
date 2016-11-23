from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from urllib.request import urlopen


url = 'http://www.insee.fr/fr/mobile/etudes/document.asp?reg_id=0&ref_id=T15F014'
html = urlopen(url)
obj = BeautifulSoup(html, "lxml")
lst2 = list()
lst = list()
res = obj.findAll("td", class_="etendue-ligne")
res2 = obj.findAll(class_="tab-chiffre")

for el2 in res2[0:30]:
    u = el2.get_text()
    lst2.append(u)

for el in res:
    v = el.get_text()
    lst.append(v)
lst = lst[1::2][0:30]
final = pd.DataFrame(list(zip(lst, lst2)), columns=['Ville', 'Population'])
final['Ville'] = final['Ville'].replace(
    'Saint-Denis (La Réunion)', 'Saint-Denis')


Key = 'AIzaSyDeQzdxwFFWxraQI_6SrcYtXpB8BmNAzTY'
url_base = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

matrix = np.zeros([30, 30])
print(final['Ville'][2])

for k in range(29,30):
    for i in range(28,29):
        dic = {'units': 'metric', 'origins': final['Ville'][k],
           'destinations': final['Ville'][i], 'key': Key}
        r = requests.get(url_base, params=dic)
        raw = r.json()['rows'][0]['elements'][0]['distance']['text'].split()[0]
        raw = float(raw.replace(",",""))
        matrix[k,i] = raw




