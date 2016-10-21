
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import numpy as np
import googlemaps
from pandas import DataFrame, Series


#@ MahzadK October 2016

ville1 =  "paris"
ville2 =  "nantes"

key =  "AIzaSyA4EYDHrnYQMADmfVsrlxA07mweSTWnkzs"
gmaps = googlemaps.Client(key=key)
villes =  ['Paris', 'Marseille', 'Lyon']

distance = gmaps.distance_matrix(villes, villes)['rows']

dis=[]
for row in distances

#resjson = json.loads(distance).keys()

print(distance)
