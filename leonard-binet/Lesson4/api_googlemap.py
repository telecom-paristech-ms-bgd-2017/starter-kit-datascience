# distance ville à ville des 30 plus grandes villes de France
# plus grandes villes en terme d'habitants
# distance en voiture
# tableau 30x30
# Utilisation de l'API de google

import requests
import ipdb
import pandas as pd
import json

API_key = "AIzaSyDHmFFvHNvFLfr8DJo6npwBZLQNnsKYXX4"

villes = [
    "Paris",
    "Lyon",
    "Marseille",
    "Lille"
]

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=API_key)

distances = gmaps.distance_matrix(villes, villes)

for row in distances:


def get_distance_json(origins=["Paris"], destinations=["Lyon"], key=API_key):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    origins = "origins=" + "|".join(origins)
    destinations = "destinations=" + "|".join(destinations)
    key = "key=" + key
    response = requests.get(url + "&" + origins + "&" +
                            destinations + "&" + key).text
    json_data = json.loads(response)
    df = pd.load(json_data)
    return df
