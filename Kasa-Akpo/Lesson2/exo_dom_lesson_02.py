import requests
from bs4 import BeautifulSoup
import sys


annee = [2010, 2011, 2012, 2013,2014]
arrondissement_paris = [75, 77, 78, 91, 92, 93, 94, 95]
for elt in annee:
    for elt1 in arrondissement_paris:
        result = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=0'+str(elt1)+'&type=BPS&param=5&exercice='+str(elt))
        soup = BeautifulSoup(result.text, 'html.parser')
        sous_titres = []
        montant = []
        print('Stats annee:' +str(elt))
        print('Arrondissement:'+str(elt1))
        sous_titres = soup.find_all(class_='libellepetit G')
        montant = soup.find_all(class_='montantpetit G')
        if (sous_titres != []):
            print(sous_titres[0].get_text())
            print("Euros par habitants:" +montant[1].get_text())
            print("Moyenne de la strate:" +montant[2].get_text())
            print(sous_titres[1].get_text())
            print("Euros par habitants:" +montant[4].get_text())
            print("Moyenne de la strate:" +montant[5].get_text())
            print(sous_titres[3].get_text())
            print("Euros par habitants:" +montant[10].get_text())
            print("Moyenne de la strate:" +montant[11].get_text())
            print(sous_titres[4].get_text())
            print("Euros par habitants:" +montant[13].get_text())
            print("Moyenne de la strate:" +montant[14].get_text())