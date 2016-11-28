from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import numpy
import json
import sys
url ="http://base-donnees-publique.medicaments.gouv.fr/index.php"

param = {'page':'1',
'affliste':'0',
'affNumero':'0',
'isAlphabet':'0',
'inClauseSubst':'0',
'nomSubstances':'',
'typeRecherche':'0',
'choixRecherche':'medicament',
'paginationUsed':'0',
'txtCaracteres':'ibuprofene',
'btnMedic.x':'12',
'btnMedic.y':'10',
'btnMedic':'Rechercher',
'radLibelle':'1',
'txtCaracteresSub':'',
'radLibelleSub':'4'}

#\s([\w\s\]+)\s(\d+)\s?([a-zA-Z%]+) ,([\w\sé]+)

#(^(\w)+\s)[0-9]+\s?[a-z]+[és]

resultat = requests.post(url, param)
html = resultat.content
soup = BeautifulSoup(html, 'lxml')
#list_med = soup.find_all('td', attrs={'class': 'ResultRowDeno'})


df = pd.DataFrame()
d = numpy.array([])

med = soup.find_all('a', attrs={'class': 'standart'})#.text.replace('\t','')
liens = map(lambda x: x['href'] , soup.find_all(class_="standart"))


s = requests.Session()
for m, link in zip(med,liens):
    m=m.text.replace('\t','')
    if re.search(r'(^(\w)+\s)((\w)+\s)+[0-9%]+', m) is not None :
        molecule = re.search(r'(^(\w)+\s)((\w)+\s)+[0-9%]+', m).group(0)
    else:
        molecule ="NA"
    url ="http://base-donnees-publique.medicaments.gouv.fr/"+link
    details_med = requests.get(url)
    soup = BeautifulSoup(details_med.text, 'html.parser')
    try:
        composant = soup.find('li', attrs={'class': 'composant'}).text.replace(' ','').replace(u'\n','').replace(u'\t','')

    except AttributeError:

        print ("composant non renseigné")
    try :
        laboratoir = soup.find('ul', attrs={'class': 'autresInfosListe'}).findChildren('li')[0].text.replace(' ','').replace(u'\n','').replace(u'\t','')

    except AttributeError:
        print("composant non renseigné")

    df = df.append({"medicament": m, "molecule": molecule, "composant": composant,"laboratoire": laboratoir},ignore_index=True)


df.to_csv('detail_ibuprpfene.csv')











