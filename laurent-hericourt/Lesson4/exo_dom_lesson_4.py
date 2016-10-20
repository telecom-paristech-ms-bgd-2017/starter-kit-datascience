from bs4 import BeautifulSoup
import pandas as pd
import re
import requests as req
import numpy as np


# Définition de constantes
URL_VOITURE = "//www.leboncoin.fr/voitures/"
liste_regions = ["ile_de_france", "provence_alpes_cote_d_azur", "aquitaine"]
liste_type = ['c', 'p']
liste_url_argus = {"ZEN TYPE 1": "http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide-2013.html",
                           "LIFE TYPE 1": "http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide-2013.html",
                           "INTENSE TYPE 1": "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide-2013.html",
                           "ZEN TYPE 2": "http://www.lacentrale.fr/cote-auto-renault-zoe-zen+charge+rapide+type+2-2013.html",
                           "LIFE TYPE 2": "http://www.lacentrale.fr/cote-auto-renault-zoe-life+charge+rapide+type+2-2013.html",
                           "INTENSE TYPE 2": "http://www.lacentrale.fr/cote-auto-renault-zoe-intens+charge+rapide+type+2-2013.html"}
detail_voitures = []


# Permet d'obtenir la liste des urls de chaque voiture
def get_liste_url_voitures(region, type, page):
    url = "https://www.leboncoin.fr/annonces/offres/" + region + "/?th=1&o="+str(page)+"&q=renault%20zoe&parrot=0&f=" + type
    html = req.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    urlvoitures_et_type = {}

    for a in soup.find_all('a', href=True):
        if URL_VOITURE in a['href']:
            urlvoitures_et_type["https://" + a['href'][2:]] = type
    return urlvoitures_et_type


# Permet d'obtenir le nombre de page de voitures qui correspondent à la recherche
def get_number_of_pages(region, type):
    url = "https://www.leboncoin.fr/annonces/offres/" + region + "/?th=1&q=renault%20zoe&parrot=0&f=" + type
    html = req.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    try:
        number_pages = soup.find(id="next").previous_sibling.previous_sibling.previous_sibling.previous_sibling.get_text()
    except:
        number_pages = 1

    return number_pages


# Fonction non utilisée car bloquée au bout de 5 appels par le bon coin
def get_telephone(url):
    list_id = re.findall('[0-9]+', url)[0]
    url_tel = req.get("https://www2.leboncoin.fr/ajapi/get/phone?list_id=" + list_id).text
    tel = req.get(url_tel).text
    return tel


# Permet de récupérer les informations sur les voitures et de les ajouter au dataframe
def add_car_in_array(urlvoitures_et_type):
    html = req.get(urlvoitures_et_type[0]).text
    soup = BeautifulSoup(html, "html.parser")
    type = urlvoitures_et_type[1]
    annee, km, prix, version = "NaN", "NaN", "NaN", "NaN"

    # Retrouve les informations année, km et prix
    liste_valeurs = soup.find_all("span", {"class": "value"})
    for valeur in liste_valeurs:
        if re.match('[0-9]{4}', valeur.text.strip()):
            annee = int(re.findall('[0-9]{4}', valeur.text.strip())[0])
        if re.match('(([0-9]+\s?)+)KM', valeur.text.strip()):
            km = int(re.findall('(([0-9]+\s?)+)KM', valeur.text.strip())[0][0].replace(u'\xa0', u' ').replace(" ", ""))
        if re.match('(([0-9]+\s?)+)€', valeur.text.strip()):
            prix = int(re.findall('(([0-9]+\s?)+)€', valeur.text.strip())[0][0].replace(u'\xa0', u' ').replace(" ", ""))

    # Retrouve la version
    description = soup.find_all(itemprop='description')
    if (description):
        if 'ZEN' in description[0].text.strip().upper():
            version = 'ZEN'

        elif 'LIFE' in description[0].text.strip().upper():
            version = 'LIFE'

        elif 'INTENS' in description[0].text.strip().upper():
            version = 'INTENSE'

    # Retouve le type
    if (description and version != "NaN"):
        if ('TYPE 2' or 'TYPE2') in description[0].text.strip().upper():
            version += ' TYPE 2'

        else:
            version += " TYPE 1"

    detail_voitures.append([version, annee, km, prix, "Nan", "NaN", type])


# Permet d'obetnir les prix pour une voiture à l'argus
def get_prix_from_argus(version, km):
    url = liste_url_argus[version]
    r = req.get(url)
    cookies = r.cookies
    headers = {
        'Referer': url,
    }

    r_prix = req.get("http://www.lacentrale.fr/cote_proxy.php?km="+str(km)+"&month=01", headers=headers, cookies=cookies)
    prix_json = r_prix.json()

    return int(prix_json["cote_perso"])

if __name__ == '__main__':
    for region in liste_regions:
        for type in liste_type:
            nbr_pages = int(get_number_of_pages(region, type)) + 1
            for page in range(1, nbr_pages):
                liste_url = get_liste_url_voitures(region, type, page)
                for voiture, type in liste_url.items():
                    add_car_in_array((voiture, type))

    df_voitures_boncoin_temp = pd.DataFrame(detail_voitures,
                                            columns=["version", "annee", "km", "prix", "prix_argus",
                                                    "telephones", "professionnel"])
    df_voitures_boncoin = df_voitures_boncoin_temp[(df_voitures_boncoin_temp["prix"] != "NaN") & (df_voitures_boncoin_temp["version"] != "NaN")]


    df_voitures_boncoin['prix_argus'] = df_voitures_boncoin.apply(axis=1,func= lambda x: get_prix_from_argus(x['version'],x['km']))

    df_voitures_boncoin['prix_au_dessus_argus'] = np.where(df_voitures_boncoin['prix'] > df_voitures_boncoin['prix_argus'], True, False)
    df_voitures_boncoin.to_csv('Analyse_voitures_boncoin.csv')

    print(df_voitures_boncoin)

