import requests
import json
import pandas as pd
myKey = 'AIzaSyAC35Od8rSo9jkvjficLUlFERjEs9pKx2Y'
URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Paris,France&destinations=Marseille,France&key=' + myKey
r = requests.get(URL)
j = json.loads(r.text)
distance_dict = j['rows'][0]['elements'][0]['distance']
