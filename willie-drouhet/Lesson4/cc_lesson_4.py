# coding: utf8
import requests
import ijson
import json
import csv
import oauth2 as oauth
import time
from urllib2 import urlopen, Request
import operator
import pandas as pd
from collections import OrderedDict
from datetime import date
import urllib2
from bs4 import BeautifulSoup
import numpy as np
import re


###############################################################################

#distance and travel duration 


gdes_villes=[ 	"Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier" ,"Bordeaux" ,        "       Rennes ","Le Havre" ,  "	Reims "]
gdes_villes1=[  "	Lille ",  "	Saint-Étienne",  "	Toulon ",  "	Grenoble" ,  "	Angers ",  "	Dijon ",  "	Brest ",  "	Le Mans",  "	Clermont-Ferrand" ,  "	Amiens "]
gdes_villes2=[  "	Aix-en-Provence",  "	Limoges",  "	Nîmes",  "	Tours",  "	Saint-Denis",  "	Villeurbanne",  "	Metz", " 	Besançon" ]
gdes_villes=gdes_villes+gdes_villes1+gdes_villes2
gdes_villes=[gdes_villes[a].strip().replace(' ','+') for a in range(len(gdes_villes))]

dist=[]


origins = gdes_villes
destinations=gdes_villes

f = open('key', 'r')
NEW_STRING=f.read()

YOUR_API_KEY=NEW_STRING

list_string_villes='|'.join(gdes_villes)



df_distances = pd.DataFrame([], columns=gdes_villes)
df_durations = pd.DataFrame([], columns=gdes_villes)





#########################################################
for a in range(len(gdes_villes)):
    requete_url="https://maps.googleapis.com/maps/api/distancematrix/json?origins="+gdes_villes[a]+"&destinations="+list_string_villes+"&language=fr-FR&key="+YOUR_API_KEY

    ############################################################ very important what is below (but subject to limits because of google api)
    api_limit_not_exceeded=0
    if api_limit_not_exceeded:
        request = Request(requete_url)
        response = urlopen(request)
        repoItem=json.load(response)
        df_distances.append([repoItem['rows'][0]['elements'][a]['distance']['value'] for a in range(len(repoItem['rows'][0]['elements']))],columns=gdes_villes)# = pd.DataFrame([], columns=gdes_villes)
        df_durations.append([repoItem['rows'][0]['elements'][a]['duration']['value'] for a in range(len(repoItem['rows'][0]['elements']))],columns=gdes_villes)# = pd.DataFrame([], columns=gdes_villes)
        
        df_distances.loc[a]=[repoItem['rows'][0]['elements'][a]['distance']['value'] for a in range(len(repoItem['rows'][0]['elements']))]
        df_durations.loc[a]=[repoItem['rows'][0]['elements'][a]['duration']['value'] for a in range(len(repoItem['rows'][0]['elements']))]

        
    else:
        df_distances.loc[a]=[b for b in range(30)]# = pd.DataFrame([], columns=gdes_villes)
        df_durations.loc[a]=[b for b in range(30)]# = pd.DataFrame([], columns=gdes_villes)

    
    print df_distances
    raw_input()

print df_distances
print df_durations
