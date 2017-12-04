import requests
from bs4 import BeautifulSoup
import sys



def getData(crawl, cat):
    record = False
    catList = []
    for c in crawl:

        if not c['rowTitle'].find(cat) == -1:
            record = True
            catList.append(c)
            continue

        if record and c['cat'] == 'Big':
            break

        if record:
            catList.append(c)
    return catList


#initialisation des variables
urlbase = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?'
# La liste des années traitées
Annees = [2010, 2011, 2012, 2013]
urlparam = {'icom': '056', 'dep': '075', 'type': 'BPS', 'param': '5'}
results = dict()
# On boucle sur les années à traiter
for annee in Annees:
    urlparam['exercice'] = annee
    # Lancement url
    r = requests.get(urlbase, params=urlparam)
    # Récupération du flux html
    soup = BeautifulSoup(r.content, 'html.parser')
    # On récupere le première ligne de
    filtre = 'table:nth-of-type(3) > tr:nth-of-type({0}) > td:nth-of-type({1})'
    crawl = []
    iRow = 6
    res = soup.select(filtre.format(iRow, 4))

    while not len(res) == 0:

        if not 'class' in res[0].attrs:
            iRow += 1
            resultat = soup.select(filtre.format(iRow, 4))
            continue

        classes = res[0]['class']

        if ('libellepetit' in classes) or ('libellepetitIi' in classes) or ('libellepetitiI' in classes):

            eurosHab = soup.select(filtre.format(iRow, 2))[0].text.replace('\xa0', '')
            moyenneStrate = soup.select(filtre.format(iRow, 3))[0].text.replace('\xa0', '')
            titleRow = soup.select(filtre.format(iRow, 4))[0].text.replace('\xa0', '')

            if 'G' in classes:
                whichTitle = 'Big'
            elif 'libellepetitIi' in classes:
                whichTitle = 'Little'
            else:
                whichTitle = 'Medium'

            crawl.append({'eurosPerHab': eurosHab, 'moyStrate': moyenneStrate, 'rowTitle': titleRow, 'cat': whichTitle})

        iRow += 1
        res = soup.select(filtre.format(iRow, 4))
		#Récuperer les données pour chaque colonne
        dataA = getData(crawl, '= A')
        dataB = getData(crawl, '= B')
        dataC = getData(crawl, '= C')
        dataD = getData(crawl, '= D')

        results[str(annee)] = {'A': dataA, 'B': dataB, 'C': dataC, 'D': dataD}

#On boucle sur les année puis sur le dico
for annee in Annees:
    print('                           ')
    print('                           ')
    print('====== Année: ' + str(annee))
    for cle, valeur in results[str(annee)].items():
        print(" ============= Colonne " + str(cle))
        print(" ======================Ligne 1 "+ str(valeur[0]))
        print(" ======================Ligne 2 "+ str(valeur[1]))
        print(" ======================Ligne 3 "+ str(valeur[2]))
        print(" ======================Ligne 4 "+ str(valeur[3]))
    print('                           ')
    print('                           ')
