import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBcRoLZRzWpmre3BMfZbkck57aZloEe160')


import json


url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=<orig>&destinations=<destins>"
url = "https://maps.googleapis.com/maps/api/distancematrix/json"

params = {'origins': 'Paris', 'destinations': 'Brest'}


resp = requests.get(url, params)
tutu=resp.json()


# map(lambda X:x['distaces','text'], row['elements'])






urlVille = "http://www.toutes-les-villes.com/villes-population.html"


req=requests.get(urlVille)

soup = bs4(req.text, 'html.parser')

allTr = soup.findall(class_='HomeTxtVert')

villes=pd.DataFrame(columns=["villes", "villes"])

cont=0
ii=0
while cont<30:























