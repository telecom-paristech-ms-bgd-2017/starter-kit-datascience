
# coding: utf-8

# In[7]:

import requests
from bs4 import BeautifulSoup


def extractData(departement,commune,year):

    r3= requests.post("http://alize2.finances.gouv.fr/communes/eneuro/tableau.php",{'ICOM':'commune','DEP':departement,
                                                                                'TYPE':'BPS','PARAM':'0',
                                                                                'dep':'','reg':'',
                                                                                'nomdep':'',
                                                                                'moysst':'','exercice':'',
                                                                                'param':'','type':'',
                                                                                'siren':'','comm':'0',
                                                                                'EXERCICE':year})
    soup = BeautifulSoup(r3.text, 'html.parser')
    cells = soup.findAll('td', {"class" : "libellepetit"})



    for cell in cells:
        listData=[]
        if (cell.string.strip () == "TOTAL DES PRODUITS DE FONCTIONNEMENT = A"):
            sibling = cell.findNextSibling ()
            print("******* TOTAL DES PRODUITS DE FONCTIONNEMENT = A "+" Departement= "+departement+" Année = "+year+ "******")
            while (sibling):
            #En milliers d'Euros	En euros par habitant	Moyenne de la strate
           #print ("\t" + sibling.string )
                listData.append(sibling.string.replace(u'\xa0',''))
                sibling = sibling.findNextSibling ()
            print ("En euros par habitant = "+ listData[1])
            print ("Moyenne de la strate  = "+ listData[2])
            print ("          ")

        elif (cell.string.strip () == "TOTAL DES CHARGES DE FONCTIONNEMENT = B"):
            listData=[]
            sibling = cell.findNextSibling ()
            print("******* TOTAL DES CHARGES DE FONCTIONNEMENT = B "+" Departement= "+departement+" Année = "+year+ "******")
            while (sibling):
                listData.append(sibling.string.replace(u'\xa0',''))
                sibling = sibling.findNextSibling ()
            print ("En euros par habitant = "+ listData[1])
            print ("Moyenne de la strate  = "+ listData[2])
            print ("          ")

        elif (cell.string.strip () == "TOTAL DES RESSOURCES D'INVESTISSEMENT = C"):
            listData=[]
            sibling = cell.findNextSibling ()
            print("******* TOTAL DES RESSOURCES D'INVESTISSEMENT = C "+" Departement= "+departement+" Année = "+year+ "******")
            while (sibling):
                listData.append(sibling.string.replace(u'\xa0',''))
                sibling = sibling.findNextSibling ()
            print ("En euros par habitant = "+ listData[1])
            print ("Moyenne de la strate  = "+ listData[2])
            print ("          ")

        elif (cell.string.strip () == "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"):
            listData=[]
            sibling = cell.findNextSibling ()
            print("******* TOTAL DES EMPLOIS D'INVESTISSEMENT = D "+" Departement= "+departement+" Année = "+year+ "******")
            while (sibling):
                listData.append(sibling.string.replace(u'\xa0',''))
                sibling = sibling.findNextSibling ()
            print ("En euros par habitant = "+ listData[1])
            print ("Moyenne de la strate  = "+ listData[2])
        else:
            print("")

# In[12]:
extractData('075','04','2008')
extractData('075','04','2015')


# In[ ]:
