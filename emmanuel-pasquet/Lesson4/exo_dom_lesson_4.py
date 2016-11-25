import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re


# Constitution de l'url de requête
url = 'https://www.leboncoin.fr/annonces/offres/ile_de_france/?th=1&q=renault%20zoe&it=1&parrot=0'

# Selectionner les voitures parmi les annonces de la page
req = requests.get(url).text
soup = BeautifulSoup(req, 'html.parser')
zoe_links = []
for link in soup.find_all('a'):
    strink = str(link.get('href'))
    if strink[:23] == '//www.leboncoin.fr/voit':
        zoe_links.append(strink)

###########################################################################
# Ouvrir les annonces des voitures une par une et récupérer les éléments

# Ouverture
url = 'http://' + zoe_links[2][2:]
req = requests.get(url).text
soup = BeautifulSoup(req, 'html.parser')

# Récupération
ispro = soup.find(class_='ispro').text[:3]
prix = soup.find(class_='item_price clearfix').find(class_='value').text
prix_pat = '[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
prix = re.
print(prix)
