import requests
import numpy as np
import json, requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

with open('D:/WORK/Big_Data/PYTHON/API_Maps.txt', 'r') as f:
     API_Key1 = f.read()
     f.closed
url1 = 'http://www.insee.fr/fr/themes/tableau.asp?reg_id=0&ref_id=nattef01214'
#API_Key1 = ' AIzaSyBz4aBEab74m7S08FbRqsNlBHBu4_426SU '

#trouver les N plus grandes villes de France et les mettre dans une liste
def use_API(Origin, Destination, mode_transport):
    url2 = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + Origin +'&destinations='+ Destination +'&mode='+ mode_transport +'&language=fr-FR&key=' + API_Key1
    results = requests.get(url2).json()
    for el in results.get('rows'):
        elements = el.get('elements')
        distance = elements[0]
        dist = distance.get('distance')
        d = (dist.get('value'))/1000
    return d

def get_the_biggest_city(url1, N):
   page = requests.post(url1)
   soup = BeautifulSoup(page.text, 'html.parser')
   city_list = []
   table = soup.find("table")
   table_body = table.find('tbody')#soup.find_all(class_="etendue-ligne")#, attrs={'class': 'etendue-ligne'}
   rows = table_body.find_all('tr')
   for row in rows:
       cols = row.find_all('td', class_='etendue-ligne')
       cols = [ele.text.strip() for ele in cols]
       city_list.append([ele for ele in cols if ele])
   for i in range(len(city_list)):
       city_list[i]= str(city_list[i]).replace('[\'', '').replace('\']', '')
    #return city_list
   if N > len(city_list):
       print('enter a number < 70')
   list_biggest_city = city_list[0:N]
   return list_biggest_city


N = 20
Origin = get_the_biggest_city(url1, N)
Destination = get_the_biggest_city(url1, N)
for i in range(0, N, 1):
    for j in range(0, N, 1):
        if Origin[i] != Destination[j]:
           print(Origin[i], '-', Destination[j], ' :', use_API(Origin[i], Destination[j], 'drive'), 'km')
