import requests
from bs4 import BeautifulSoup
import pandas as pd

def exploring(id_commune, id_departement, year, hashmap):
	try:
		ville = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom='
			+ "%03d"%id_commune + '&dep=' + "%03d"%id_departement
			+ '&type=BPS&param=5&exercice=' + str(year) )
		soup = BeautifulSoup(ville.text, 'html.parser')

		

		for x in soup.find_all('tr') :
			if x.find_all(class_="libellepetit") != [] and "DEPARTEMENT" in x.find_all(class_="libellepetit")[0].text:
				hashmap['departement'].append(x.find_all(class_="libellepetit")[0].text.split(' : ')[1])
				hashmap['commune'].append(x.find_all(class_="G")[0].text)
				hashmap['year'].append(year)

			elif x.find_all(class_="libellepetit G") != [] and "TOTAL" in x.find_all(class_="libellepetit G")[0].text:
				title_M = x.find_all(class_="libellepetit G")[0].text.split('>')[0].split(' = ')[0] + ' (Moyenne de la strate)'
				title_E = x.find_all(class_="libellepetit G")[0].text.split('>')[0].split(' = ')[0] + ' (Euros par habitant)'

				if title_E not in hashmap.keys() and title_M not in hashmap.keys():
					print(hashmap.keys())
					hashmap[title_M] = x.find_all(class_="montantpetit G")[2].text.replace('\xa0','')
					hashmap[title_E] = x.find_all(class_="montantpetit G")[1].text.replace('\xa0','')
				else:
					hashmap[title_M].append( x.find_all(class_="montantpetit G")[2].text.replace('\xa0','') )
					hashmap[title_E].append( x.find_all(class_="montantpetit G")[1].text.replace('\xa0','') )
		return True
	except:
		return False
 
futur_df = {'year' : [], 'departement' : [], 'commune' : [], 'TOTAL DES PRODUITS DE FONCTIONNEMENT (Euros par habitant)' : [],
'TOTAL DES PRODUITS DE FONCTIONNEMENT (Moyenne de la strate)' : [], 'TOTAL DES EMPLOIS D\'INVESTISSEMENT (Moyenne de la strate)' : [],
'TOTAL DES EMPLOIS D\'INVESTISSEMENT (Euros par habitant)' : [], 'TOTAL DES CHARGES DE FONCTIONNEMENT (Euros par habitant)' : [],
'TOTAL DES CHARGES DE FONCTIONNEMENT (Moyenne de la strate)' : [], 'TOTAL DES RESSOURCES D\'INVESTISSEMENT (Euros par habitant)' : [],
'TOTAL DES RESSOURCES D\'INVESTISSEMENT (Moyenne de la strate)' : []}

for i in range(2010,2014):
	for j in range (74, 77):
		is_exploring = True
		for k in range(1, 10):
			print('year ' + str(i) + ' departement ' + str(j) + ' commune ' + str(k) )
			is_exploring = exploring(k, j, i, futur_df)
			if not is_exploring:
				break

df = pd.DataFrame(futur_df)
df.to_csv('test.csv')
