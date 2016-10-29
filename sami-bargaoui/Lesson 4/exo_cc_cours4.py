from sklearn import linear_model
import numpy as np
import pandas
import requests
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import urllib, json

def GetSoupFromUrl(url):
    request=requests.get(url)
    return BeautifulSoup(request.text, 'html.parser')

fichier = 'Villes_france.csv'
data = pd.read_csv(fichier, sep=',')
print data
villes=data['Villes']
mytoken = 'AIzaSyDWg78VWNp8ROgTUZDt8rKGVXMf9R98p5U'

distanceTotale=[]
distance=[]
ville=[]
for ville1 in villes:
	distance=[]
	for ville2 in villes:
		map = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+ville1+'&destinations='+ville2+'&language=fr-FR&key='+mytoken
		googleResponse = urllib.urlopen(map)
		jsonResponse = json.loads(googleResponse.read())
		distance.append(jsonResponse['rows'][0]['elements'][0]['distance']['value'])

	distanceTotale.append(distance)
	ville.append(ville1)

Result_DF = pd.DataFrame(data=distanceTotale, columns=ville,index=ville)
Result_DF.to_csv("ResultsVilles.csv")

