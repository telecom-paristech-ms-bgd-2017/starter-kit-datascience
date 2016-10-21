import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# Prix de l'argus pour chaque type de Zoé

prix_argus = []

for type_zoe in ['intens', 'life', 'zen']:
    url_argus = 'http://www.lacentrale.fr/cote-auto-renault-zoe-' + type_zoe + '+charge+rapide-2013.html'

    r_argus = requests.get(url_argus)
    soup_argus = BeautifulSoup(r_argus.text, 'html.parser')

    prix_argus.append(soup_argus.find(class_='f24 bGrey9L txtRed pL15 mL15').text.replace('€','').replace(' ','').strip())

# Données des Zoé sur le bon coin et construction du dictionnaire
data = {}


url = 'https://www.leboncoin.fr/voitures/offres/ile_de_france/?th=1&parrot=0&brd=Renault&mdl=Zoe'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

list_an = soup.select('#listingAds ul')[0]
links = ['http:' + a['href'] for a in list_an.select('li > a')]


regex_type_zoe = re.compile(r'Zen|intens|Life', flags = re.IGNORECASE)
regex_pro = re.compile(r'pro', flags=re.IGNORECASE)


for link in links :
    data[link]={}
    r_an = requests.get(link)
    soup_an = BeautifulSoup(r_an.text, 'html.parser')
    titre_an = soup_an.find(class_='no-border').get_text().replace('\n','').replace('\t','').strip()
    data[link]["titre_an"]= titre_an
    if regex_type_zoe.search(titre_an):
        type_zoe = regex_type_zoe.search(titre_an).group(0)
        data[link]["type_zoe"] = type_zoe
    else:
        continue

    # find the owner's type
    owner_type_tag = soup_an.find(class_="line line_pro noborder").text
    if owner_type_tag == '\n':
        type_owner = 'part'
        data[link]["type_owner"] = type_owner
    else:
        type_owner = 'pro'
        data[link]["type_owner"] = type_owner

    # Find the other elements in tags span, class = 'value'
    dat = soup_an.find_all('span', {'class':'value'})

    price = dat[0].text.replace(' ','').replace('\n','').replace('\xa0€','')
    price = price.encode("utf8").decode('ascii', 'ignore')
    data[link]["price"] = int(price)

    km = dat[5].text.replace('KM','').replace(' ','')
    data[link]["km"] = int(km)

    year = dat[4].text.replace(' ','').replace('\n','')
    data[link]["year"] = int(year)

    if data[link]["type_zoe"].lower() == 'intens':
        data[link]["prix_argus"] = prix_argus[0]
    elif data[link]["type_zoe"].lower() == 'life':
        data[link]["prix_argus"] = prix_argus[1]
    elif data[link]["type_zoe"].lower() == 'zen':
        data[link]["prix_argus"] = prix_argus[2]

df = pd.DataFrame.from_dict(data, orient='index')
for i in range(len(df.index)):
    df.ix[i,'titre_an'] = df.ix[i,'titre_an'].lower()
    df.ix[i, 'type_zoe'] = df.ix[i, 'type_zoe'].lower()

columns = ['price','prix_argus','km','year','type_zoe','type_owner']
result_boncoin = df.to_csv(path_or_buf='/Users/mayliscotadze/starter-kit-datascience/maylis-cotadze/Lesson4/result2.csv', columns = columns)
