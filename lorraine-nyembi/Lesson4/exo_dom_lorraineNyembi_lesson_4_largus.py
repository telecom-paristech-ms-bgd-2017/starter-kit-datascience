# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:35:28 2016

@author: lorraine

"""


import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


# Get from generic url to search all Renault Zoe sales in regions Ile-de-france, Aquitaine and PACA


MARQUE = 'Renault'
MODELE = 'Zoe'
REGIONS = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']
PAGES = 2

def clearData(s, typePrix):   # si typePrix = True, s est un prix, sinon s est le kilométrage
   
    for caracter in s: 
        if(typePrix == True):
            if caracter ==' ':
                s = s.replace(' ','')
            if caracter =='€':
                s = s.replace('€','')
          #  s = int(s)
        else:
            for caracter in s:
                if caracter ==' ':
                    s = s.replace(' ','')
                if caracter =='K':
                    s = s.replace('K','')
                if caracter =='M':
                    s = s.replace('M','')
    return s


def completeCarFeatures(paramAllCarIds):

  #df3 = getALLCarsID()
  allCarIds = paramAllCarIds #df3['ID voiture']
  sizeTab = len(allCarIds)
  KILOMETRAGES_ = np.zeros(sizeTab)
  PRIX_ = np.zeros(sizeTab)
  ANNEES_=  np.zeros(sizeTab)
  
  for i in range(1, len(allCarIds)):
   
     result = requests.get('https://www.leboncoin.fr/voitures/'+str(allCarIds[i])+'.htm?ca=12_s')
     soup = BeautifulSoup(result.text, 'html.parser')
         
     MONTANT = soup.find_all(class_='value')
     annee = MONTANT[4].get_text()
     ANNEES_[i] = int(float(annee))
    
     prix = MONTANT[0].get_text()
     prix = clearData(prix, True)
     PRIX_[i] = int(prix) 
     
     kilometrage = MONTANT[5].get_text()
     kilometrage = clearData(kilometrage, False)  
     KILOMETRAGES_[i] = int(kilometrage)
     
             
  #df = pd.DataFrame({ 'Kilometrage':KILOMETRAGES,'Annee':ANNEES,'Prix':PRIX, 'ID voiture':allCarIds})

  #df.to_csv('donnees_voitures_largus.csv')
  return KILOMETRAGES_, ANNEES_, PRIX_

# Recherche de données de voitures par région, marque, modèle par particulier ou professionnel 
def getDataUnitary(paramRegion,paramMarque, paramModele, paramTypeRecherche):

    # LOC is used for local variables that contains function parameters   
    # Variable definition and affectation
   
    LOC_REGION = paramRegion
    LOC_MODELE = paramModele
    LOC_MARQUE = paramMarque
    LOC_RECHERCHE = paramTypeRecherche
    CAR_ID = dirty_car_id = []
    for PAGE in range(1,PAGES):
        
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
                   
            for i in range(len(dirty_car_id)):
                CAR_ID[i] = dirty_car_id[i].replace('"', '')
        else:
            print('Veuillez renseigner le type de recherche: Particulier = %d, Professionnel = %d' %(0, 1))
    
    KILOMETRAGES = ANNEES =  PRIX = []
    KILOMETRAGES, ANNEES, PRIX = completeCarFeatures(CAR_ID)

    if (LOC_RECHERCHE == 0):
        type_recherche = "PARTICULIER"
    if (LOC_RECHERCHE == 1):
         type_recherche = "PROFESSIONNEL"
    df = pd.DataFrame({'region': LOC_REGION, 'kilometrage':KILOMETRAGES, 'annee':ANNEES, 'prix': PRIX, 'marque' : LOC_MARQUE, 'modele': LOC_MODELE,
              'ID voiture': CAR_ID, 'type recherche': type_recherche})
    #df.to_csv('donnees_voitures_leBonCoin.csv')

   # print(df)
               
    return  df


def getALLCarsData():

    ALL_CAR_ID = pd.DataFrame()
    df1 = getDataUnitary(REGIONS[0], MARQUE, MODELE, 0)  #PACA PARTICULIER
    df2 = getDataUnitary(REGIONS[1], MARQUE, MODELE, 0)  #IDF PARTICULIER
    df3 = getDataUnitary(REGIONS[2], MARQUE, MODELE, 0) #AQUITAINE PARTICULIER

    df4 = getDataUnitary(REGIONS[0], MARQUE, MODELE, 1)  #PACA PROFESSIONNEL
    df5 = getDataUnitary(REGIONS[1], MARQUE, MODELE, 1) #IDF PROFESSIONNEL
    df6 = getDataUnitary(REGIONS[2], MARQUE, MODELE, 1)  #AQUITAINE PROFESSIONNEL

    ALL_CAR_ID = pd.concat([df1, df2, df3, df4, df5, df6])

    ALL_CAR_ID = ALL_CAR_ID.set_index(np.arange( ALL_CAR_ID.region.count()))
    ALL_CAR_ID.to_csv('donnees_voitures_leBonCoin_argus.csv')
#
    print(ALL_CAR_ID)

    
    
getALLCarsData()


#df_carFeaturesPart2 = completeCarFeatures()

#allCarFeatures = df_carFeaturesPart2.merge(df_carFeaturesPart1)
