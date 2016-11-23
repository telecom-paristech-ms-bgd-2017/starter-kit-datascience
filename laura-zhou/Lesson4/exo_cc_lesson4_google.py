# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup 
import requests
import json 
import pandas as pd
from pprint import pprint
import numpy as np

# copy the list from http://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/
# and past into a xls file
workbook = pd.ExcelFile('list_ville.xls')
dictionary= {}
for sheet_name in workbook.sheet_names:
    df = workbook.parse(sheet_name) 
 
df = df.rename(columns={'Ville ': 'Ville'}) 

# print des villes et creation d'une liste de villes
l=[]
for i in range(df['Ville'].size):
    origine = df['Ville'][i].strip()
    l.append(origine)
    print(origine)


YOUR_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token=YOUR_API_KEY

def get_distance(origin, arrive):
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+
                        '&destinations='+arrive+'&key='+YOUR_API_KEY, headers=headers)
    me_json = response.json()
    dist = me_json["rows"][0]['elements'][0]['distance']['value']
    return dist

#matrice de zeros

distance_mat=np.zeros((len(l),len(l))) 

# on remplit la matrice avec les distance
for i in range(len(l)):
    for j in range(len(l)): 
        distance_mat[i][j] = get_distance(l[i],l[j]) 

# dataframe final
DF=pd.DataFrame(data=distance_mat/1000., # avoir les distance en km
             index=l,     
             columns=l)

print(DF)
#creation csv
DF.to_csv("distance_matrix.csv", sep=";", header = True)
