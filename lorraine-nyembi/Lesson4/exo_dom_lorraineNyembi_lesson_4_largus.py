# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine

L'objectif est de générer un fichier de données sur le prix des Renault Zoé
sur le marché de l'occasion en Ile de France, PACA et Aquitaine. 

Vous utiliserezleboncoin.fr comme source. Le fichier doit être propre et 
contenir les infos suivantes : version ( il y en a 3), année, kilométrage, 
prix, téléphone du propriétaire, est ce que la voiture est vendue par un 
professionnel ou un particulier.

Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous 
récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables
(pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.

https://www.npmjs.com/package/leboncoin-api
"""


#import urllib.request as ur
#from github3 import login, GitHub
#from getpass import getpass, getuser
#import sys

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import json


# Get from generic url to search all Renault Zoe sales in regions Ile-de-france, Aquitaine and PACA


MARQUE = 'Renault'
MODELE = 'Zoe'
REGIONS = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']
PAGES = 2



#jsonObj = json.loads(requests.get(GITHUB_URL))

#s = str(SOUP.text)
#user_repos_list = json.loads(s.format())
def getCarsIDUnitary(paramRegion,paramMarque, paramModele, paramTypeRecherche):

    # LOC is used for local variables that contains function parameters   
    # Variable definition and affectation
   
    LOC_REGION = paramRegion
    LOC_MODELE = paramModele
    LOC_MARQUE = paramMarque
    LOC_RECHERCHE = paramTypeRecherche
    CAR_ID = dirty_car_id = []
    for PAGE in range(1,PAGES):
        print(PAGE)
        if (LOC_RECHERCHE == 0):
            
            URL_PROFESSIONNEL = 'https://www.leboncoin.fr/voitures/offres/' \
                            + LOC_REGION + '/?o=' + str(PAGE) + '&brd=' + LOC_MARQUE + '&mdl=' + LOC_MODELE + '&f=c'
            
            RESULTS = requests.get(URL_PROFESSIONNEL)
            SOUP_PROFESSIONNEL = BeautifulSoup(RESULTS.text,'html.parser')
            MAIN_CONTENT = (SOUP_PROFESSIONNEL.find_all(class_='tabsContent block-white dontSwitch'))
            
        elif (LOC_RECHERCHE == 1):
            
            URL_PARTICULIER = 'https://www.leboncoin.fr/voitures/offres/' + LOC_REGION + '/?o=' + str(PAGE) + '&brd=' + LOC_MARQUE + '&mdl=' + LOC_MODELE + '&f=p'
            RESULTS = requests.get(URL_PARTICULIER)
            SOUP_PARTICULIER = BeautifulSoup(RESULTS.text,'html.parser')
            MAIN_CONTENT = (SOUP_PARTICULIER.find_all(class_='tabsContent block-white dontSwitch'))
            
        if LOC_RECHERCHE == 0 or LOC_RECHERCHE == 1:
            for content in MAIN_CONTENT:
                ALL_LI_TAG = content.find_all('li')
                
                for li_tag in ALL_LI_TAG:
                    info_from_li_tag = (li_tag.contents[1].get('data-info')).replace(':','')
                    info_from_li_tag = info_from_li_tag.replace(',','')
                    dirty_car_id.append(info_from_li_tag.split()[5])
                    #print(CAR_ID)
            for i in range(len(dirty_car_id)):
                CAR_ID[i] = dirty_car_id[i].replace('"', '')
        else:
            print('Veuillez renseigner le type de recherche: Particulier = %d, Professionnel = %d' %(0, 1))
        #print(MAIN_CONTENT)
              
    return CAR_ID


def getALLCarsID():

    ALL_CAR_ID = getCarsIDUnitary(REGIONS[0], MARQUE, MODELE, 0)  #PACA PARTICULIER
    ALL_CAR_ID = np.concatenate((ALL_CAR_ID, getCarsIDUnitary(REGIONS[1], MARQUE, MODELE, 0)), axis=0)  #IDF PARTICULIER
    ALL_CAR_ID = np.concatenate((ALL_CAR_ID, getCarsIDUnitary(REGIONS[2], MARQUE, MODELE, 0)), axis=0)  #AQUITAINE PARTICULIER
    SIZE_PART = len(ALL_CAR_ID)
    RECHERCHE_ARRAY = np.repeat(np.array(['Particulier']), SIZE_PART)

    ALL_CAR_ID = np.concatenate((ALL_CAR_ID, getCarsIDUnitary(REGIONS[0], MARQUE, MODELE, 1)), axis=0)  #PACA PROFESSIONNEL
    ALL_CAR_ID = np.concatenate((ALL_CAR_ID, getCarsIDUnitary(REGIONS[1], MARQUE, MODELE, 1)), axis=0)  #IDF PROFESSIONNEL
    ALL_CAR_ID = np.concatenate((ALL_CAR_ID, getCarsIDUnitary(REGIONS[2], MARQUE, MODELE, 1)), axis=0)  #AQUITAINE PROFESSIONNEL
    SIZE_TOTAL = len(ALL_CAR_ID)
    SIZE_PART = SIZE_TOTAL - SIZE_PART
    RECHERCHE_ARRAY = np.concatenate((RECHERCHE_ARRAY, np.repeat(np.array(['Professionnel']), SIZE_PART)), axis=0)

    MARQUE_ARRAY = np.repeat([MARQUE], SIZE_TOTAL)
    MODELE_ARRAY = np.repeat([MODELE], SIZE_TOTAL)
    MY_DICO = {'marques' : MARQUE_ARRAY, 'modele': MODELE_ARRAY,
              'ID voiture': ALL_CAR_ID, 'type recherche': RECHERCHE_ARRAY}

    DF = pd.DataFrame(MY_DICO)
    DF.to_csv('donnees_voitures_leBonCoin.csv')

    print(DF)

    return DF
getALLCarsID()



#tab = ['1035061660','990711542','988625609']
def completeCarFeatures():
#tab = ['1035061660','990711542','988625609']

  df3 = getALLCarsID()
  tab = df3['ID voiture']
  print(tab)
    
  ANNEES = KILOMETRAGES = PRIX = []
       
  REGION = ['Paris']
  PARAMETRES = ['Kilometrage','Annee','Prix']
  for variable in tab:
        result = requests.get('https://www.leboncoin.fr/voitures/'+str(variable)+'.htm?ca=12_s')
        soup = BeautifulSoup(result.text, 'html.parser')
         
    
        titre = soup.find_all(class_='no-border')
        titre = titre[0].get_text()
        titre = titre[14:21]
        if (titre == 'Renault'):
            montant = soup.find_all(class_='value')
            prix = montant[0].get_text()
            annee = montant[4].get_text()
            for elt in prix:
                if elt ==' ':
                    prix = prix.replace(' ','')
                if elt =='€':
                    prix = prix.replace('€','')
            prix = int(prix)
            kilometrage = montant[5].get_text()
            for elt1 in kilometrage:
                if elt1 ==' ':
                    kilometrage = kilometrage.replace(' ','')
                if elt1 =='K':
                    kilometrage = kilometrage.replace('K','')
                if elt1 =='M':
                    kilometrage = kilometrage.replace('M','')  
            ANNEES.append(int (annee))
            KILOMETRAGES.append(int(kilometrage))
            PRIX.append(int(prix))          
            l_1 = []
            for i in range (len(KILOMETRAGES)):
                l_1.append([KILOMETRAGES[i],ANNEES[i],PRIX[i]])
            REGION = REGION * len(KILOMETRAGES)  
            df = pd.DataFrame(l_1, index=REGION, columns=PARAMETRES)
  return df

#print(completeCarFeatures())
"""

    
#DF_ID =  getALLCarsID()
#CARS_ID = DF_ID['ID voiture']
#CAR_REGION = DF_ID['ID voiture']
    
#VERSIO = KILOMETRE = REGION = []
    
#for car_id in CARS_ID:
#1036839788
dirty_data_2 = []

PRIX = ANNEE = KM = VERSION = REGION = ''
RESULTS_ = requests.get('https://www.leboncoin.fr/voitures/1006686148.htm?ca=21_s')
CAR_SOUP = BeautifulSoup(RESULTS_.text, 'html.parser')
#print(CAR_SOUP)
PHONE_DIRTY_CONTENT = CAR_SOUP.find_all(class_='phone_number font-size-up')
GLOBAL_DESC = CAR_SOUP.find_all('body')#(class_='ua_FIR')
for desc in GLOBAL_DESC:
    info_from_body = ((desc.find_all('script'))[2].contents[0])#replace(':', '')
    #print(info_from_body.find('km'))
    #info_from_body = info_from_body.replace(',','')
    #dirty_data_2.append(info_from_body.split())
    dirty_data_2 = np.append(dirty_data_2, info_from_body.split())
    PRIX = dirty_data_2[103] #ok
    ANNEE = dirty_data_2[112] #ok
    KM = dirty_data_2[50] #OK
    VERSION = dirty_data_2[91] #ok
    REGION = dirty_data_2[52] #OK
    try:
        print(info_from_body.index('km'))
    except ValueError:
        pass
    #print((dirty_data_2))#, dirty_data_2[90], dirty_data_2[104], dirty_data_2[113], dirty_data_2[122])
    print('prix %s annee %s km %s version %s region %s' % (PRIX, ANNEE, KM, VERSION, REGION))
    
    #info_from_body = ((desc.find_all('script'))[2].contents[0]).replace('var utag_data = ', '')
    #print(str(info_from_body))
    #print(info_from_body.replace('var utag_data = ', ''))
    #print(type(ast.literal_eval(str(info_from_body))))

"""                    #print(CAR_ID)
#for i in range(len(dirty_car_id)):
#   CAR_ID[i] = dirty_car_id[i].replace('"', '')
#   
#print(DIRTY_DATA[2].contents[0].replace(':',''))


#jsonObj = json.loads(requests.get('https://www.leboncoin.fr/voitures/1036839788.htm?ca=21_s').text)
#print (jsonObj)
#s = str(SOUP.text)
#user_repos_list = json.loads(s.format())

#print(GLOBAL_DESC)
"""
for content in PHONE_DIRTY_CONTENT:
    ALL_A_TAG = content.find_all('a')
    
    #print(PHONE_DIRTY_CONTENT)    
    for a_tag in ALL_A_TAG:
        info_from_a_tag = (a_tag)#.contents[0].get('href').text)#.replace(' ','')
     #   print(info_from_a_tag)
            
"""        
