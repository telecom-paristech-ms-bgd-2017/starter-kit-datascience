# encoding: utf-8

import pandas as pd
from urllib.request import urlopen
import json

data = pd.read_csv('villes.csv')

data_out = pd.DataFrame(columns=['Départ', 'Arrivée', 'Distance'])

url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
api_key = 'AIzaSyA4EYDHrnYQMADmfVsrlxA07mweSTWnkzs'
destinations = ''

for reci in data.values:
    for recj in data.values:
        if recj[0] != reci[0]:
            query = url + 'origins=' + reci[0]
            query += '&destinations=' + recj[0] +'&mode=bicycling&language=fr-FR&'
            query += '&key=' + api_key
            response = json.loads(urlopen(query).read().decode('utf-8')))
            data_out.append({
                'Départ': reci[0],
                'Arrivée': recj[0],
                'Distance': response['rows'][0]['elements'][0]['distance']['value']
            })

print (data_out)
