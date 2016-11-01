import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
result = requests.get('https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es')
soup = BeautifulSoup(result.text, 'html.parser')
nombre_ville = 30
ville = []
distance_dict = []
duration_dict = []
temp = np.zeros([nombre_ville])
temp = pd.DataFrame(temp , columns=['drop'])
for i in range (1, nombre_ville+1) :
    nom_ville = soup.find_all('tr')[i].find_all('td')[1].find('b').text.replace(u'\xa0', '')
    ville.append(nom_ville)

api_key = 'AIzaSyBkYzNq7sSfzpaWBQZr6KxT4fCS90pPkb8'

for i in range(len(ville)) :
    for j in range(len(ville)) :
        api_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + ville[i] + '&destinations='+ ville[j]+ '&mode=driving ' + '&key=' + api_key
        r = requests.get(api_url)
        if r:
            json_contents = json.loads(r.text)
            distance = json_contents.get('rows')[0].get('elements')[0].get('distance').get('text')
            duration = json_contents.get('rows')[0].get('elements')[0].get('duration').get('text')
            distance_dict.append(distance)
            duration_dict.append(duration)
    distance_df_temp = pd.DataFrame(distance_dict,  columns=['%s' % ville[i]])
    distance_dict = []
    temp = temp.join(distance_df_temp)
    df = temp.drop('drop',1)


print(df)

