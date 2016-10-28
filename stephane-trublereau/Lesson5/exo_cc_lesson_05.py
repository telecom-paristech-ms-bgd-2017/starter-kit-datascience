# dans le cas des medicaments recuperer, l'ibuprofen, Levothyroxine l'ensemble des formes medicamenteuses :
# dosage, nb de comprimes, format
# molecule un dosage une forme galenique
# base publique des medicaments
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def nettoie(text):
    texts = text.replace(u'<a class="standart" href="extrait.php?', ''). \
        replace(u' title="Cliquez pour accéder à la fiche info et à la \
        liste des documents de référence du médicament :  ', ''). \
        replace(u'				</a>', '').replace(u'\t\t\t\t', '')
    return texts


def nettoie2(text):
    texts = text.replace(u'<a class="standart" href="extrait.php?', ''). \
        replace(u' title="Cliquez pour accéder à la fiche info et à la \
        liste des documents de référence du médicament :  ', ''). \
        replace(u'				</a>', '').replace(u'\t\t\t\t', '').\
        replace(u'%', ' %')
    return texts


# regex_selection = r'IBUPROFENE\s([\w\s]+)\s(\d+)\s?([a-zA-Z%]+),([\w\sé])((comprimé pelliculé)|(gel)|(comprimé enrobé))'
# pattern = re.compile(regex_selection)

regex_selection_court = r'([A-Z]+) (\d+) ([a-zA-Z%-Zµ]+),*(.*)'

regex = re.compile(regex_selection_court)
datas = {'page': '1', 'affliste': '0', 'affNumero': '0', 'isAlphabet': '0',
         'inClauseSubst': '0', 'nomSubstances': '',
         'typeRecherche': '0', 'choixRecherche': 'medicament',
         'paginationUsed': '0', 'txtCaracteres': 'IBUPROF',
         'btnMedic.x': '0', 'btnMedic.y': '10', 'btnMedix': 'Rechercher',
         'radLibelle': '2', 'txtCaracteresSub': '', 'radLibelleSub': '4'}
print(datas['page'])


# préparatiion des paramètres du post
# datas['page'] = 2
# print(datas['page'])



def get_liste_medic(nommedic, page, page_maximum, meds):
    print('page : ' + str(page))
    datas['page'] = str(page)
    datas['txtCaracteres'] = str(nommedic)
    req = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php', datas)
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup.get_text())
    # print(soup)
    objMax = soup.find(class_="navBarGauche")
    if objMax is not None and page_maximum == 99:
        maxPageReg = re.compile(r'\d+\s/\s(\d)+')
        page_maximum = int(maxPageReg.search(objMax.text).groups(1)[0])
    print(page_maximum)
    # Recuperation medicaments
    count = 0
    count1 = 0
    for listemedicaments in soup.findAll(class_="ResultRowDeno"):
        count = count + 1
        # print(str(listemedicaments.get_text()))
        name = None
        description = None
        quantity = None
        unity = None
        match = re.search(regex, nettoie(str(listemedicaments.get_text())))
        # print(str(listemedicaments.get_text()))
        if match:
            count1 = count1 + 1
            name = match.group(1)
            quantity = match.group(2)
            unity = match.group(3).replace (u',','')
            description = match.group(4)
            meds.append([name, quantity, unity, description])
        else:
            match = re.search(regex, nettoie2(str(listemedicaments.get_text())))
            if match:
                count1 = count1 + 1
                name = match.group(1)
                quantity = match.group(2)
                unity = match.group(3).replace (u',','')
                description = match.group(4)
                meds.append([name, quantity, unity, description])
            else :
                print(str(listemedicaments.get_text()))
    #print(count)
    #print(count1)
    # print(meds)
    if page >= page_maximum:
        return meds
    else:
        page = page + 1
        return get_liste_medic(nommedic, page, page_maximum, meds)


liste_nom_medicament = ['IBUPROFENE', 'LEVOTHY']
for nommedic in liste_nom_medicament:
    page_max = 99
    nb = 0
    meds = []
    meds = get_liste_medic(nommedic, 1, page_max, meds)
    for medic in meds:
        print(str(medic))
        if nb == 0:
            colonnes = ['name', 'quantity', 'unity', 'forme galenique']
        nb = nb + 1
    print(" Liste des formes médicamenteuses de " + nommedic )
    df = pd.DataFrame(meds, columns=colonnes)
    print(type(df))
    print(len(df))
    print(df.head(5))
    df.to_csv(nommedic + '.csv', index=False)