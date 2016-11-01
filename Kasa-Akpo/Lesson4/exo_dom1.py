import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import numpy as np
import pandas as pd


########################recuperation des id des vehicules a mettre dans l'url################



######################exploitation###################

tab = ['1035061660','990711542','988625609']
annees = []
kilometrages = []
prixx = []
villes = ['Paris']
Parametres = ['Kilometrage','Annee','Prix']
for variable in tab:
    result = requests.get('https://www.leboncoin.fr/voitures/'+str(variable)+'.htm?ca=12_s') 
    soup = BeautifulSoup(result.text, 'html.parser')
    titre = soup.find_all(class_='no-border')
    titre = titre[0].get_text()
    titre = titre[14:21]
    if (titre == 'Renault'):
        montant = soup.find_all(class_='value')
        prix = montant[0].get_text()
        annee = montant[4].get_text()
        for elt in prix:
            if elt ==' ' or elt =='€':
                prix = prix.replace(' ','')
                prix = prix.replace('€','')
        prix = int(prix)
        kilometrage = montant[5].get_text()
        for elt in kilometrage:
            if elt ==' ' or elt =='K' or elt =='M':
                kilometrage = kilometrage.replace(' ','')
                kilometrage = kilometrage.replace('K','')
                kilometrage = kilometrage.replace('M','')                 
        annees.append(int (annee))
        kilometrages.append(int(kilometrage))
        prixx.append(int(prix))          
l_1 = []
for i in range (len(kilometrages)):
    l_1.append([kilometrages[i],annees[i],prixx[i]])
villes = villes * len(kilometrages)   
df = pd.DataFrame(l_1, index=villes, columns=Parametres)
