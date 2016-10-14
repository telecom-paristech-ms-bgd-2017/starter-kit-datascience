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

# L'exercice pour le cours prochain est le suivant: 
# - Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075

# - En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories qui leur appartiennent.
#Pour finir classer ces 256 contributors par leur note moyenne.﻿

###############################################################################


recup_dict=0
if recup_dict:  # true si on veut récupérer les dictionnaires / false si on veut travailler à partir des dictionaires déjà récupéré  

    ##########################################################################################################
    #Crawling des utilisateurs les plus fréquents

    adress='https://gist.github.com/paulmillr/2657075'
    html = urllib2.urlopen(adress).read()
    soup = BeautifulSoup(html)

    list_250_users=[]

    for a in soup.find_all('td'):

         if len(a.find_all(href=True))>0:

             if 'https://github.com/' in a.find_all(href=True)[0]['href']:

                 list_250_users.append(a.find_all(href=True)[0]['href'].split('https://github.com/')[1])


    ##########################################################################################################             
    #creation des dictionnaires (initialisation et remplissage)
    #clef   = utilisateur ; 
    #valeur = nombre moyen d'étoiles des repositories

    star_dic={}
    wat_dic={}

    access_token='1e9bfc92488ee503f37d1762ab61f1dde65a7326'

    for i in range(len(list_250_users)):

        adress_api="https://api.github.com/users/"+list_250_users[i]+"/repos"
        url =adress_api 
        token = '1e9bfc92488ee503f37d1762ab61f1dde65a7326'

        request = Request(url)
        request.add_header('Authorization', 'token %s' % token)
        response = urlopen(request)
        repoItem=json.load(response)


        stargaz=[]
        watch=[]

        if 1:     
            for a in repoItem:

                if 'stargazers_count' in a:
                    stargaz.append(a['stargazers_count'])
                if 'stargazers_count' in a:
                    watch.append(a['watchers_count'])

        star_dic[list_250_users[i]] = np.mean(stargaz)
        wat_dic[list_250_users[i]] = np.mean(watch)

        print 'user nb'
        print i

    ############################################################################################################################################
    #écriture des dictionnaires dans un .json pour les nombres de stargazers / watchers 

    with open('wat_dic.json', 'w') as fp:
        json.dump(wat_dic, fp)
    with open('star_dic.json', 'w') as fp:
        json.dump(star_dic, fp)










############################################################################################################################################
#Lecture des .json contenant les dictionnaires

with open('wat_dic.json', 'r') as f:
    wat_dic = json.load(f)

with open('star_dic.json', 'r') as f:
    star_dic = json.load(f)


############################################################################################################################################
#Tri des dictionaires selon la valeur des moyennes du nombre d'étoile pour les reposities de chacun des 256 utilisateurs les plus fréquents

star_dic_sorted_x = sorted(star_dic.items(), key=operator.itemgetter(1))
wat_dic_sorted_x = sorted(wat_dic.items(), key=operator.itemgetter(1))



############################################################################################################################################
#mise en forme des dictionnaire grâce à la librairie panda

df_wat_dic = pd.DataFrame(wat_dic_sorted_x)
df_star_dic = pd.DataFrame(star_dic_sorted_x)



############################################################################################################################################
#printing du tableau complet des utilisateurs selon leur nombre moyen d'etoiles 

pd.set_option('display.max_rows', len(star_dic_sorted_x))
print df_star_dic
pd.reset_option('display.max_rows')
print "touch any key !"
raw_input()




############################################################################################################################################
#exploration du caractère stargazer / watchers

ne = (df_star_dic != df_wat_dic).any(1)
x=ne
pd.set_option('display.max_rows', len(x))
print(x)
pd.reset_option('display.max_rows')
print "exploration du caractère stargazer / watchers (au dessus)"
print " On remarque qu'un des utilisateurs a un nombre de stargazer différent du nombre de watchers ! ?"





