import numpy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

col_dict = {'brand': '1-Marque', 'description': '4-Version', 'model': '2-Modele', 'price': '6-prix',
            'releaseDate': '3-Annee', 'B': '0-PROPAR', 'Kilometre': '5-kms'}
liste_region = ["ile_de_france" , "provence_alpes_cote_d_azur", "aquitaine"]

def replacerdescr(text):
    re_str1 = r"\s*.*(zen).*"
    re_str2 = r"\s*.*(life).*"
    re_str3 = r"\s*.*(intens).*"

    m1 = re.match(re_str1, text.lower())
    m2 = re.match(re_str2, text.lower())
    m3 = re.match(re_str3, text.lower())
    if m1 is None:
        if m2 is None:
            if m3 is None:
                sortie = "NT"
            else:
                sortie = "INTENS"
        else:
            sortie = "LIFE"
    else:
        sortie = "ZEN"
    return sortie


def nettoie(text):
    texts = text.replace(u'<span class="total_page">', '').replace(u'</span>', '')
    #    texts = text.replace(u'<span class="total_page">', ' ').replace('%C3%89', 'E').replace('%C3%AE', 'i').replace(
    #        '%C3%A9', 'é')
    return texts


def get_detail_zoe(complement_url):
    #    leboncoin_url_detail = 'https://www.leboncoin.fr/voitures/1018931643.htm?ca=12_s'
    leboncoin_url_detail = 'https:' + complement_url
    data = requests.get(leboncoin_url_detail)
    parser = BeautifulSoup(data.text, 'html.parser')
    properties = ['brand', 'model', 'releaseDate', 'price', 'description']
    info_zoe = {}
    node = parser.find(class_="adview_header")
    all_text = node.text
    for v in parser.findAll(class_= "property"):
        if v.text == "Kilométrage":
            kilo = v.parent.find(class_="value").text.replace(u'KM', '').replace(u' ', '')
            info_zoe["Kilometre"] = kilo
    for valeur in parser.findAll(class_=["value", "clearfix"]):
        try:
            #print(valeur.text)
            propriete = valeur.attrs['itemprop']
            if propriete in properties:
                try:
                    value = valeur.attrs['content']
                except KeyError:
                    value = valeur.text.strip()
                # print(value)
                if propriete == 'description':
                    value = replacerdescr(value.lower())
                    if value == "NT":
                        value = replacerdescr(all_text.lower())
                info_zoe[propriete] = value.lower()
        except KeyError:
            pass

        # print(info_zoe)
    return info_zoe


def get_liste_zoe(page, region):
    leboncoin_url = 'https://www.leboncoin.fr/voitures/offres/' + region + '/?th=' + str(page) + '&q=zoe&parrot=0&brd=Renault&mdl=Zoe'
    #leboncoin_url = 'https://www.leboncoin.fr/voitures/offres/'+ region + '/?o=' + str(page) + '&q=zoe'
    print(leboncoin_url)
    data = requests.get(leboncoin_url)
    # liste des voitures à récupérer
    print("Attente du résultat dans une minute, requêtes envoyées ")
    parser = BeautifulSoup(data.text, 'html.parser')
    nb_page = 0
    if page == 1:
        for li in parser.find_all(class_="total_page"):
            # print(li)
            nb_page = nettoie(str(li))
            print(nb_page)
    liste_url_detail_page = []
    liste_categorie = []
    for ref_page in parser.find_all(class_="list_item clearfix trackable"):
        #print(ref_page)
        url_detail = ref_page.attrs['href']
        #print(url_detail)
        #url_valide = url_detail[2:18]
        #print(url_valide)
        liste_url_detail_page.append(url_detail)
        # Récupération
        categorie = "par"
        for ref_pro in ref_page.findChildren(class_="ispro"):
            #        print(ref_page)
            categorie = "pro"
        # print(categorie)
        liste_categorie.append(categorie)
        categorie = "particulier"
    return liste_url_detail_page, nb_page, liste_categorie

for region in liste_region :
    liste_url_detail = []
    liste_cat = []
# recuperation des versions
    resultat, pages, liste_cat = get_liste_zoe(1, region)
#print(pages)
# print(liste_cat)
    page_max = int(pages)
    print(page_max)
    liste_url_detail.append(resultat)
    i = 2
    page_max = page_max + 1
    liste = []
    while i < page_max :
        print("tt")
        resultat, pagefin, liste = get_liste_zoe(i, region)
        liste_cat.extend(liste)
    #print("liste cat : " + str(liste_cat))
        liste_url_detail.append(resultat)
        i = i + 1

    liste_info_zoe = []
    for page in liste_url_detail:
        for voiture in page:
            liste_info_zoe.append(get_detail_zoe(voiture))

    df1 = pd.DataFrame(liste_cat, columns=['A'])
    df = pd.DataFrame(liste_info_zoe)
    df['B'] = df1['A']
    df2 = df.rename(columns=col_dict)
    df3 = df2.sort_index(axis=1, ascending=True)
    print(df3)
    df3.to_csv(region + '.csv')
