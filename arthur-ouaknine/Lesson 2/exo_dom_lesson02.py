# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 22:42:31 2016

@author: arthurouaknine
"""

from bs4 import BeautifulSoup
import requests

def getDataForTown():
    departement = 0
    while departement != "stop":
        departement = input("Entrez le département d'étude (stop pour arrêter) : ")
        if departement == "stop":
            break
        elif len(departement) == 1:
            departement = "0" + str(departement)
        for date in range(2009, 2014):
            url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=0"+str(departement)+"&type=BPS&param=5&exercice=" + str(date)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            dicoValeurs = getValueClean(soup, "montantpetit G")
            print("Données de la ville sélectionnée pour l'année " + str(date))
            if dicoValeurs != "yes":
                printResults(dicoValeurs)
                print()
                print("==================================")
                print()
                
  
def getValueClean(soup, classname):
    values = {}
    values['A'] = []
    values['B'] = []
    values['C'] = []
    values['D'] = []
    allDataValues = soup.find_all(class_=classname)
    error = "no"
    if allDataValues == []:
        print("Il n'y a pas de valeur pour cette année")
        error = "yes"
        return error
    else:
        dicoToFindValues = {'A': [1, 2], 'B': [4, 5], 'C': [10, 11], 'D': [13, 14]}
        for k, v in dicoToFindValues.items():
            values[k].append(int(allDataValues[v[0]].text.replace('</td>', '').replace('\xa0', '').replace(' ', '')))
            values[k].append(int(allDataValues[v[1]].text.replace('</td>', '').replace('\xa0', '').replace(' ', '')))
        return values


def printResults(dicoValues):
    print("Total des produits de dysfonctionnement, euros par habitant : "+ str(dicoValues['A'][0]) + ", moyenne par strate : "
    +str(dicoValues['A'][1]))
    print("Total des charges de fonctionnement, euros par habitant : " + str(dicoValues['B'][0]) + ", moyenne par strate : " +str(dicoValues['B'][1]))
    print("Total des ressources d'investissement, euros par habitant : " + str(dicoValues['C'][0]) + ", moyenne par strate : " +str(dicoValues['C'][1]))
    print("Total des emplois d'investissement, euros par habitant : " + str(dicoValues['D'][0]) + ", moyenne par strate : " +str(dicoValues['D'][1]))
    

getDataForTown()