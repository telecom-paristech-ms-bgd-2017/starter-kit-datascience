# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Author Manu
"""

import requests
import pandas as pd
import numpy as np
import json

# Constitution de la liste des villes
villes = pd.read_csv('/home/nux/Documents/INFMDI721/Crawling/VillesFrance2.csv', index_col=1)
ind = np.arange(len(villes))
vil_df = pd.DataFrame(index=ind, columns=ind)
vil_df.fillna('N')

# Constitution de l'url de requête
vil_str = ''
for i in range(len(villes)):
    vil_str += str(villes['Ville'][i]) + '|'

url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
url += 'origins=' + vil_str[0:-1]
url += '&' + 'destinations=' + vil_str[0:-1]
url += '&key=AIzaSyBNbKETeIFoDKTIvKy3oxUUVfr71oD_lcg'

# Requête URL
json_vil = requests.get(url).text
viljson = json.loads(str(json_vil))

# Exploitation du fichier JSON renvoyé et export to csv
for i in range(len(villes)):
    for j in range(len(villes)):
        vil_df[i][j] = viljson['rows'][i]['elements'][j]['distance']['text']
vil_df.to_csv('villas.csv')


